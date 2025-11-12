import arcade
from main_menu import MainMenuView
from world_map1 import WorldMap1View

MAP_SIZE = 100
SCALE = 200

WINDOW_TITLE = "NECROMANCER"

class GameView(arcade.Window): 
    def __init__(self):
        super().__init__(fullscreen=True, title=WINDOW_TITLE)
        self.background_color = arcade.csscolor.WHITE         
        self.player = None   
        self.main_menu = MainMenuView(self)
        self.world_map_1 = WorldMap1View(self, MAP_SIZE, SCALE)
        self.show_view(self.main_menu)
          

    def on_key_press(self, symbol, modifiers): 
        if symbol == arcade.key.F9:
            self.close()

    def get_screen_dimensions(self):
        return self.get_size()  # (width, height)

