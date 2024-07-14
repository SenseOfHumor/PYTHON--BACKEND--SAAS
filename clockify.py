import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

class ClockifyTracker:
    def __init__(self):
        self.api_key = os.getenv("CLOCKIFY_API_KEY")
        self.base_url = "https://api.clockify.me/api/v1"
        self.headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        self.workspace_id = self._get_workspace_id()
        self.user_id = self._get_user_id()
        self.current_timer_id = None

    def _get_workspace_id(self):
        url = f"{self.base_url}/workspaces"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            workspaces = response.json()
            if workspaces:
                return workspaces[0]["id"]
            else:
                raise Exception("No workspaces found")
        else:
            self._log_error(response)
            raise Exception("Failed to fetch workspaces")

    def _get_user_id(self):
        url = f"{self.base_url}/user"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            user = response.json()
            return user["id"]
        else:
            self._log_error(response)
            raise Exception("Failed to fetch user information")

    def _log_error(self, response):
        print(f"Error: {response.status_code} - {response.text}")

    def get_projects(self):
        url = f"{self.base_url}/workspaces/{self.workspace_id}/projects"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            projects = response.json()
            for project in projects:
                print(f"Project ID: {project['id']}, Name: {project['name']}")
            return projects
        else:
            self._log_error(response)
            return []

    def create_project(self, project_name="Default Project"):
        url = f"{self.base_url}/workspaces/{self.workspace_id}/projects"
        data = {
            "name": project_name,
            "isPublic": False
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            project = response.json()
            print(f"Created project '{project_name}' with ID: {project['id']}")
            return project['id']
        else:
            self._log_error(response)
            raise Exception("Failed to create project")

    def start_track(self, description="Working", project_id=None):
        if not project_id:
            projects = self.get_projects()
            if not projects:
                project_id = self.create_project()
            else:
                project_id = projects[0]['id']
                
        url = f"{self.base_url}/workspaces/{self.workspace_id}/time-entries"
        data = {
            "start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "description": description,
            "billable": True,
            "projectId": project_id,
            "taskId": None,
            "tagIds": [],
            "userId": self.user_id
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            self.current_timer_id = response.json()["id"]
            print(f"Tracking started at {data['start']}")
        else:
            self._log_error(response)

    def stop_track(self):
        if self.current_timer_id:
            url = f"{self.base_url}/workspaces/{self.workspace_id}/time-entries/{self.current_timer_id}"
            data = {
                "end": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            response = requests.put(url, headers=self.headers, json=data)
            if response.status_code == 200:
                print(f"Tracking stopped at {data['end']}")
                self.current_timer_id = None
            else:
                self._log_error(response)
        else:
            print("No active timer to stop")

    def get_current_time(self):
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def get_tracked_time(self):
        url = f"{self.base_url}/workspaces/{self.workspace_id}/user/{self.user_id}/time-entries"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            time_entries = response.json()
            total_seconds = 0
            for entry in time_entries:
                start = time.strptime(entry["timeInterval"]["start"], "%Y-%m-%dT%H:%M:%SZ")
                if "end" in entry["timeInterval"]:
                    end = time.strptime(entry["timeInterval"]["end"], "%Y-%m-%dT%H:%M:%SZ")
                else:
                    end = time.gmtime()  # Ongoing entry
                total_seconds += time.mktime(end) - time.mktime(start)
            return self._seconds_to_time(int(total_seconds))
        else:
            self._log_error(response)
            return "00:00:00"

    def _seconds_to_time(self, seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f'{h:02}:{m:02}:{s:02}'

# Example usage
if __name__ == "__main__":
    tracker = ClockifyTracker()
    projects = tracker.get_projects()
    if projects:
        project_id = projects[0]['id']
    else:
        project_id = tracker.create_project()

    tracker.start_track("Working on project", project_id)
    time.sleep(5)  # Simulate some time passing
    tracker.stop_track()

    current_time = tracker.get_current_time()
    print(f"Current UTC time: {current_time}")
    tracked_time = tracker.get_tracked_time()
    print(f"Total tracked time: {tracked_time}")
