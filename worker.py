from math import dist
from config import VISIT_TIME

class Worker:
    def __init__(self, name, start_pos = (0, 0)):
        self.name = name
        self.pos = start_pos
        self.path = [start_pos]
        self.status = "idle"
        self.target_point = None
        self.next_free_time = 0

    def is_idle(self):
        return self.status == "idle"
    
    def set_task(self, target, current_time, travel_time):
        self.target_point = target
        self.path.append(target)

        if travel_time == 0:
            self.status = "visiting"
            self.next_free_time = current_time + VISIT_TIME
            print(f"time : {current_time} {self.name} start visit {target}")
        else:
            self.status = "walking"
            self.next_free_time = current_time + travel_time
            print(f"time : {current_time}, {self.name} will go to {target}, need {travel_time} {'minutes' if travel_time != 1 else 'minute'}")

    def update_status(self, current_time):
        if self.status != "idle" and current_time == self.next_free_time:
            if self.status == "walking":
                self.status = "visiting"
                self.pos = self.target_point
                self.next_free_time = current_time + VISIT_TIME
                print(f"time : {current_time}, {self.name} arrival {self.pos}, start visit {VISIT_TIME} {VISIT_TIME} {'minutes' if VISIT_TIME != 1 else 'minute'}")
            elif self.status == "visiting":
                print(f"time : {current_time}, {self.name} complete visit point {self.target_point}")
                self.status = "idle"
                self.target_point = None