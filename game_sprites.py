import arcade

PLAYER_SPRITES = {
        "idle_1":"assets/sprites/player_idle_2.png"
                  }

TILE_TEXTURES = {
    "grass": arcade.load_texture("assets/map_tiles/grass_tile.png"),
    "water": arcade.load_texture("assets/map_tiles/water_tile.png"),
    "black stone": arcade.load_texture("assets/map_tiles/black_stone_tile.png"),
    "dirt path": arcade.load_texture("assets/map_tiles/dirt_path.png"),
    "stone path": arcade.load_texture("assets/map_tiles/stone_path.png"),
    "tilled earth": arcade.load_texture("assets/map_tiles/tilled_earth_01.png")
                }

BUILDING_TEXTURES = {
    "house 1": arcade.load_texture("assets/buildings/house_1.png"),
    "house 2": arcade.load_texture("assets/buildings/house_2.png"),
    "shop": arcade.load_texture("assets/buildings/shop.png"),
    "inn": arcade.load_texture("assets/buildings/inn.png"),
    "barn": arcade.load_texture("assets/buildings/barn.png"),
    "well": arcade.load_texture("assets/buildings/well.png"),
    "warehouse": arcade.load_texture("assets/buildings/warehouse.png"),
    "stall": arcade.load_texture("assets/buildings/stall.png"),
}

character_textures = {
    "elf man" : arcade.load_texture("assets/sprites/elf_man_1.png"),
    "elf woman" : arcade.load_texture("assets/sprites/elf_woman_1.png"),
    "skeleton" : arcade.load_texture("assets/sprites/skeleton_1.png")
}