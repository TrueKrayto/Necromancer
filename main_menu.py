import arcade
import arcade.gui

class MainMenuView(arcade.View):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.manager = arcade.gui.UIManager()
        new_game_button = arcade.gui.UIFlatButton(text="New Game", width=200)
        @new_game_button.event("on_click")
        def start_new_game(event):
            self.game.player = None
            self.window.show_view(self.window.world_map_1)

        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child= new_game_button
        )
        

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_show_view(self):
        self.background_color = arcade.csscolor.BLACK
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:           
            self.window.show_view(self.window.world_map_1)

    