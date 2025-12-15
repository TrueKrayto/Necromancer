from npc import NPC
from crops import Seed

class Villager(NPC):
    def __init__(self, name, x, y, map, village):
        super().__init__(name, x, y, map)
        self.village = village
        self.manager = self.village.manager
        self.valid_jobs = ["farmer", "shopkeeper", "innkeeper"]
        self.job = None
        self.current_task = None
        self.target_tile = None
        self.inventory = []
        self.working = False        

    def start_working(self):
        self.working = True

    def stop_working(self):
        self.working = False

    def assign_manager(self, manager):
        self.manager = manager

    def assign_job(self, job):
        if job in self.valid_jobs:
            self.job = job
            self.idle_mode = False

    def update(self, delta_time):
        # NOTE:
        # Task failure / recovery logic (e.g. path failure, releasing tree/tile assignments)
        # is currently handled here in Villager.update().
        # This is temporary.
        # Long-term, tasks themselves should own:
        # - validation (is location still valid?)
        # - failure handling
        # - assignment / unassignment of tiles, trees, etc.
        # NPC logic should only execute tasks, not manage world state.
        # --------------------------------------------------
        # ABORT TASK ONLY IF PATHFINDING ACTUALLY FAILED
        # --------------------------------------------------
        if self.current_task and self.target is not None and not self.path:
            # release tree assignment if needed
            if hasattr(self.current_task, "tree") and self.current_task.tree:
                self.current_task.tree.assigned = False

            self.current_task = None
            self.target = None
            self.working = False
            self.idle_mode = True
            return

        # --------------------------------------------------
        # 1) IF NO TASK, TRY TO GET ONE
        # --------------------------------------------------
        if self.current_task is None:
            self.current_task = self.manager.choose_task(self)

        # --------------------------------------------------
        # 2) STILL NO TASK → IDLE / WANDER
        # --------------------------------------------------
        if self.current_task is None:
            self.idle_mode = True
            super().update(delta_time)
            return

        # --------------------------------------------------
        # 3) SET MOVEMENT TARGET IF NOT SET
        # --------------------------------------------------
        if self.target is None:
            tx, ty = self.current_task.location
            self.set_target(tx, ty)
            self.path_to_position(tx, ty)

        # --------------------------------------------------
        # 4) MOVE TOWARDS TASK LOCATION
        # --------------------------------------------------
        x, y = self.get_position()
        if not self.current_task.at_location(x, y):
            super().update(delta_time)
            return

        # --------------------------------------------------
        # 5) ARRIVED AT TASK LOCATION
        # --------------------------------------------------
        self.target = None

        # --------------------------------------------------
        # TASK EXECUTION
        # --------------------------------------------------

        # Start task if not started
        if not self.current_task.started:
            self.current_task.on_start(self)
            return

        # Update running task
        if not self.current_task.task_completed:
            self.current_task.on_update(self, delta_time)
            return

        # --------------------------------------------------
        # TASK COMPLETED
        # --------------------------------------------------
        self.current_task.on_complete(self)
        self.manager.complete_task(self.current_task)

        self.current_task = None
        self.working = False
        self.idle_mode = True

        # resume idle behavior immediately
        super().update(delta_time)
