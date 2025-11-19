import arcade
import arcade.gui

class PauseMenu:
    def __init__(self, game, current_view):
        self.view = current_view
        self.game = game
        self.main_menu = self.game.get_main_menu_view()

        self.manager = arcade.gui.UIManager()

        # This is the full-screen root container
        self.anchor = self.manager.add(
            arcade.gui.UIAnchorLayout(size_hint=(1, 1))
        )

    def pause_frame(self):
        """Construct the actual pause menu window (panel + layout)."""

        pause_menu = self

        # Create the panel (a UIAnchorLayout with fixed width/height)
        self.frame = arcade.gui.UIAnchorLayout(
            width=800,
            height=900,
            size_hint=None
        )

        # Add padding inside the panel
        self.frame.with_padding(all=20)

        # Add the background 9-patch texture
        self.frame.with_background(
            texture=arcade.gui.NinePatchTexture(
                left=7,
                right=7,
                bottom=7,
                top=7,
                texture=arcade.load_texture(
                    "assets/sprites/pause_menu_texture.png"
                ),
            )
        )

        self.box = arcade.gui.UIBoxLayout(
            align="center",
            space_between=30
        )

        spacer = arcade.gui.UIWidget(width=0, height=30)
        self.box.add(spacer)

        title = arcade.gui.UILabel(
            text="PAUSED",
            font_size=60,
            text_color=arcade.color.GHOST_WHITE
        )

        self.box.add(title)

        self.frame.add(
            child=self.box,
            anchor_x="center_x",
            anchor_y="center_y"
        )

        # ---------------------------
        # Add the panel to the center
        # ---------------------------
        self.anchor.add(
            child=self.frame,
            anchor_x="center_x",
            anchor_y="center_y",
        )

        # buttons
        main_menu_button = arcade.gui.UIFlatButton(text="Main Menu", width=200)
        @main_menu_button.event("on_click")
        def return_to_main_menu(event):
            pause_menu.game.change_view(pause_menu.main_menu)
            pause_menu.view.clear_all()
            pause_menu.view.toggle_pause()

        options_button = arcade.gui.UIFlatButton(text="Options", width=200)

        return_button = arcade.gui.UIFlatButton(text="Return", width=200)
        @return_button.event("on_click")
        def unpause(event):
            pause_menu.view.toggle_pause()

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        @quit_button.event("on_click")
        def quit_game(event):   
            pause_menu.game.close()

        spacer_2 = arcade.gui.UIWidget(width=0, height=75)
        self.box.add(spacer_2)

        self.box.add(main_menu_button)
        self.box.add(options_button)
        self.box.add(return_button)
        self.box.add(spacer)
        self.box.add(quit_button)

        