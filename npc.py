import arcade
import heapq
import math
import random
from game_config import GAME_STATE
from game_sprites import character_textures

class NPC:
    def __init__(self, name, x, y, view):
        self.view = view
        self.spawn_tile = self.view.map_manager.get_tile_at(x, y)
        self.texture = character_textures.get(name)
        if self.texture is None:
            raise NameError(f"Invalid NPC '{name}'")

        self.sprite = arcade.Sprite(self.texture, center_x=x, center_y=y)

        base_scale = GAME_STATE["SCALE"] / self.texture.width
        self.sprite.scale = base_scale
        self.base_scale = base_scale

        self.target = None
        self.path = []

        self.idle_mode = True
        self.speed = 200 + random.randint(-20, 20)

    def get_sprite(self):
        return self.sprite

    def get_position(self):
        return self.sprite.center_x, self.sprite.center_y

    def set_target(self, x, y):
        self.target = (x, y)

    def _at_position(self, x, y, threshold=2):
        cx, cy = self.get_position()
        return abs(cx - x) < threshold and abs(cy - y) < threshold

    # ----------------------------------------------------------
    # IDLE WANDERING
    # ----------------------------------------------------------
    def idle(self):
        tiles = self.view.map_manager.get_neighbours(self.spawn_tile, 10, flat=True)

        passable = [t for t in tiles if t.passable]

        if self.target is None and passable:
            target_tile = random.choice(passable)
            x, y = target_tile.get_center()
            self.set_target(x, y)
            self.path_to_position(x, y)

    # ----------------------------------------------------------
    # MAIN UPDATE LOOP
    # ----------------------------------------------------------
    def update(self, delta_time):
        # If idle and not moving, pick a new location
        if self.target is None and self.idle_mode:
            self.idle()
            return

        if not self.path:
            return

        target_x, target_y = self.path[0]
        cx, cy = self.get_position()

        if self._at_position(target_x, target_y):
            self.path.pop(0)
            if not self.path:
                self.target = None
                return
            else:
                target_x, target_y = self.path[0]

        # Movement
        dx = target_x - cx
        dy = target_y - cy

        # Flip sprite direction
        if dx < 0:
            self.sprite.scale_x = -abs(self.base_scale)
        else:
            self.sprite.scale_x = abs(self.base_scale)

        dist = math.hypot(dx, dy)
        if dist == 0:
            return

        nx = dx / dist
        ny = dy / dist

        move_amount = self.speed * delta_time
        mx = nx * move_amount
        my = ny * move_amount

        # Clamp movement
        if abs(mx) > abs(dx):
            mx = dx
        if abs(my) > abs(dy):
            my = dy

        self.sprite.center_x += mx
        self.sprite.center_y += my

    # ----------------------------------------------------------
    # SAFE NEIGHBOR CHECK
    # ----------------------------------------------------------
    def _get_walkable_neighbors(self, row, col):
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        neighbors = []

        max_row = len(self.view.map.tile_map) - 1
        max_col = len(self.view.map.tile_map[0]) - 1

        for dr, dc in directions:
            nr = row + dr
            nc = col + dc

            # SAFETY: prevent out-of-bounds BEFORE calling get_tile_at_index
            if nr < 0 or nr > max_row:
                continue
            if nc < 0 or nc > max_col:
                continue

            tile = self.view.map_manager.get_tile_at_index(nr, nc)
            if not tile or not tile.passable:
                continue

            # Diagonal corner-cut prevention
            if dr != 0 and dc != 0:
                side1 = self.view.map_manager.get_tile_at_index(row, col + dc)
                side2 = self.view.map_manager.get_tile_at_index(row + dr, col)
                if not (side1 and side1.passable and side2 and side2.passable):
                    continue

            neighbors.append((nr, nc))

        return neighbors

    # ----------------------------------------------------------
    # HEURISTIC (OCTILE DISTANCE)
    # ----------------------------------------------------------
    def _heuristic(self, a, b):
        dx = abs(a[1] - b[1])
        dy = abs(a[0] - b[0])
        return (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)

    # ----------------------------------------------------------
    # A* PATHFINDING
    # ----------------------------------------------------------
    def _a_star(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}

        while open_set:
            current_priority, current = heapq.heappop(open_set)

            if current == goal:
                return came_from

            row, col = current
            neighbors = self._get_walkable_neighbors(row, col)

            for neighbor in neighbors:
                dr = neighbor[0] - row
                dc = neighbor[1] - col
                move_cost = math.sqrt(2) if (dr != 0 and dc != 0) else 1

                tentative_g = g_score[current] + move_cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g

                    f = tentative_g + self._heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))

        return None

    # ----------------------------------------------------------
    # RECONSTRUCT PATH
    # ----------------------------------------------------------
    def _reconstruct_path(self, came_from, start, goal):
        path = [goal]
        current = goal

        while current != start:
            current = came_from[current]
            path.append(current)

        path.reverse()
        return path

    # ----------------------------------------------------------
    # PUBLIC API: PATH TO PIXEL POSITION
    # ----------------------------------------------------------
    def path_to_position(self, x, y):
        self.path = []

        npc_x, npc_y = self.get_position()
        start_tile = self.view.map_manager.get_tile_at(npc_x, npc_y)
        goal_tile = self.view.map_manager.get_tile_at(x, y)

        if start_tile is None or goal_tile is None:
            return
        if not goal_tile.passable:
            return

        self.start_index = start_tile.get_index()
        self.goal_index = goal_tile.get_index()

        came_from = self._a_star(self.start_index, self.goal_index)
        if came_from is None:          
            self.path = None
            return

        tile_path = self._reconstruct_path(came_from, self.start_index, self.goal_index)

        pixel_path = []
        for row, col in tile_path:
            tile = self.view.map_manager.get_tile_at_index(row, col)
            if tile:
                px, py = tile.get_center()
                pixel_path.append((px, py))

        self.path = pixel_path
