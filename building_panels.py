import arcade
import arcade.gui

# NOTE:
# Panels are currently non-draggable.
# Arcade 3.3.x layouts do not support reliable draggable widgets.
# Revisit when upgrading Arcade or UI system.

class BuildingPanel:
    PANEL_WIDTH = 700
    PANEL_HEIGHT = 800
    HEADER_HEIGHT = 50

    def __init__(self, view, building, ui_manager):
        self.view = view
        self.building = building
        self.ui_manager = ui_manager

        # Root anchor for positioning
        self.anchor = arcade.gui.UIAnchorLayout(size_hint=(1, 1))
        self.ui_manager.add(self.anchor)

        self._build_panel()

    # -------------------------------------------------
    # Panel construction
    # -------------------------------------------------
    def _build_panel(self):
        # Main panel layout (this owns size + background + children)
        self.frame = arcade.gui.UIBoxLayout(
            vertical=True,
            width=self.PANEL_WIDTH,
            height=self.PANEL_HEIGHT,
            size_hint=None
        )

        # Anchor panel to top-right
        self.anchor.add(
            self.frame,
            anchor_x="right",
            anchor_y="top",
            align_x=-100,
            align_y=-100
        )

        # Background
        self.frame.with_background(
            texture=arcade.gui.NinePatchTexture(
                left=0,
                right=0,
                bottom=0,
                top=0,
                texture=arcade.load_texture(
                    "assets/sprites/building_panel_bg.png"
                ),
            )
        )

        # Header
        spacer = arcade.gui.UIWidget(width=0, height=40)
        self.frame.add(spacer)
        self._build_header()

        # Content container (empty for now)
        self.content_container = arcade.gui.UIBoxLayout(
            vertical=True,
            width=self.PANEL_WIDTH,
            height=self.PANEL_HEIGHT - self.HEADER_HEIGHT
        )

        self.frame.add(self.content_container)

    # -------------------------------------------------
    # Header
    # -------------------------------------------------
    def _build_header(self):
        header = arcade.gui.UIBoxLayout(
            vertical=False,
            width=self.PANEL_WIDTH,
            height=self.HEADER_HEIGHT,
            size_hint= None
        )

        left_pad = arcade.gui.UIWidget(width=50)

        title = arcade.gui.UILabel(
            text=self.building.building_type.upper(),
            font_size=35,
            align="left"
        )

        spacer = arcade.gui.UIWidget(size_hint=(1, 1))

        close_button = arcade.gui.UIFlatButton(
            text="✕",
            width=36,
            height=30,           
            
        )

        right_pad = arcade.gui.UIWidget(width=50)

        @close_button.event("on_click")
        def _on_close(event):
            self.view.world_ui.close_panel()

        header.add(left_pad)
        header.add(title)
        header.add(spacer)
        header.add(close_button)
        header.add(right_pad)

        self.frame.add(header)

    # -------------------------------------------------
    # Content API
    # -------------------------------------------------
    def set_content(self, widget):
        """Replace panel content."""
        self.clear_content()
        self.content_container.add(widget)

    def clear_content(self):
        self.content_container.clear()

    # -------------------------------------------------
    # Lifecycle
    # -------------------------------------------------
    def destroy(self):
        if self.anchor:
            self.ui_manager.remove(self.anchor)
            self.anchor = None

    def contains_point(self, x, y):
        if not self.frame:
            return False

        rect = self.frame.rect
        return (
            rect.left <= x <= rect.right and
            rect.bottom <= y <= rect.top
        )
