from clock import get_local_time

class TimeTracker:
    def __init__(self, location):
        self.location = location
        self.start_time = None
        self.pause_time = None
        self.total_seconds = 0
        self.is_running = False

    def _get_current_time(self):
        local_time, _, _, _, _ = get_local_time(self.location)
        return local_time

    def _time_to_seconds(self, time_str):
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s

    def _seconds_to_time(self, seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f'{h:02}:{m:02}:{s:02}'

    def _time_difference(self, start, end):
        start_seconds = self._time_to_seconds(start)
        end_seconds = self._time_to_seconds(end)

        if end_seconds < start_seconds:  # Handle span over midnight
            end_seconds += 24 * 3600

        return end_seconds - start_seconds

    def start_track(self):
        if not self.is_running:
            self.start_time = self._get_current_time()
            self.is_running = True
            print(f"Tracking started at {self.start_time}")

    def pause_track(self):
        if self.is_running:
            self.pause_time = self._get_current_time()
            self.total_seconds += self._time_difference(self.start_time, self.pause_time)
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
            self.total_seconds += self._time_difference(self.start_time, stop_time)
            self.is_running = False
            print(f"Tracking stopped at {stop_time}")
        print(f"Total tracked time: {self._seconds_to_time(self.total_seconds)}")

    def get_current_time(self):
        return get_local_time(self.location)

    def get_tracked_time(self):
        if self.is_running:
            current_time = self._get_current_time()
            current_tracked_seconds = self.total_seconds + self._time_difference(self.start_time, current_time)
            return self._seconds_to_time(current_tracked_seconds)
        else:
            return self._seconds_to_time(self.total_seconds)


