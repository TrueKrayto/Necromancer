"""
Docstring for Necromancer.trees
"""

import arcade
from game_config import GAME_STATE
from game_sprites import TREE_SPRITES

TREES = {
    # Pine Tree
    "pine":{"max_stage":3, "hp":3, "yield":(10,2),
        "stage":{
        1:{"sprite":TREE_SPRITES["planted_seed"], "time":30},
        2:{"sprite":TREE_SPRITES["sapling"], "time":60},
        3:{"sprite":TREE_SPRITES["pine_tree"], "time":20},
        }
    },
    # Next tree
}

class Tree:
    def __init__(self, tree_type, tile):
        self.assigned = False
        self.tree_type = tree_type
        self.tile = tile
        self.data = TREES[self.tree_type]
        self.current_stage = 1
        self.health = self.data["hp"]   
        self.x, self.y = self.tile.get_center()
        self.sprite = arcade.Sprite(self.data["stage"][self.current_stage]["sprite"])
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y
        base_scale = GAME_STATE["SCALE"] / self.sprite.width
        self.sprite.scale = base_scale 
        self.growth_timer = self.data["stage"][self.current_stage]["time"]


    @property
    def grown(self):
        return self.current_stage == self.data["max_stage"]

    def grow_to_mature(self):
        # method to allow the map/abilities to set trees to maturity
        self.current_stage = self.data["max_stage"]
        stage_data = self.data["stage"][self.current_stage]

        self.change_sprite(stage_data["sprite"])
        self.growth_timer = stage_data["time"]    

    def chop(self):
        self.health -= 1
        if self.health <= 0:
            self.fell()
    
    def fell(self):
        # for now just remove tree from tile, later handle drops
        self.tile.remove_tree(self)

    def get_sprite(self):
        return self.sprite
    
    def change_sprite(self, sprite_texture):
        self.sprite.texture = sprite_texture

    def update(self, delta_time):
        # decrement the growth timer
        self.growth_timer -= delta_time
        if self.growth_timer > 0:
            return

        # timer expired — resolve stage transition
        if self.grown:
            # final stage cycle (fruit/seeds later)
            self.growth_timer = self.data["stage"][self.current_stage]["time"]
            return

        # advance to next stage
        self.current_stage += 1
        stage_data = self.data["stage"][self.current_stage]

        self.change_sprite(stage_data["sprite"])
        self.growth_timer = stage_data["time"]

    