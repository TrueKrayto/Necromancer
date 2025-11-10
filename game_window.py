import arcade

WINDOW_TITLE = "NECROMANCER"

class GameView(arcade.Window): 
    def __init__(self):
        super().__init__(fullscreen=True, title=WINDOW_TITLE)
        self.background_color = arcade.csscolor.WHITE  

    def on_draw(self):           
        self.clear() 
    
    def on_key_press(self, symbol, modifiers): 
        if symbol == arcade.key.F9:
            self.close()

