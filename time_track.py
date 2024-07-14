from datetime import datetime, timedelta
from clock import get_local_time

class TimeTracker:
    def __init__(self, location):
        self.location = location
        self.start_time = None
        self.pause_time = None
        self.total_time = timedelta(0)
        self.is_running = False

    def _get_current_time(self):
        local_time, _, _, _, _ = get_local_time(self.location)
        return local_time

    def _time_difference(self, start, end):
        fmt = '%H:%M:%S'
        tdelta = datetime.strptime(end, fmt) - datetime.strptime(start, fmt)
        return timedelta(hours=tdelta.seconds//3600, minutes=(tdelta.seconds//60)%60, seconds=tdelta.seconds%60)

    def start_track(self):
        if not self.is_running:
            self.start_time = self._get_current_time()
            self.is_running = True
            print(f"Tracking started at {self.start_time}")

    def pause_track(self):
        if self.is_running:
            self.pause_time = self._get_current_time()
            self.total_time += self._time_difference(self.start_time, self.pause_time)
            self.is_running = False
            print(f"Tracking paused at {self.pause_time}")

    def resume_track(self):
        if not self.is_running and self.pause_time:
            self.start_time = self._get_current_time()
            self.is_running = True
            print(f"Tracking resumed at {self.start_time}")

    def stop_track(self):
        if self.is_running:
            stop_time = self._get_current_time()
            self.total_time += self._time_difference(self.start_time, stop_time)
            self.is_running = False
            print(f"Tracking stopped at {stop_time}")
        print(f"Total tracked time: {self.total_time}")

    def get_current_time(self):
        return get_local_time(self.location)[0]

    def get_tracked_time(self):
        if self.is_running:
            current_time = self._get_current_time()
            current_tracked_time = self.total_time + self._time_difference(self.start_time, current_time)
            return current_tracked_time
        else:
            return self.total_time


