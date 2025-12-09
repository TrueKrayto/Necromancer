"""
Docstring for Necromancer.crops
The basic crop classes for planting farm tiles
"""
import arcade
from game_config import GAME_STATE
from game_sprites import PLANT_SPRITES

# dictionary to hold crop info hravest is a tuple (items, seeds)

plants = {
    "cabbage":{
        "growth time":30,
        "harvest":(5,5)
    }
}

class Seed:
    def __init__(self, type):
        self.type = type

class Plant:
    def __init__(self, type, tile):
        self.type = type
        self.tile = tile
        self.growth_stage = 0
        self.watered = False
        self.growing = False
        self.x, self.y = self.tile.get_center()
        self.sprite = arcade.Sprite(PLANT_SPRITES["planted_seed"])
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y
        base_scale = GAME_STATE["SCALE"] / self.sprite.width
        self.sprite.scale = base_scale  
      
    def get_sprite(self):
        return self.sprite

    def water(self):
        if not self.watered:
            self.watered = True

