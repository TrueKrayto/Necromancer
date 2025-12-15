import arcade
import arcade.gui

class WorldUI:
    def __init__(self, view):
        self.view = view
        
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.active_panel = None

    def enable(self):
        self.manager.enable()

    def disable(self):
        self.manager.disable()

    def open_panel(self, panel):       
        self.close_panel()        
        self.active_panel = panel

    def close_panel(self):        
        if self.active_panel:
            self.active_panel.destroy()
            self.active_panel = None

    def has_active_panel(self):
        return self.active_panel is not None
    
    def click_is_on_panel(self, x, y):
        if not self.active_panel:
            return False
        return self.active_panel.contains_point(x, y)
