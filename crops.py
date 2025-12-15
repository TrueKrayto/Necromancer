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
        "growth time":60,
        "growth stages":[40,10],
        "harvest":(5,5),
        "stage 1":PLANT_SPRITES["sprout"],
        "stage 2":PLANT_SPRITES["cabbage_plant"]
    }
}

class Seed:
    def __init__(self, type):
        self.type = type

class Plant:
    def __init__(self, type, tile):
        self.type = type
        self.data = plants[self.type]
        self.tile = tile
        self.growth_stage = 0
        self.watered = False
        self.growing = False
        self.harvest_ready = False
        self.x, self.y = self.tile.get_center()
        self.sprite = arcade.Sprite(PLANT_SPRITES["planted_seed"])
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y
        base_scale = GAME_STATE["SCALE"] / self.sprite.width
        self.sprite.scale = base_scale 
        self.growth_timer = self.data["growth time"]
        self.water_timer = 10
      
    def get_sprite(self):
        return self.sprite

    def water(self):
        if not self.watered:
            self.watered = True
            self.growing = True
            # Plants need less water as they grow
            self.water_timer = 10 + 10 * self.growth_stage

    def change_sprite(self, sprite_texture):
        self.sprite.texture = sprite_texture

    def update(self, delta_time):
        if self.growing:
            self.growth_timer -= delta_time
            if self.growth_timer <= 0:
                self.harvest_ready = True
            if not self.harvest_ready:
                self.water_timer -= delta_time
                if self.water_timer <= 0:
                    self.growing = False
                    self.watered = False

        if self.growth_stage < len(self.data["growth stages"]):
            if self.growth_timer <= self.data["growth stages"][self.growth_stage]:                
                self.growth_stage += 1
                self.change_sprite(self.data[f"stage {self.growth_stage}"])

    