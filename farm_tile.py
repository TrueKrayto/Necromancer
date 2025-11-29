import arcade

class FarmComponent:
    def __init__(self):
        self.tile = None
        self.center_x = None
        self.center_y = None
        self.planted = False

    def set_up(self, tile):
        self.tile = tile
        self.tile.type = "farm"
        self.tile.set_terrain("tilled earth")
        self.tile.set_passable(True)
        self.center_x, self.center_y = self.tile.get_center()

    def interact(self, item, user):
        pass