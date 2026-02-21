# utils/progress.py

import time
import sys


class ProgressBar:

    def __init__(self, total_tasks):
        self.total_tasks = total_tasks
        self.completed_tasks = 0
        self.start_time = time.time()
        self.current_stage = ""
        self.last_update_time = time.time()

    def set_stage(self, stage_name):
        self.current_stage = stage_name
        self.last_update_time = time.time()

    def update(self, completed_increment=1):
        self.completed_tasks += completed_increment
        self.last_update_time = time.time()
        self.render()

    def render(self):
        percent = (self.completed_tasks / self.total_tasks) * 100
        bar_length = 30
        filled_length = int(bar_length * self.completed_tasks // self.total_tasks)

        bar = "#" * filled_length + "-" * (bar_length - filled_length)

        elapsed = time.time() - self.start_time

        if self.completed_tasks > 0:
            avg_time_per_task = elapsed / self.completed_tasks
            remaining_tasks = self.total_tasks - self.completed_tasks
            eta = avg_time_per_task * remaining_tasks
        else:
            eta = 0

        sys.stdout.write(
            f"\r[{bar}] {percent:.0f}% | "
            f"{int(elapsed)}s elapsed | "
            f"ETA {int(eta)}s | "
            f"{self.current_stage}   "
        )
        sys.stdout.flush()

    def finish(self):
        self.completed_tasks = self.total_tasks
        self.render()
        print("\nExecution completed.")