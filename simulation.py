import random
import asyncio
import time

GRID_SIZE = 8
NUM_ROBOTS = 5

class Robot:
    def __init__(self, robot_id):
        self.id = robot_id
        self.x = random.randint(0, GRID_SIZE - 1)
        self.y = random.randint(0, GRID_SIZE - 1)
        self.status = "IDLE"
        self.task = None
        self.completed_tasks = 0

class Simulation:
    def __init__(self):
        self.robots = [Robot(i) for i in range(NUM_ROBOTS)]
        self.logs = []
        self.running = False
        self.conflicts = 0
        self.start_time = None

    def reset(self):
        self.__init__()

    async def run(self):
        if self.running:
            return

        self.running = True
        self.start_time = time.time()
        self.logs.append("Simulation started.")

        for robot in self.robots:
            await self.assign_task(robot)
            await asyncio.sleep(0.5)

        self.logs.append("Simulation complete.")
        self.running = False

    async def assign_task(self, robot):
        target_x = random.randint(0, GRID_SIZE - 1)
        target_y = random.randint(0, GRID_SIZE - 1)

        robot.status = "WORKING"
        robot.task = f"Shelf ({target_x},{target_y})"
        self.logs.append(f"Robot {robot.id} assigned to {robot.task}")

        while robot.x != target_x or robot.y != target_y:
            await asyncio.sleep(0.2)

            if robot.x < target_x:
                robot.x += 1
            elif robot.x > target_x:
                robot.x -= 1

            if robot.y < target_y:
                robot.y += 1
            elif robot.y > target_y:
                robot.y -= 1

            if self.detect_conflict(robot):
                self.conflicts += 1
                self.logs.append(f"Conflict detected for Robot {robot.id}, re-routing.")
                break

        robot.completed_tasks += 1
        robot.status = "IDLE"
        robot.task = None
        self.logs.append(f"Robot {robot.id} completed task.")

    def detect_conflict(self, current_robot):
        for robot in self.robots:
            if robot.id != current_robot.id:
                if robot.x == current_robot.x and robot.y == current_robot.y:
                    return True
        return False

    def get_state(self):
        duration = time.time() - self.start_time if self.start_time else 0
        total_completed = sum(r.completed_tasks for r in self.robots)

        efficiency = 100
        if total_completed > 0:
            efficiency = round(
                ((total_completed - self.conflicts) / total_completed) * 100,
                2
            )

        return {
            "robots": [
                {
                    "id": r.id,
                    "x": r.x,
                    "y": r.y,
                    "status": r.status,
                    "task": r.task,
                    "completed": r.completed_tasks
                }
                for r in self.robots
            ],
            "logs": self.logs[-20:],
            "metrics": {
                "conflicts": self.conflicts,
                "duration": round(duration, 2),
                "total_completed": total_completed,
                "efficiency": efficiency
            }
        }

simulation = Simulation()
