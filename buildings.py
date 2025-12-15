import arcade
from game_sprites import BUILDING_TEXTURES
from pause_menu import PauseMenu
# offsets required for variations in sprite size
building_offsets = {
                "house 1" : [200, 200],
                "shop" : [300, 100],
                "inn" : [400, 150],
                "warehouse" : [400, 200],
                "barn" : [400, 200],
                "well" : [100, 100],
                "stall" : [50, 50]
            }


class Building:
    def __init__(self, building, tile, size):
        if building in BUILDING_TEXTURES:
            self.sprite = arcade.Sprite(BUILDING_TEXTURES[building])
        self.building = building
        self.building_type = building
        self.offsets = building_offsets
        offset_x = self.get_offset_x(building)
        offset_y = self.get_offset_y(building)
        tile_center_x, tile_center_y = tile.get_center()
        self.sprite.center_x = tile_center_x
        self.sprite.center_y = tile_center_y
        self.sprite.width = (tile.get_scale() * size) + offset_x
        self.sprite.height = (tile.get_scale() * size) + offset_y
        self.tile = tile
        self.size = size
        self.entrance_tile = None
        self.set_up()

    def set_up(self):
        self.map = self.tile.map   

        center_row, center_col = self.tile.get_index()
        offset = (self.size // 2) + 1

        self.entrance_tile = self.map.map_manager.get_tile_at_index(center_row - offset, center_col)
        self.entrance_tile.add_component(BuildinInteriorComponent())     
        radius = self.size // 2  
         
        owned_tiles = self.map.map_manager.get_neighbours(self.tile, radius, flat=True)
        for tile in owned_tiles:
            tile.set_passable(False)
            tile.building = self

    def get_entrance(self):
        return self.entrance_tile

    def get_sprite(self):
        return self.sprite

    def get_offset_x(self, building):
        if building in self.offsets:
            return self.offsets[building][0]    
        return 0
        
    def get_offset_y(self, building):
        if building in self.offsets:
            return self.offsets[building][1]  
        return 0
        
class BuildinInteriorComponent:
    def __init__(self,):
       pass

    def set_up(self, tile):
        self.game = tile.map.game

    def interact(self, object, user):
        self.game.show_view(self.game.building_interior)
        

class BuildingInteriorView(arcade.View):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.pause_menu = PauseMenu(self.game, self)
        self.pause_menu.pause_frame()
        self.paused = False

    def on_draw(self):
        self.clear()
        if self.paused:
            self.pause_menu.manager.draw()

    def on_hide_view(self):
        self.pause_menu.manager.disable()

    def clear_all(self):
        pass

    def toggle_pause(self):        
        self.paused = not self.paused
        if self.paused:
            self.pause_menu.manager.enable()
        else:
            self.pause_menu.manager.disable()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.toggle_pause()