import arcade
import random
from game_sprites import TILE_TEXTURES
from trees import Tree
from game_config import GAME_STATE

class Tile:
    def __init__(self, x, y, scale, map, terrain="grass"):
        self.map = map
        self.game_state = GAME_STATE
        # sprite
        self.x = x
        self.y = y
        self.terrain = terrain
        self.scale = scale
        self.texture = TILE_TEXTURES.get(terrain, TILE_TEXTURES["grass"])
        self.sprite = arcade.Sprite(path_or_texture=self.texture)
        self.sprite.width = scale
        self.sprite.height = scale
        self.sprite.center_x = x * scale + scale / 2
        self.sprite.center_y = y * scale + scale / 2
        # Current component - the type of tile
        self.component = None
        self.type = "Map tile"
        # flags
        self.has_tree = False
        self.tree = None
        self.passable = True
        self.has_entity = False
        self.building = None
        self.entities = []

    def set_up(self):
        if random.randint(0,100) <= self.game_state["tile data"]["trees"]["chance"]: # percentage tree chance, fix later
            self.plant_tree("pine")                    
            if random.randint(0,100) <= self.game_state["tile data"]["trees"]["mature"]:
                self.tree.grow_to_mature()
        elif random.randint(0,100) <= self.game_state["tile data"]["water chance"]:
            self.set_terrain("water")
            self.set_passable(False)

    def plant_tree(self, tree_type):
        if self.has_tree:
            return
        if self.map.tree_manager:            
            self.tree = Tree(tree_type, self)
            self.map.tree_manager.add_tree(self.tree)
            self.add_entity(self.tree)
            self.has_tree = True
            self.passable = False

    def remove_tree(self, tree):
        if self.tree is tree:
            self.tree = None

        self.remove_entity(tree)
        self.has_tree = False
        self.passable = True

        if self.map.tree_manager:
            self.map.tree_manager.remove_tree(tree)

    def add_component(self, component):
        self.component = component
        self.component.set_up(self)

    def interact(self, item, user):
        if self.component:            
            self.component.interact(item, user)
        return

    def set_passable(self, value):
        if value == True or value == False:
            self.passable = value
        return

    def add_entity(self, entity):             
        self.entities.append(entity)
        self.has_entity = True
        if hasattr(entity, "sprite") and entity.sprite:                    
                    self.map.entity_sprite_list.append(entity.get_sprite())

    def clear_entities(self):
        for entity in self.entities:
            self.remove_entity(entity)

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

            if not self.entities:
                self.has_entity = False

            sprite = entity.get_sprite()
            if sprite:
                self.remove_sprite(sprite)

    def remove_sprite(self, sprite):
        if sprite in self.map.entity_sprite_list:
            self.map.entity_sprite_list.remove(sprite)

    def get_sprite(self):
        return self.sprite

    def draw(self):
        # this draw function is obsolete only use for testing
        # add sprites to appropriate View sprite lists                           
        pass

    def set_terrain(self, terrain):               
        if terrain in TILE_TEXTURES:
            self.sprite.texture = TILE_TEXTURES[terrain]
            self.terrain = terrain
            return
    
    def get_index(self):
        return self.y, self.x 
    
    def get_center(self):
        return self.sprite.center_x, self.sprite.center_y
    
    def get_scale(self):
        return self.scale
    
    def get_entities(self):
         return self.entities