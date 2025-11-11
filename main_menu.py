import arcade

class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()

    def on_show_view(self):
        self.background_color = arcade.csscolor.BLACK  

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:           
            self.window.show_view(self.window.world_map_1)