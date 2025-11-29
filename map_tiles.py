import arcade
from game_sprites import TILE_TEXTURES

class Tile:
    def __init__(self, x, y, scale, map, terrain="grass"):
        self.map = map
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
        self.passable = True
        self.has_entity = False
        self.entities = []

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

    def get_sprite(self):
        return self.sprite

    def draw(self):
        arcade.draw_sprite(self.sprite)

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