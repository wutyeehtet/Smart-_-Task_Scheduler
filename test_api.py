import requests

BASE_URL = 'http://127.0.0.1:5000'


new_task = {
    "title": "Finish Database Schema",
    "deadline": "2026-06-10",
    "priority": 5,
    "duration": 120,
    "category": "Project"
}

print("Creating a new task...")
response = requests.post(f"{BASE_URL}/tasks", json=new_task)
print(response.json())


print("\nFetching all tasks...")
response = requests.get(f"{BASE_URL}/tasks")
print(response.json())