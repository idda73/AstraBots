import threading
import time
import random

GRID_POSITIONS = {
    "Shelf 1": (100, 100),
    "Shelf 2": (300, 100),
    "Shelf 3": (200, 250)
}

HOME_POSITIONS = {
    "Robot A": (50, 350),
    "Robot B": (350, 350)
}

class Robot:
    def __init__(self, name):
        self.name = name
        self.status = "Idle"
        self.current_task = None
        self.x, self.y = HOME_POSITIONS[name]

class SimulationEngine:
    def __init__(self):
        self.lock = threading.Lock()
        self.reset()

    def reset(self):
        self.robots = {
            "Robot A": Robot("Robot A"),
            "Robot B": Robot("Robot B")
        }
        self.tasks = ["Shelf 1", "Shelf 2", "Shelf 3"]
        self.logs = []
        self.running = False
        self.conflicts = 0
        self.completed_tasks = 0
        self.start_time = None

    def start(self):
        with self.lock:
            if self.running:
                return
            self.running = True
            self.start_time = time.time()

        thread = threading.Thread(target=self.run_simulation)
        thread.start()

    def move_robot(self, robot, target_x, target_y):
        steps = 20
        dx = (target_x - robot.x) / steps
        dy = (target_y - robot.y) / steps

        for _ in range(steps):
            with self.lock:
                robot.x += dx
                robot.y += dy
            time.sleep(0.05)

    def run_simulation(self):
        for task in self.tasks:
            target_x, target_y = GRID_POSITIONS[task]

            with self.lock:
                r1 = self.robots["Robot A"]
                r2 = self.robots["Robot B"]
                r1.status = "Moving"
                r2.status = "Moving"
                r1.current_task = task
                r2.current_task = task
                self.logs.append(f"Both robots moving to {task}")

            self.move_robot(r1, target_x, target_y)
            self.move_robot(r2, target_x, target_y)

            with self.lock:
                r1.status = "Working"
                r2.status = "Working"
                self.logs.append(f"Both robots working on {task}")

                if random.choice([True, False]):
                    self.conflicts += 1
                    self.logs.append("Conflict detected")
                    r2.status = "Reassigned"
                    r2.current_task = None
                    self.logs.append("Robot B reassigned")

                self.completed_tasks += 1

            time.sleep(1)

        with self.lock:
            for name, r in self.robots.items():
                r.status = "Idle"
                r.current_task = None
                r.x, r.y = HOME_POSITIONS[name]

            self.logs.append("Simulation complete")
            self.running = False

    def get_state(self):
        with self.lock:
            elapsed = 0
            if self.start_time:
                elapsed = round(time.time() - self.start_time, 2)

            efficiency = 0
            if self.completed_tasks > 0:
                efficiency = round(
                    (self.completed_tasks - self.conflicts) / self.completed_tasks * 100,
                    2
                )

            return {
                "robots": {
                    name: {
                        "status": r.status,
                        "task": r.current_task,
                        "x": r.x,
                        "y": r.y
                    }
                    for name, r in self.robots.items()
                },
                "logs": self.logs[-12:],
                "metrics": {
                    "conflicts": self.conflicts,
                    "completed_tasks": self.completed_tasks,
                    "efficiency": efficiency,
                    "runtime": elapsed
                },
                "running": self.running
            }
