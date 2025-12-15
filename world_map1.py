import arcade
import random
from pause_menu import PauseMenu
from arcade import Vec2
from map_tiles import Tile
from player import Player
from villages import Village
from buildings import Building
from npc import NPC
from villager import Villager
from map_tiles import Tile
from tile_map import TileMap
from WorldUI import WorldUI

WATER_CHANCE = 10

class WorldMap1View(arcade.View):
    def __init__(self, game, map_size, scale):
        super().__init__()
        self.map_size = map_size
        self.scale = scale        
        self.tile_sprite_list = arcade.SpriteList()
        self.building_sprite_list = arcade.SpriteList()
        self.npc_sprite_list = arcade.SpriteList()
        self.entity_sprite_list = arcade.SpriteList()
        self.npc_list = []
        self.game = game
        self.held_keys = set()
        self.camera = arcade.Camera2D()       
        self.visible_tiles = []  
        self.paused = False
        self.tree_manager = TempTreeManager()
        # UI manager
        self.world_ui = WorldUI(self)
        # setting up the map
        self.map = TileMap(self, self.map_size, self.map_size, Tile, self.scale)
        self.map.generate_map(set_up=True, sprite_list=self.tile_sprite_list)
        self.tile_grid = self.map.get_map()
        self.map_manager = self.map.manager
        
        # The pause menu  
        self.pause_menu = PauseMenu(self.game, self)
        self.pause_menu.pause_frame()
        #test
        self.test_village = None
        
    def on_update(self, delta_time):
        if not self.paused:
            if self.game.player:
                self.game.player.update(delta_time, self.held_keys, self)
                self.center_camera_to_player()
                # slightly redundant call, sprite list removes need for this
                self.select_visible_tiles()
            if self.test_village is not None:          
                self.test_village.manager.update(delta_time)
            self.tree_manager.update(delta_time)

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.world_ui.disable()
            self.pause_menu.manager.enable()
        else:
            self.pause_menu.manager.disable()
            self.world_ui.enable()

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.tile_sprite_list.draw()
        
        self.entity_sprite_list.draw()
        self.npc_sprite_list.draw()
        self.building_sprite_list.draw()
        
        if self.game.player:
            self.game.player.draw()       

        if self.paused:
            self.pause_menu.manager.draw()
        self.world_ui.manager.draw()

    def on_show_view(self):        
        self.background_color = arcade.csscolor.WHITE       
        
        if self.game.player is None:
            self.create_player()  

    def clear_all(self):
        self.tile_grid.clear()
        self.tile_sprite_list.clear()
        self.visible_tiles.clear()      

    def create_player(self):
        x, y = self.map_manager.center_of_map()       
        self.game.player = Player(x, y, self.scale)
        spawn_tile = self.map_manager.get_tile_at(x,y)
        spawn_area = self.map_manager.get_neighbours(spawn_tile, 2, flat=True)
        for tile in spawn_area:
            tile.set_terrain("black stone")
            tile.set_passable(True)
        
        # test village delete later
        row, col = spawn_tile.get_index()

        self.test_village = Village(spawn_tile, self)
        for building in self.test_village.get_buildings():
            self.building_sprite_list.append(building.get_sprite())
                    
    def on_mouse_press(self, x, y, button, modifiers):
            # -------------------------
            # LEFT CLICK (UI / buildings)
            # -------------------------
            if self.world_ui.has_active_panel():
                if self.world_ui.click_is_on_panel(x, y):
                    return
            if button == arcade.MOUSE_BUTTON_LEFT:
                world_x, world_y = self.get_world_pos(x, y)

                tile = self.map_manager.get_tile_at(world_x, world_y)                
                if not tile:
                    return

                if hasattr(tile, "building") and tile.building:
                    from building_panels import BuildingPanel
                    panel = BuildingPanel(self, tile.building, self.world_ui.manager)
                    self.world_ui.open_panel(panel)
                    return
                
            # -------------------------
            # RIGHT CLICK (Skeletons!!!!!)
            # -------------------------    
            if button == arcade.MOUSE_BUTTON_RIGHT:
                world_x, world_y = self.get_world_pos(x, y)
                for i in range(1000):
                    test_skeleton = Villager("skeleton", world_x, world_y, self, self.test_village)
                    test_skeleton.assign_job("farmer")
                    self.test_village.villager_list.append(test_skeleton)
                    self.building_sprite_list.append(test_skeleton.get_sprite())
                
    def get_world_pos(self, x, y):
        camera_x, camera_y = self.camera.position
        screen_w, screen_h = self.game.get_screen_dimensions()
        screen_center_x = screen_w // 2
        screen_center_y = screen_h // 2

        offset_x = x - screen_center_x
        offset_y = y - screen_center_y

        world_x = camera_x + offset_x
        world_y = camera_y + offset_y

        return world_x, world_y

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.toggle_pause()
        elif symbol == arcade.key.E and self.game.player:
            x, y = self.game.player.get_position()
            tile = self.map_manager.get_tile_at(x, y)
            self.game.player.interact(tile)        
        else:
            self.held_keys.add(symbol)
        
    def on_key_release(self, symbol, modifiers):
        self.held_keys.discard(symbol)

    def center_camera_to_player(self):
        x, y = self.game.player.get_position()
        self.camera.position = Vec2(x,y)

    def select_visible_tiles(self):        
        radius = 10
        self.visible_tiles.clear()
        player_pos_x, player_pos_y = self.game.player.get_position()        
        current_tile = self.map_manager.get_tile_at(player_pos_x, player_pos_y)
        if current_tile is None:             
             return
        
        tile_row, tile_col = current_tile.get_index()
        rows = self.map_manager.slice_around(self.map.tile_map, tile_row, radius)
        for row in rows:
            cols = self.map_manager.slice_around(row, tile_col, radius)
            self.visible_tiles.append(cols)                 


class TempTreeManager:
    def __init__(self, bucket_count=10, batch_interval=0.5):
        self.bucket_count = bucket_count
        self.batch_interval = batch_interval

        # buckets of trees
        self.buckets = [[] for _ in range(bucket_count)]

        # round-robin state
        self.current_bucket = 0
        self.timer = batch_interval

        # used for auto-assignment
        self._assign_index = 0

    def update(self, dt):
        self.timer -= dt
        if self.timer > 0:
            return

        # full growth time each tree should receive
        growth_delta = self.batch_interval * self.bucket_count

        bucket = self.buckets[self.current_bucket]
        for tree in bucket:
            tree.update(growth_delta)

        # advance to next bucket
        self.current_bucket = (self.current_bucket + 1) % self.bucket_count
        self.timer = self.batch_interval

    def add_tree(self, tree):
        # round-robin assignment to keep buckets balanced
        bucket_index = self._assign_index % self.bucket_count
        self.buckets[bucket_index].append(tree)
        self._assign_index += 1

    def remove_tree(self, tree):
        # trees are few compared to updates; linear search is fine
        for bucket in self.buckets:
            if tree in bucket:
                bucket.remove(tree)
                return
