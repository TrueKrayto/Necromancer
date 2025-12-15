import arcade
import re
import random
from villager import Villager
from farm_tile import FarmComponent
from buildings import Building
from layouts import village_layouts
import tasks as NewTask

class Village:
    def __init__(self, tile, map):
        self.map = map
        self.villager_list = []
        self.center_tile = tile
        self.buildings = []
        self.layout = random.choice(village_layouts)
        self.village_radius = self.layout["size"] // 2
        self.village_area = self.map.map_manager.get_neighbours(self.center_tile, self.village_radius)
        self.village_hinterland_radius = self.layout["size"]
        self.village_hinterland_tiles = []
        # reverse the grid for accurate indexing
        self.village_area.reverse()
        #array to hold the farm tiles for npc access
        self.farm_tiles = []        
        self.manager = VillageManager(self)
        self.set_up()
        

    def get_buildings(self):
        return self.buildings

    def set_up(self):
        self.clear_ground()
        self.terrain()
        self.large_buildings()
        self.small_buildings()
        self.houses()
        self.wells()
        self.villagers()
        self.define_hinterland()
        
    def clear_ground(self):
        # clears the tiles in the village sets them to passable and default terrain
        for row in self.village_area:
            for tile in row:
                tile.set_terrain("grass")
                tile.set_passable(True)
                tile.clear_entities()

    def define_hinterland(self):
        total_area = self.map.map_manager.get_neighbours(self.center_tile, self.village_hinterland_radius, flat=True)
        village_tiles = set(self.map.map_manager.get_neighbours(self.center_tile, self.village_radius, flat=True))
        self.village_hinterland_tiles = [tile for tile in total_area if tile not in village_tiles]

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
                

    def small_buildings(self):
        buildings = ["stalls"]

        for name in buildings:
            if name in self.layout:                
                for row, cols in self.layout[name]["coords"].items():
                    for col in cols:
                        tile = self.village_area[row][col]                        
                        self.add_building("stall", tile, self.layout[name]["size"])                  

    def houses(self):
        if "houses" in self.layout:
            size = self.layout["houses"]["size"] // 2
            for row, cols in self.layout["houses"]["coords"].items():
                for col in cols:
                    tile = self.village_area[row][col]
                    # in the future add a random selection for different house textures
                    self.add_building("house 1", tile, self.layout["houses"]["size"])
                    

    def wells(self):
        if "well" in self.layout:
            row = self.layout["well"]["row"]
            col = self.layout["well"]["col"]
            tile = self.village_area[row][col]
            tile.set_terrain("black stone")          
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
                        
    def villagers(self):      
        for building in self.buildings:
            text = building.building_type
            if re.search(r"\bhouse\b", text):
               tile = building.get_entrance()
               x, y = tile.get_center()
               male = Villager("elf man", x, y, self.map, self)
               self.villager_list.append(male)
               female = Villager("elf woman", x, y, self.map, self)
               #female.assign_job("farmer")
               self.villager_list.append(female)

        for villager in self.villager_list:
            sprite = villager.get_sprite()
            self.map.npc_sprite_list.append(sprite)
            self.map.npc_list.append(villager)

        
class VillageManager:
    def __init__(self, village):
        self.village = village
        self.faction = None
        self.available_tasks = TaskQue()
        self.active_tasks = []
        self.completed_tasks = []
        self.task_refresh_rate = 10
        self.task_timer = 10
        
    def update(self, delta_time):
        self.task_timer -= delta_time
        if self.task_timer <= 0:
            self.check_for_farm_tasks()
            self.task_timer = self.task_refresh_rate
        for villager in self.village.villager_list:
            villager.update(delta_time)
        for tile in self.village.farm_tiles:
            farm = tile.component
            if isinstance(farm, FarmComponent) and farm.crop:
                farm.crop.update(delta_time)
        
    def complete_task(self, task):
        component = task.tile.component
        if component and hasattr(component, "unassign"):
            component.unassign()
        self.active_tasks.remove(task)
        self.completed_tasks.append(task)
        task.task_completed = True

    def choose_task(self, worker):
        self.available_tasks.sort_tasks()
        task = self.available_tasks.get_task(worker)
        if task:
            self.active_tasks.append(task)
            return task

    def select_seed(self):
        # will add logic here later to allow the manager to choose which crops to grow
        return "cabbage"

    def check_for_farm_tasks(self):
        for tile in self.village.village_hinterland_tiles:
            if tile.tree is not None and tile.tree.assigned is False and tile.tree.grown:
                neighbours = self.village.map.map_manager.get_neighbours(tile, 1, flat=True)
                free_tiles = []
                for neighbour in neighbours:
                    if neighbour.passable:
                        free_tiles.append(neighbour)
                if free_tiles:
                    choice = free_tiles[0]
                    tile.tree.assigned = True
                    task = NewTask.FellTreeTask("farmer", tile)
                    task.set_location(choice)
                    self.available_tasks.add_task(task)

        if hasattr(self.village, "farm_tiles"):
            for tile in self.village.farm_tiles:                                    
                farm = tile.component
                if not farm.planted and not farm.assigned:
                    farm.assign() # <-- added assign/unassign methods to avoid toggling
                    seed = self.select_seed()
                    task = NewTask.PlantTask("farmer", tile, seed)
                    self.available_tasks.add_task(task)
                if farm.planted and not farm.crop.watered and not farm.assigned:
                    farm.assign()
                    task = NewTask.WaterTask("farmer", tile)
                    self.available_tasks.add_task(task)
                if farm.planted and not farm.assigned and farm.crop.harvest_ready:
                    farm.assign()
                    task = NewTask.HarvestTask("farmer", tile)
                    self.available_tasks.add_task(task)
                            
class TaskQue:
    def __init__(self):
        self.que = []

    def add_task(self, task):
        self.que.insert(0, task)

    def get_task(self, worker):
        for i, task in enumerate(self.que):
            if task.required_job == worker.job or task.required_job is None:
                return self.que.pop(i)
        return None
    
    def sort_tasks(self):
        # always keep the lowest priotity first -> this way i know 0 will always be the most important task
        if self.que:
            self.que.sort(key=lambda task: task.priority)

