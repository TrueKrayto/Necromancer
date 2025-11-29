import arcade
import random
from farm_tile import FarmComponent
from buildings import Building
from layouts import village_layouts

class Village:
    def __init__(self, tile, map):
        self.map = map
        self.center_tile = tile
        self.buildings = []
        self.layout = random.choice(village_layouts)
        self.village_radius = self.layout["size"] // 2
        self.village_area = self.map.get_neighbours(self.center_tile, self.village_radius)
        # reverse the grid for accurate indexing
        self.village_area.reverse()
        #array to hold the farm tiles for npc access
        self.farm_tiles = []

        self.set_up()

    def get_buildings(self):
        return self.buildings

    def set_up(self):
        self.clear_ground()
        self.large_buildings()
        self.small_buildings()
        self.houses()
        self.wells()
        self.terrain()

    def clear_ground(self):
        # clears the tiles in the village sets them to passable and default terrain
        for row in self.village_area:
            for tile in row:
                tile.set_terrain("grass")
                tile.set_passable(True)

    def add_building(self, building, tile, size):
        building = Building(building, tile, size)
        self.buildings.append(building)

    def large_buildings(self):
        buildings = ["inn", "shop", "barn", "warehouse"]
        for name in buildings:
            if name in self.layout:
                row = self.layout[name]["row"]
                col = self.layout[name]["col"]
                tile = self.village_area[row][col]
                self.add_building(name, tile, self.layout[name]["size"])
                size = self.layout[name]["size"] // 2
                area = self.map.get_neighbours(tile, size)
                for area_row in area:
                    for tile in area_row:
                        tile.set_passable(False)

    def small_buildings(self):
        buildings = ["stalls"]

        for name in buildings:
            if name in self.layout:                
                for row, cols in self.layout[name]["coords"].items():
                    for col in cols:
                        tile = self.village_area[row][col]
                        tile.set_passable(False)
                        self.add_building("stall", tile, self.layout[name]["size"])                  

    def houses(self):
        if "houses" in self.layout:
            size = self.layout["houses"]["size"] // 2
            for row, cols in self.layout["houses"]["coords"].items():
                for col in cols:
                    tile = self.village_area[row][col]
                    # in the future add a random selection for different house textures
                    self.add_building("house 1", tile, self.layout["houses"]["size"])
                    house_area = self.map.get_neighbours(tile, size)
                    for area_row in house_area:
                        for tile in area_row:                            
                            tile.set_passable(False)

    def wells(self):
        if "well" in self.layout:
            row = self.layout["well"]["row"]
            col = self.layout["well"]["col"]
            tile = self.village_area[row][col]
            tile.set_terrain("black stone")            
            tile.set_passable(False)
            self.add_building("well", tile, self.layout["well"]["size"])

    def terrain(self):
        terrains = [("paths", "stone path"), ("farms", "tilled earth")]
        for terrain in terrains:
            name, texture = terrain
            if name in self.layout:
                for row, cols in self.layout[name]["coords"].items():
                    for col in cols:
                        tile = self.village_area[row][col]
                        if name == "farms":
                            tile.add_component(FarmComponent())
                            self.farm_tiles.append(tile)
                        tile.set_terrain(texture)
                        
 