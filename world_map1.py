import arcade
from arcade import Vec2
from map_tiles import Tile
from player import Player


class WorldMap1View(arcade.View):
    def __init__(self, game, map_size, scale):
        super().__init__()
        self.map_size = map_size
        self.scale = scale
        self.tile_grid = []
        self.game = game
        self.held_keys = set()
        self.camera = arcade.Camera2D()
        self.generate_tile_map()
        self.visible_tiles = []       
        
    def on_update(self, delta_time):
        self.game.player.update(delta_time, self.held_keys)
        self.center_camera_to_player()
        self.select_visible_tiles()
     

    def on_draw(self):
        self.clear()
        self.camera.use()
        for row in self.visible_tiles:
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
        center_y = y // 2
        self.game.player = Player(center_x, center_y, self.scale)
        
    def on_key_press(self, symbol, modifiers):
        self.held_keys.add(symbol)
        
    def on_key_release(self, symbol, modifiers):
        self.held_keys.discard(symbol)

    def center_camera_to_player(self):
        x, y = self.game.player.get_position()
        self.camera.position = Vec2(x,y)

    def get_tile_at(self, x, y):
        tile_index_x = int(x // self.scale)
        tile_index_y = int(y // self.scale)
        if 0 <= tile_index_y < len(self.tile_grid):
            if 0 <= tile_index_x < len(self.tile_grid[tile_index_y]):
                return self.tile_grid[tile_index_y][tile_index_x]
        return None
    
    def select_visible_tiles(self):        
        radius = 10
        self.visible_tiles.clear()
        player_pos_x, player_pos_y = self.game.player.get_position()
        print(f"Player position: {player_pos_x, player_pos_y}")
        current_tile = self.get_tile_at(player_pos_x, player_pos_y)
        if current_tile is None:             
             return
        
        tile_row, tile_col = current_tile.get_index()
        rows = self.slice_around(self.tile_grid, tile_row, radius)
        for row in rows:
            cols = self.slice_around(row, tile_col, radius)
            self.visible_tiles.append(cols)         
        
    def slice_around(self, lst, index, distance):
        start = max(index - distance, 0)
        end = index + distance + 1
        return lst[start:end]