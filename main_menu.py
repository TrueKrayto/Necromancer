import arcade
import arcade.gui

class MainMenuView(arcade.View):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.manager = arcade.gui.UIManager()
        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout(size_hint=(1,1)))
        self.frame = arcade.gui.UIAnchorLayout(
            width=800,
            height=900,
            size_hint=None
        )
        self.frame.with_padding(all=20)
        self.anchor.add(
            child=self.frame,
            anchor_x="center_x",
            anchor_y="center_y"
        )

        self.button_box = arcade.gui.UIBoxLayout(
            align="center",
            space_between=30
            )
        
        title = arcade.gui.UILabel(
            text="Necromancer",
            text_color=arcade.color.ALIZARIN_CRIMSON,
            font_size=100
        )

        new_game_button = arcade.gui.UIFlatButton(text="New Game", width=200)        
        @new_game_button.event("on_click")
        def start_new_game(event):
            self.game.player = None
            self.window.show_view(self.window.world_map_1)
        quit_button = arcade.gui.UIFlatButton(text="QUIT", width=200)
        @quit_button.event("on_click")
        def quit_game(event):
            self.game.close()

        self.button_box.add(title)
        self.button_box.add(new_game_button)
        self.button_box.add(quit_button)

        self.frame.add(
            child=self.button_box,
            anchor_x="center_x",
            anchor_y="center_y"
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

