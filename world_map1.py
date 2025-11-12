import arcade
from map_tiles import Tile
from player import Player


class WorldMap1View(arcade.View):
    def __init__(self, game, map_size, scale):
        super().__init__()
        self.map_size = map_size
        self.scale = scale
        self.tile_grid = []
        self.game = game
        self.generate_tile_map() 
        
                
    def on_draw(self):
        self.clear()
        for row in self.tile_grid:
            for tile in row:
                tile.draw()
        if self.game.player:
            self.game.player.draw()

    def on_show_view(self):        
        self.background_color = arcade.csscolor.WHITE
        if self.game.player == None:
            self.create_player()  

    def generate_tile_map(self):
        self.tile_grid.clear()
        for y in range(self.map_size):
            row = []
            for x in range(self.map_size):
                tile = Tile(x, y, self.scale)
                row.append(tile)
            self.tile_grid.append(row)

    def create_player(self):
        x, y = self.game.get_screen_dimensions()
        center_x = x // 2
        cente_y = y // 2
        self.game.player = Player(center_x, cente_y, self.scale)
        
        



