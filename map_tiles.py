import arcade
from game_sprites import TILE_TEXTURES

class Tile:
    def __init__(self, x, y, scale, terrain="grass"):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.scale = scale
        self.texture = TILE_TEXTURES.get(terrain, TILE_TEXTURES["grass"])
        self.sprite = arcade.Sprite(path_or_texture=self.texture)
        self.sprite.width = scale
        self.sprite.height = scale
        self.sprite.center_x = x * scale + scale / 2
        self.sprite.center_y = y * scale + scale / 2

    def get_sprite(self):
        return self.sprite

    def draw(self):
        arcade.draw_sprite(self.sprite)

    def set_terrain(self, terrain):               
        if terrain in TILE_TEXTURES:
            self.sprite.texture = TILE_TEXTURES[terrain]
            return
    
    def get_index(self):
        return self.y, self.x 