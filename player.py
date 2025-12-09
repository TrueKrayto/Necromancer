import arcade
from game_sprites import PLAYER_SPRITES
from crops import Seed

class Player:
    def __init__(self, x, y, scale):
        # Load texture only once
        texture = arcade.load_texture(PLAYER_SPRITES["idle_1"])

        # Create sprite
        self.sprite = arcade.Sprite(texture, center_x=x, center_y=y)

        # Scale so sprite matches your tile scale
        self.sprite.scale = scale / texture.width     
        self.speed = 200
        
        self.held_item = Seed("cabbage")
    # ------------------------------
    # Drawing
    # ------------------------------
    def draw(self):
        arcade.draw_sprite(self.sprite)

    # ------------------------------
    # Position helper
    # ------------------------------
    def get_position(self):
        return self.sprite.center_x, self.sprite.center_y

    # ------------------------------
    # Main movement & collision
    # ------------------------------
    def update(self, delta_time, held_keys, world):
        dx = dy = 0

        speed = self.speed * (5 if arcade.key.LSHIFT in held_keys else 1)

        # Y movement
        if arcade.key.W in held_keys or arcade.key.UP in held_keys:
            dy += speed
        if arcade.key.S in held_keys or arcade.key.DOWN in held_keys:
            dy -= speed

        # X movement + flipping
        if arcade.key.A in held_keys or arcade.key.LEFT in held_keys:
            dx -= speed
            self.sprite.scale_x = -abs(self.sprite.scale_x)
        elif arcade.key.D in held_keys or arcade.key.RIGHT in held_keys:
            dx += speed
            self.sprite.scale_x = abs(self.sprite.scale_x)

        # --- normalize diagonal speed ---
        if dx != 0 and dy != 0:
            dx *= 0.70710678  # 1/sqrt(2)
            dy *= 0.70710678

        # proposed new positions
        new_x = self.sprite.center_x + dx * delta_time
        new_y = self.sprite.center_y + dy * delta_time       
        
        # find position of feet + offset for sprite (Note in future may need dynamic offset if multiple sprites)
        offset = 50

        feet_y_current = self.sprite.center_y - (self.sprite.height / 2) + offset

        # X-axis collision
        if world.is_position_passable(new_x, feet_y_current):
            self.sprite.center_x = new_x

        # ---------------------------
        # Y-axis collision (check feet at NEW Y)
        # ---------------------------
        feet_y_new = new_y - (self.sprite.height / 2) + offset

        if world.is_position_passable(self.sprite.center_x, feet_y_new):
            # Move center, not feet
            self.sprite.center_y = new_y

    def interact(self, tile):
        tile.interact(self.held_item, self)