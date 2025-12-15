"""
Docstring for Necromancer.tile_map
The class to create and manage maps
- Requires a map tile object
"""

class TileMap:
    def __init__(self, view, width, height, tile_class, scale):
        self.view = view        
        self.width = width
        self.height = height
        self.tile_class = tile_class
        self.scale = scale        
        self.tile_map = []
        self.manager = MapManager(self, self.view)

    def generate_map(self, set_up=False, sprite_list=None):                     
        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile = self.tile_class(x, y, self.scale, self.view)
                if set_up:
                    tile.set_up()
                if sprite_list is not None:                    
                    sprite_list.append(tile.get_sprite())
                row.append(tile)
            self.tile_map.append(row)
                
    def get_map(self):
        return self.tile_map
    
class MapManager:
    def __init__(self, map, view):
        self.map = map
        self.scale = self.map.scale
        self.view = view

    def is_position_passable(self, x, y):
        tile = self.get_tile_at(x, y)
        if tile is None:
            return False
        return tile.passable
    
    def get_tile_at(self, x, y):
        tile_index_x = int(x // self.scale)
        tile_index_y = int(y // self.scale)
        if 0 <= tile_index_y < len(self.map.tile_map):
            if 0 <= tile_index_x < len(self.map.tile_map[tile_index_y]):
                return self.map.tile_map[tile_index_y][tile_index_x]
        return None

    def get_tile_at_index(self, row, col):
        if row >= len(self.map.tile_map) or row < 0:
            return None
        if col >= len(self.map.tile_map[row]) or col < 0:
            return None
        return self.map.tile_map[row][col]
    
    def center_of_map(self):
        mid_y = len(self.map.tile_map) // 2          
        mid_x = len(self.map.tile_map[mid_y]) // 2          
        return self.map.tile_map[mid_y][mid_x].get_center()
    
    def slice_around(self, lst, index, distance):
        start = max(index - distance, 0)
        end = index + distance + 1
        return lst[start:end]

    def get_neighbours(self, tile, distance, flat=False, include_center=True, mutator=None):
        neighbours = []
        row, col = tile.get_index()

        rows_in_range = self.slice_around(self.map.tile_map, row, distance)
        for r in rows_in_range:
            cols_in_range = self.slice_around(r, col, distance)
            if mutator:
                for t in cols_in_range:
                    mutator(t)
            neighbours.append(cols_in_range)

        # Flatten if requested
        if flat:
            flat_list = [t for row in neighbours for t in row]
        
            if not include_center:
                flat_list = [t for t in flat_list if t is not tile]            
            return flat_list

        # If not flat, remove center tile from 2D result if needed
        if not include_center:
            for r in neighbours:
                if tile in r:
                    r.remove(tile)

        return neighbours