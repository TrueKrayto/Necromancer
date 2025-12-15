"""
Docstring for Necromancer.tasks
The task classes to be created and assigned by the managers
"""

from crops import Seed

class Task:
    def __init__(self, job,  tile, actions=1, item = None, sub_task = None, priority = 0):
        self.priority  = priority
        self.required_job = job
        self.tile = tile
        self.location = self.tile.get_center()
        self.actions = actions
        self.item = item
        self.sub_task = sub_task
        self.reserved = False
        self.worker = None
        self.started = False
        self.task_completed = False

    def change_priority(self, prio):
        self.priority = prio

    def reserve_task(self, worker):
        self.reserved = True
        self.worker = worker
    
    def set_location(self, tile):
        self.location = tile.get_center()

    def at_location(self, x, y, threshold=2):        
        cx, cy = self.location
        return abs(cx - x) < threshold and abs(cy - y) < threshold
    
    def on_start(self, worker):
        self.started = True
        worker.start_working()

    def on_update(self, worker, dt):
        pass

    def on_complete(self, worker):
        worker.stop_working()

class PlantTask(Task):
    def __init__(self, job, tile, seed, actions=1, item=None, sub_task=None):
        super().__init__(job, tile, actions, item, sub_task)
        self.duration = 3
        self.seed = seed
        self.change_priority(5)

    def on_update(self, worker, dt):
        if worker.working:
            self.duration -= dt
            if self.duration <= 0:
                self.actions -= 1
                if self.actions == 0:
                    self.task_completed = True

    def on_complete(self, worker):
        farm = self.tile.component
        item = Seed(self.seed)
        farm.interact(item, worker)
        worker.stop_working()
        
class WaterTask(Task):
    def __init__(self, job, tile, actions=1, item=None, sub_task=None, priority=0):
        super().__init__(job, tile, actions, item, sub_task, priority)
        self.duration = 1.5
        self.change_priority(10)               

    def on_update(self, worker, dt):
        if worker.working:
            self.duration -= dt
            if self.duration <= 0:
                self.actions -= 1
                if self.actions == 0:
                    self.task_completed = True

    def on_complete(self, worker):
        farm = self.tile.component        
        farm.crop.water()
        worker.stop_working()

class HarvestTask(Task):
    def __init__(self, job, tile, actions=1, item=None, sub_task=None, priority=0):
        super().__init__(job, tile, actions, item, sub_task, priority)
        self.duration = 2
        self.change_priority(1)

    def on_update(self, worker, dt):
        if worker.working:
            self.duration -= dt
            if self.duration <= 0:
                self.actions -= 1
                if self.actions == 0:
                    self.task_completed = True

    def on_complete(self, worker):
        farm = self.tile.component
        farm.harvest(worker)
        worker.stop_working()

class FellTreeTask(Task):
    def __init__(self, job, tile, actions=1, item=None, sub_task=None, priority=0,):
        super().__init__(job, tile, actions, item, sub_task, priority)
        self.duration = 2
        self.action_time = 2          
        self.tree = tile.tree
        if not self.tree:
            self.task_completed = True
            return
        self.actions = self.tree.health        
        self.change_priority(-999) # <--- lowest prio for testing

    def on_update(self, worker, dt):
        if worker.working:
            self.duration -= dt
            if self.duration <= 0:
                self.actions -= 1
                self.action()
                self.duration = self.action_time
                if self.actions == 0:
                    self.task_completed = True

    def action(self):
        if self.tree and self.tree.health > 0:
            self.tree.chop()