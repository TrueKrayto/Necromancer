import arcade
from crops import Seed, Plant

class FarmComponent:
    def __init__(self):
        self.tile = None
        self.center_x = None
        self.center_y = None
        self.planted = False
        self.assaigned = False

    def set_up(self, tile):
        self.tile = tile
        self.map = self.tile.map
        self.tile.type = "farm"
        self.tile.set_terrain("tilled earth")
        self.tile.set_passable(True)
        self.center_x, self.center_y = self.tile.get_center()
    
    def toggle_assaigned(self):
        self.assaigned = not self.assaigned

    def interact(self, item, user):
        if isinstance(item, Seed):           
            self.plant_seed(item)
    
    def plant_seed(self, seed):
        if self.planted:
            return
        else:            
            crop = Plant(seed.type, self.tile)
            self.tile.add_entity(crop)
            self.planted = True