import arcade
from crops import Seed, Plant

class FarmComponent:
    def __init__(self):
        self.tile = None
        self.center_x = None
        self.center_y = None
        self.planted = False
        self.assigned = False
        self.crop = None

    def set_up(self, tile):
        self.tile = tile
        self.map = self.tile.map
        self.tile.type = "farm"
        self.tile.set_terrain("tilled earth")
        self.tile.set_passable(True)
        self.center_x, self.center_y = self.tile.get_center()
    
    def toggle_assign(self):
        self.assigned = not self.assigned

    def assign(self):
        self.assigned = True

    def unassign(self):
        self.assigned = False

    def interact(self, item, user):
        if isinstance(item, Seed):           
            self.plant_seed(item)
    
    def plant_seed(self, seed):
        if self.planted:
            return
        else:            
            crop = Plant(seed.type, self.tile)
            self.crop = crop
            self.tile.add_entity(crop)
            self.planted = True

    def harvest(self, worker):
        self.tile.remove_entity(self.crop)
        self.crop = None
        self.planted = False