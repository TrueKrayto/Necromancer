import arcade
from game_sprites import BUILDING_TEXTURES

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
        self.offsets = building_offsets
        offset_x = self.get_offset_x(building)
        offset_y = self.get_offset_y(building)
        tile_center_x, tile_center_y = tile.get_center()
        self.sprite.center_x = tile_center_x
        self.sprite.center_y = tile_center_y
        self.sprite.width = (tile.get_scale() * size) + offset_x
        self.sprite.height = (tile.get_scale() * size) + offset_y

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
        
    
