import arcade
from map_tiles import Tile


class WorldMap1View(arcade.View):
    def __init__(self, map_size, scale):
        super().__init__()
        self.map_size = map_size
        self.scale = scale
        self.tile_grid = []
        self.generate_tile_map()
        
    def on_draw(self):
        self.clear()
        for row in self.tile_grid:
            for tile in row:
                tile.draw()

    def on_show_view(self):        
        self.background_color = arcade.csscolor.WHITE   

    def generate_tile_map(self):
        self.tile_grid.clear()
        for y in range(self.map_size):
            row = []
            for x in range(self.map_size):
                tile = Tile(x, y, self.scale)
                row.append(tile)
            self.tile_grid.append(row)



