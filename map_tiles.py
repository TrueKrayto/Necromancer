import arcade
from game_sprites import TILE_TEXTURES

class Tile:
    def __init__(self, x, y, scale, terrain="grass"):
        self.x = x
        self.y = y
        self.terrain = terrain

        self.texture = TILE_TEXTURES.get(terrain, TILE_TEXTURES["grass"])
        self.sprite = arcade.Sprite(center_x=x * scale + scale // 2,
                                    center_y=y * scale + scale // 2)
        self.sprite.texture = self.texture
        self.sprite.scale = scale / self.texture.width

    def draw(self):
        arcade.draw_sprite(self.sprite)