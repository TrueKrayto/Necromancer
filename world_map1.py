import arcade
import random
from pause_menu import PauseMenu
from arcade import Vec2
from map_tiles import Tile
from player import Player
from test_script import test_village
from buildings import Building

WATER_CHANCE = 10

class WorldMap1View(arcade.View):
    def __init__(self, game, map_size, scale):
        super().__init__()
        self.map_size = map_size
        self.scale = scale
        self.tile_grid = []
        self.tile_sprite_list = arcade.SpriteList()
        self.building_sprite_list = arcade.SpriteList()
        self.game = game
        self.held_keys = set()
        self.camera = arcade.Camera2D()       
        self.visible_tiles = []  
        self.paused = False 
        # The pause menu  
        self.pause_menu = PauseMenu(self.game, self)
        self.pause_menu.pause_frame()
            
    def on_update(self, delta_time):
        if not self.paused:
            if self.game.player:
                self.game.player.update(delta_time, self.held_keys, self)
                self.center_camera_to_player()
                # slightly redundant call, sprite list removes need for this
                self.select_visible_tiles()
     
    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_menu.manager.enable()
        else:
            self.pause_menu.manager.disable()

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.tile_sprite_list.draw()
        self.building_sprite_list.draw()

        if self.game.player:
            self.game.player.draw() 

        if self.paused:
            self.pause_menu.manager.draw()

    def on_show_view(self):        
        self.background_color = arcade.csscolor.WHITE        
        if not self.tile_grid:
            self.generate_tile_map()
        if self.game.player is None:
            self.create_player()  

    def clear_all(self):
        self.tile_grid.clear()
        self.tile_sprite_list.clear()
        self.visible_tiles.clear()

    def generate_tile_map(self):
        self.tile_grid.clear()
        for y in range(self.map_size):
            row = []
            for x in range(self.map_size):
                tile = Tile(x, y, self.scale, self)
                if random.randint(0,100) <= WATER_CHANCE:
                    tile.set_terrain("water")
                    tile.set_passable(False)
                row.append(tile)
                self.tile_sprite_list.append(tile.get_sprite())
            self.tile_grid.append(row)        

    def create_player(self):
        x, y = self.center_of_map()       
        self.game.player = Player(x, y, self.scale)
        spawn_tile = self.get_tile_at(x,y)
        spawn_area = self.get_neighbours(spawn_tile, 1, flat=True)
        for tile in spawn_area:
            tile.set_terrain("black stone")
            tile.set_passable(True)
        
        # test village delete later
        row, col = spawn_tile.get_index()
        self.create_village(test_village, row + 50, col)
        test_house = Building("house 1", spawn_tile, 3)
        self.building_sprite_list.append(test_house.get_sprite())

    def is_position_passable(self, x, y):
        tile = self.get_tile_at(x, y)
        if tile is None:
            return False
        return tile.passable

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.toggle_pause()
        else:
            self.held_keys.add(symbol)
        
    def on_key_release(self, symbol, modifiers):
        self.held_keys.discard(symbol)

    def center_camera_to_player(self):
        x, y = self.game.player.get_position()
        self.camera.position = Vec2(x,y)

    def get_tile_at(self, x, y):
        tile_index_x = int(x // self.scale)
        tile_index_y = int(y // self.scale)
        if 0 <= tile_index_y < len(self.tile_grid):
            if 0 <= tile_index_x < len(self.tile_grid[tile_index_y]):
                return self.tile_grid[tile_index_y][tile_index_x]
        return None
    
    def get_tile_at_index(self, row, col):
        if row > len(self.tile_grid) or row < 0:
            return None
        if col > len(self.tile_grid[row]) or col < 0:
            return None
        return self.tile_grid[row][col]

    def select_visible_tiles(self):        
        radius = 10
        self.visible_tiles.clear()
        player_pos_x, player_pos_y = self.game.player.get_position()        
        current_tile = self.get_tile_at(player_pos_x, player_pos_y)
        if current_tile is None:             
             return
        
        tile_row, tile_col = current_tile.get_index()
        rows = self.slice_around(self.tile_grid, tile_row, radius)
        for row in rows:
            cols = self.slice_around(row, tile_col, radius)
            self.visible_tiles.append(cols)         
        
    def slice_around(self, lst, index, distance):
        start = max(index - distance, 0)
        end = index + distance + 1
        return lst[start:end]
    
    def center_of_map(self):
        mid_y = len(self.tile_grid) // 2          
        mid_x = len(self.tile_grid[mid_y]) // 2          
        return self.tile_grid[mid_y][mid_x].get_center()
    
    def get_neighbours(self, tile, distance, grid=None, flat=False, include_center=True):
        neighbours = []
        row, col = tile.get_index()

        rows_in_range = self.slice_around(self.tile_grid, row, distance)
        for r in rows_in_range:
            cols_in_range = self.slice_around(r, col, distance)
            neighbours.append(cols_in_range)

        # Flatten if requested
        if flat:
            flat_list = [t for row in neighbours for t in row]
        
            if not include_center:
                flat_list = [t for t in flat_list if t is not tile]
        
            return flat_list

        # If not flat, remove center tile from 2D result if needed
        if not include_center:
            for r in neighbours:
                if tile in r:
                    r.remove(tile)

        return neighbours

    def create_village(self, village, row, col):     
        radius = village["size"] // 2  

        center_tile = self.get_tile_at_index(row, col)        
        village_area = self.get_neighbours(center_tile, radius)
        # reverse the grid for accurate indexing
        village_area.reverse() 
       
        for row in village_area:
            for tile in row:
                tile.set_terrain("dirt path")
                tile.set_passable(True)

        if "well" in village:
            row = village["well"]["row"]
            col = village["well"]["col"]
            tile = village_area[row][col]
            tile.set_terrain("water")
            tile.set_passable(False)

        if "inn" in village:
            row = village["inn"]["row"]
            col = village["inn"]["col"]
            tile = village_area[row][col]
            size = village["inn"]["size"] // 2
            inn_area = self.get_neighbours(tile, size)
            for row in inn_area:
                for tile in row:
                    tile.set_terrain("black stone")
                    tile.set_passable(False)

        if "warehouse" in village:
            row = village["warehouse"]["row"]
            col = village["warehouse"]["col"]
            tile = village_area[row][col]
            size = village["warehouse"]["size"] // 2
            inn_area = self.get_neighbours(tile, size)
            for row in inn_area:
                for tile in row:
                    tile.set_terrain("black stone")
                    tile.set_passable(False)

        if "shop" in village:
            row = village["shop"]["row"]
            col = village["shop"]["col"]
            tile = village_area[row][col]
            size = village["shop"]["size"] // 2
            inn_area = self.get_neighbours(tile, size)
            for row in inn_area:
                for tile in row:
                    tile.set_terrain("black stone")
                    tile.set_passable(False)

        if "barn" in village:
            row = village["barn"]["row"]
            col = village["barn"]["col"]
            tile = village_area[row][col]
            size = village["barn"]["size"] // 2
            inn_area = self.get_neighbours(tile, size)
            for row in inn_area:
                for tile in row:
                    tile.set_terrain("black stone")
                    tile.set_passable(False)

        if "houses" in village:
            size = village["houses"]["size"] // 2
            for row, cols in village["houses"]["coords"].items():
                for col in cols:
                    tile = village_area[row][col]
                    house_area = self.get_neighbours(tile, size)
                    for area_row in house_area:
                        for tile in area_row:
                            tile.set_terrain("black stone")
                            tile.set_passable(False)

        if "stalls" in village:
            for row, cols in village["stalls"]["coords"].items():
                for col in cols:
                    tile = village_area[row][col]
                    tile.set_terrain("black stone")
                    tile.set_passable(False)

        if "paths" in village:
            for row, cols in village["paths"]["coords"].items():
                for col in cols:
                    tile = village_area[row][col]
                    tile.set_terrain("stone path")
                    tile.set_passable(True)

        if "farms" in village:
            for row, cols in village["farms"]["coords"].items():
                for col in cols:
                    tile = village_area[row][col]
                    tile.set_terrain("tilled earth")
                    tile.set_passable(True)

        