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

def delete(id: int):
    tasks = load_data()

    index_to_remove = None
    for index, task in enumerate(tasks):
        if task["id"] == id:
            index_to_remove = index
    
    if index_to_remove == None:
        print("There is no such task with given id.")
        return 
    
    tasks.pop(index_to_remove)

    post_data(tasks)

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

def mark_done(id: int):
    tasks = load_data()

    task_to_mark = None
    for task in tasks:
        if task["id"] == id:
            task_to_mark = task
    
    if not task_to_mark:
        print("There is no such task with given id.")
        return 

    task_to_mark["status"] = "done"

    post_data(tasks)

def mark_in_progress():
    tasks = load_data()

    task_to_mark = None
    for task in tasks:
        if task["id"] == id:
            task_to_mark = task
    
    if not task_to_mark:
        print("There is no such task with given id.")
        return 

    task_to_mark["status"] = "in-progress"

    post_data(tasks)



if __name__ == "__main__":
    args = sys.argv[1:]

    if(args[0] == "add"):
        if len(args) != 2:
            print("Invalid command usage.\nCorrect usage: task add <task_description>")

        new_task_description = args[1]
        add(new_task_description)

    elif(args[0] == "update"):
        if len(args) != 3:
            print("Invalid command usage.\nCorrect usage: task update <id> <new_task_description>")
        try:
            id = int(args[1])
            new_task_description = args[2]
        except ValueError:
            print("id has to be an integer")

        update(id, new_task_description)

    elif(args[0] == "delete"):
        if len(args) != 2:
            print("Invalid command usage.\nCorrect usage: task delete <id>")
        
        try:
            id = int(args[1])
        except ValueError:
            print("id has to be an integer")

        delete(id)

    elif(args[0] == "list"):
        list()

    elif(args[0] == "mark-done"):
        if len(args) != 2:
            print("Invalid command usage.\nCorrect usage: task mark-done <id>")

        try:
            id = int(args[1])
        except ValueError:
            print("id has to be an integer")

        mark_done(id)

    elif(args[0] == "mark-in-progress"):
        if len(args) != 2:
            print("Invalid command usage.\nCorrect usage: task mark-in-progress <id>")

        try:
            id = int(args[1])
        except ValueError:
            print("id has to be an integer")

        mark_in_progress()
    else:
        print("temporary")