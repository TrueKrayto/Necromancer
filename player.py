import arcade
from game_sprites import PLAYER_SPRITES

class Player():
    def __init__(self, scale):
        self.sprite =arcade.Sprite(PLAYER_SPRITES["idle_1"])
        sprite_texture = arcade.load_texture(PLAYER_SPRITES["idle_1"])
        self.sprite.scale = scale / sprite_texture.width        

    def draw(self):
        arcade.draw_sprite(self.sprite)

    