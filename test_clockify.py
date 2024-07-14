from clockify import ClockifyTracker

def main():
    tracker = ClockifyTracker()
    projects = tracker.get_projects()

    if projects:
        print("Available Projects:")
        for project in projects:
            print(f"Project ID: {project['id']}, Name: {project['name']}")
        project_id = input("Enter the project ID to use for tracking: ")
    else:
        print("No projects available. Creating a default project.")
        project_id = tracker.create_project()

    while True:
        print("\nOptions:")
        print("1. Start tracking")
        print("2. Stop tracking")
        print("3. Get current UTC time")
        print("4. Get total tracked time")
        print("5. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            description = input("Enter description for time entry: ")
            tracker.start_track(description, project_id)
        elif choice == "2":
            tracker.stop_track()
        elif choice == "3":
            current_time = tracker.get_current_time()
            print(f"Current UTC time: {current_time}")
        elif choice == "4":
            tracked_time = tracker.get_tracked_time()
            print(f"Total tracked time: {tracked_time}")
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
