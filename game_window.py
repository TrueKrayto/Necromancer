import arcade
from main_menu import MainMenuView
from world_map1 import WorldMap1View
from buildings import BuildingInteriorView

MAP_SIZE = 200
SCALE = 200

WINDOW_TITLE = "NECROMANCER"

class GameView(arcade.Window): 
    def __init__(self):
        super().__init__(fullscreen=True, title=WINDOW_TITLE)
        self.background_color = arcade.csscolor.WHITE         
        self.player = None   
        self.main_menu = MainMenuView(self)
        self.world_map_1 = WorldMap1View(self, MAP_SIZE, SCALE)
        self.building_interior = BuildingInteriorView(self)
        self.show_view(self.main_menu)
          

    def on_key_press(self, symbol, modifiers): 
        pass

    def get_screen_dimensions(self):
        return self.get_size()  # (width, height)
    
    def get_main_menu_view(self):
        return self.main_menu

    def change_view(self, view):
        self.show_view(view)