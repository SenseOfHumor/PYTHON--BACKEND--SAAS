from time_track import TimeTracker

def main():
    location = input("Enter location (e.g., Asia/Kolkata): ")
    tracker = TimeTracker(location)
    
    while True:
        print("\nOptions:")
        print("1. Start tracking")
        print("2. Pause tracking")
        print("3. Resume tracking")
        print("4. Stop tracking")
        print("5. Get current local time")
        print("6. Get total tracked time")
        print("7. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            tracker.start_track()
        elif choice == "2":
            tracker.pause_track()
        elif choice == "3":
            tracker.resume_track()
        elif choice == "4":
            tracker.stop_track()
        elif choice == "5":
            current_time_info = tracker.get_current_time()
            print(f"Current local time: {current_time_info}")
        elif choice == "6":
            tracked_time = tracker.get_tracked_time()
            print(f"Total tracked time: {tracked_time}")
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


#TODO: test out the time tracking around midnight to see if the time is tracked properly