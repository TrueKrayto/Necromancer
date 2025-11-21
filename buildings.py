import arcade
from game_sprites import BUILDING_TEXTURES

class Building:
    def __init__(self, building, tile, size):
        if building in BUILDING_TEXTURES:
            self.sprite = arcade.Sprite(BUILDING_TEXTURES[building])
        tile_center_x, tile_center_y = tile.get_center()
        self.sprite.center_x = tile_center_x
        self.sprite.center_y = tile_center_y
        self.sprite.width = tile.get_scale() * size
        self.sprite.height = tile.get_scale() * size

    def get_sprite(self):
        return self.sprite

        