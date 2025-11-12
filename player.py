import arcade
from game_sprites import PLAYER_SPRITES

class Player():
    def __init__(self, x, y, scale):
        self.sprite =arcade.Sprite(PLAYER_SPRITES["idle_1"], center_x=x, center_y=y)
        sprite_texture = arcade.load_texture(PLAYER_SPRITES["idle_1"])
        self.sprite.scale = scale / sprite_texture.width

        self.speed = 200
       
    def draw(self):
        arcade.draw_sprite(self.sprite)
   
    def get_position(self):
        return self.sprite.center_x, self.sprite.center_y

    def update(self, delta_time, held_keys):
        dx = dy = 0
        if arcade.key.LSHIFT in held_keys:
            speed = self.speed * 5
        else:
            speed = self.speed

        if arcade.key.W in held_keys or arcade.key.UP in held_keys:
            dy += speed
        if arcade.key.S in held_keys or arcade.key.DOWN in held_keys:
            dy -= speed
        if arcade.key.A in held_keys or arcade.key.LEFT in held_keys:
            dx -= speed
        if arcade.key.D in held_keys or arcade.key.RIGHT in held_keys:
            dx += speed
        if dx < 0:
            self.sprite.scale_x = -abs(self.sprite.scale_x)  # face left
        elif dx > 0:
            self.sprite.scale_x = abs(self.sprite.scale_x)  # face right

        new_x = self.sprite.center_x + dx * delta_time
        new_y = self.sprite.center_y + dy * delta_time

        self.sprite.center_x = new_x
        self.sprite.center_y = new_y