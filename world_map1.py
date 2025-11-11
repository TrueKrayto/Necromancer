import arcade

class WorldMap1View(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()

    def on_show_view(self):        
        self.background_color = arcade.csscolor.WHITE