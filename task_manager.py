import sys
import json
from pathlib import Path
from datetime import datetime

TASK_FILE = Path(__file__).parent / "tasks.json"

def load_data() -> list:
    if not TASK_FILE.exists():
        return []
    with TASK_FILE.open("r", encoding='utf-8') as file:
        return json.load(file)

def post_data(data: list):
    with TASK_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

def add(new_task_description: str):
    tasks = load_data()

    new_task = {
        "id": tasks[-1]['id'] + 1 if len(tasks) else 1,
        "description": new_task_description,
        "status": "in-progress",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }

    tasks.append(new_task)
    post_data(tasks)

def update(id: int, new_task_description: str):
    tasks = load_data()

    if not len(tasks):
        print("There are no tasks right now add one before updating.")
        return

    task_to_update = None
    for task in tasks:
        if task["id"] == id:
            task_to_update = task
    
    if not task_to_update:
        print("No task with such id.")
        return
    
    task_to_update["id"] = id
    task_to_update["description"] = new_task_description
    task_to_update["updated_at"] = datetime.now().isoformat()

    post_data(tasks)

def delete():
    print("temporary2")

def list():
    tasks = load_data()
    if not tasks:
        print("No tasks found.")
        return

    print("-" * 85)
    print(f"{'ID':<5} | {'Status':<12} | {'Description':<40} | {'Last Updated':<18}")
    print("-" * 85)
    for task in tasks:
        task_id = task.get("id", "")
        status = task.get("status", "")
        desc = task.get("description", "")
        
        # Handle both possible timestamp keys (updated_at and updatedAt)
        updated = task.get("updated_at") or task.get("updatedAt") or task.get("createdAt") or ""
        if updated:
            try:
                dt = datetime.fromisoformat(updated)
                time_str = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                time_str = str(updated)
        else:
            time_str = ""

        if len(desc) > 37:
            desc = desc[:37] + "..."
            
        print(f"{task_id:<5} | {status:<12} | {desc:<40} | {time_str:<18}")
    print("-" * 85)

def mark_done():
    print("temporary4")

def mark_in_progress():
    print("temporary5")



if __name__ == "__main__":
    args = sys.argv[1:]

    if(args[0] == "add"):
        if(len(args) != 2):
            print("Invalid command usage.\nCorrect usage: task add <task_description>")

        new_task_description = args[1]
        add(new_task_description)

    elif(args[0] == "update"):
        if(len(args) != 3):
            print("Invalid command usage.\nCorrect usage: task update <id> <new_task_description>")
        try:
            id = int(args[1])
            new_task_description = args[2]
        except ValueError:
            print("id has to be an integer")

        update(id, new_task_description)

    elif(args[0] == "delete"):
        delete()
    elif(args[0] == "list"):
        list()
    elif(args[0] == "mark-done"):
        mark_done()
    elif(args[0] == "mark-in-progress"):
        mark_in_progress()
    else:
        print("temporary")