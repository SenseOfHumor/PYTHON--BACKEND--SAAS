import time

class TimeTracker:
    def __init__(self):
        self.start_time = None
        self.pause_time = None
        self.total_tracked_seconds = 0
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
            print(f"Tracking started at {self.get_current_time()} (Elapsed: 00:00:00)")
        else:
            print("Tracking is already running.")

    def pause(self):
        if self.is_running:
            self.pause_time = time.time()
            self.total_tracked_seconds += self.pause_time - self.start_time
            self.is_running = False
            print(f"Tracking paused at {self.get_current_time()} (Elapsed: {self.get_total_time()})")
        else:
            print("Tracking is not running.")

    def resume(self):
        if not self.is_running and self.pause_time is not None:
            self.start_time = time.time()
            self.is_running = True
            print(f"Tracking resumed at {self.get_current_time()} (Elapsed: {self.get_total_time()})")
        else:
            print("Tracking is already running or has not been paused.")

    def stop(self):
        if self.is_running:
            stop_time = time.time()
            self.total_tracked_seconds += stop_time - self.start_time
            self.is_running = False
            self.start_time = None
            self.pause_time = None
            total_time = self.format_seconds(self.total_tracked_seconds)
            print(f"Tracking stopped at {self.get_current_time()} (Total time: {total_time})")
            self.total_tracked_seconds = 0  # Reset total tracked time
        else:
            print("Tracking is not running.")

    def get_total_time(self):
        if self.is_running:
            current_time = time.time()
            total_seconds = self.total_tracked_seconds + (current_time - self.start_time)
        else:
            total_seconds = self.total_tracked_seconds
        return self.format_seconds(total_seconds)

    def get_current_time(self):
        return time.strftime("%H:%M:%S", time.localtime())

    @staticmethod
    def format_seconds(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h:02}:{m:02}:{s:02}"

# Example usage
if __name__ == "__main__":
    tracker = TimeTracker()

    while True:
        print("\nOptions:")
        print("1. Start tracking")
        print("2. Pause tracking")
        print("3. Resume tracking")
        print("4. Stop tracking")
        print("5. Get total tracked time")
        print("6. Exit")
        
        choice = input("Choose an option: ")

        if choice == "1":
            tracker.start()
        elif choice == "2":
            tracker.pause()
        elif choice == "3":
            tracker.resume()
        elif choice == "4":
            tracker.stop()
        elif choice == "5":
            print(f"Total tracked time: {tracker.get_total_time()}")
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")
