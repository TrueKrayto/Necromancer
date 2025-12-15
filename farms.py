import arcade
from building_panels import BuildingPanel as BP

class FarmInterface(BP):
    def __init__(self, view, building, ui_manager):
        super().__init__(view, building, ui_manager)

    def build_content(self):
        return super().build_content()