from npc import NPC
from crops import Seed

class Villager(NPC):
    def __init__(self, name, x, y, map, village):
        super().__init__(name, x, y, map)
        self.village = village
        self.valid_jobs = ["farmer", "shopkeeper", "innkeeper"]
        self.job = None
        self.current_task = None
        self.target_tile = None
        self.inventory = []

        # --- Task timing / animation pause ---
        self.performing_task = False
        self.task_timer = 0
        self.task_durations = {"planting": 2.5, "watering":1} # seconds spent doing a farm task

    def assign_job(self, job):
        if job in self.valid_jobs:
            self.job = job
            self.idle_mode = False

    def update(self, delta_time):
        if self.job == "farmer":
            self.farming_update(delta_time)
        else:
            super().update(delta_time)

    # -----------------------------------------------------------------------
    #   FARMER LOGIC
    # -----------------------------------------------------------------------

    def farming_update(self, delta_time):

        # --- If currently performing a task, remain paused until timer expires ---
        if self.performing_task:
            self.task_timer -= delta_time
            if self.task_timer <= 0:
                self.finish_farm_task()
            return

        # --- No active task: try to find one ---
        if not self.current_task:
            found_task = self.find_farm_task()

            # No farm tasks -> idle
            if not found_task:
                self.idle_mode = True
                super().update(delta_time)  # wander
                return

            # Task found -> stop idle wandering
            self.idle_mode = False
            return

        # --- Move toward the assigned task tile ---
        super().update(delta_time)

        # When we reach the tile: begin the timed task animation
        if self.target and self._at_position(*self.target):
            self.perform_farm_task()

    def find_farm_task(self):       
        # --- 1) PLANTING task ---
        for tile in self.village.farm_tiles:
            farm = tile.component
            if not farm.planted and not farm.assigned:
                x, y = tile.get_center()
                self.set_target(x, y)
                self.path_to_position(x, y)
                self.current_task = "planting"                
                self.target_tile = tile
                farm.toggle_assigned()
                self.idle_mode = False
                return True

        # --- 2) WATERING task ---
        for tile in self.village.farm_tiles:
            farm = tile.component
            if farm.planted and not farm.crop.watered and not farm.assigned:
                x, y = tile.get_center()
                self.set_target(x, y)
                self.path_to_position(x, y)
                self.current_task = "watering"                
                self.target_tile = tile
                farm.toggle_assigned()
                self.idle_mode = False
                return True

        # --- No tasks found ---
        return False

    # -----------------------------------------------------------------------
    #   TASK TIMING SYSTEM
    # -----------------------------------------------------------------------

    def perform_farm_task(self):
        """Begin a timed farm task pause."""
        self.target = None
        self.performing_task = True
        self.task_timer = self.task_durations.get(self.current_task, 1.0)  # begin countdown

    def finish_farm_task(self):
        """Finish the farm task after the delay finishes."""
        farm = self.target_tile.component

        if self.current_task == "planting":
            item = Seed("cabbage")  # later pull seeds from storage
            farm.interact(item, self)
            farm.toggle_assigned()

        elif self.current_task == "watering":
            farm.crop.water()
            farm.toggle_assigned()

        # Reset task state
        self.current_task = None
        self.target_tile = None
        self.performing_task = False
