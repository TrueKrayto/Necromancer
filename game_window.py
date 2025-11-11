import arcade

WINDOW_TITLE = "NECROMANCER"

class GameView(arcade.Window): 
    def __init__(self, player):
        super().__init__(fullscreen=True, title=WINDOW_TITLE)
        self.background_color = arcade.csscolor.WHITE         
        self.player = player
        self.center_player()        
        

    def on_draw(self):           
        self.clear() 
        self.player.draw()
        
    
    def on_key_press(self, symbol, modifiers): 
        if symbol == arcade.key.F9:
            self.close()

    def get_screen_dimensions(self):
        return self.get_size()  # (width, height)

    def center_player(self):        
        screen = self.get_screen_dimensions()
        self.player.sprite.center_x = screen[0] / 2
        self.player.sprite.center_y = screen[1] / 2