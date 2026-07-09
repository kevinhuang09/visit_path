from math import dist
from worker import Worker
import config

class Simulation:
    def __init__(self):
        self.file_path = config.COORDINATES_FILE
        self.walk_speed = config.WALK_SPEED
        self.points = []
        self.workers = []
        self.current_time = 0

    def load_coordinates(self):
        try:
            with open(self.file_path, 'r', encoding = "utf-8") as f:
                for line in f:
                    x, y = list(map(int, line.split(" ")))
                    self.points.append((x, y))
            print(f"success read {len(self.points)} visit {'points' if len(self.points) > 1 else 'point'}")
        except: 
            print(f"no found {self.file_path}")

    def add_worker(self, name, start_pos = config.START_POSITION):
        self.workers.append(Worker(name, start_pos))

    def _assign_tasks(self):
        for worker in self.workers:
            if worker.is_idle():
                if not self.points:
                    break
                # sort the distance with worker
                # select minimum distnace worker
                self.points.sort(key = lambda p : dist(worker.pos, p))
                best_point = self.points.pop(0)

                # count time
                distance = dist(worker.pos, best_point)
                travel_time = round(distance * self.walk_speed)

                # assign task
                worker.set_task(best_point, self.current_time, travel_time)

    def run(self):
        print("Start simulation")

        while self.points or any(not w.is_idle() for w in self.workers):
            # update all worker status
            for worker in self.workers:
                worker.update_status(self.current_time)
            
            # assign new task
            self._assign_tasks()
            self.current_time += 1
        self._print_summary()

    def _print_summary(self):
        print("=" * 20)
        print(f"total use time : {self.current_time - 1}")
        print("=" * 20)
        for worker in self.workers:
            print(f"the path of {worker.name} : {worker.path}")
            