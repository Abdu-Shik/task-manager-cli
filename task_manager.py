import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# Configure logging to output cleanly to console
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("task_manager")

TASK_FILE = Path(__file__).parent / "tasks.json"

def load_data() -> list:
    if not TASK_FILE.exists():
        return []
    try:
        with TASK_FILE.open("r", encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []

def post_data(data: list):
    try:
        with TASK_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
    except IOError as e:
        logger.error(f"Could not save tasks to database: {e}")

def add(new_task_description: str):
    tasks = load_data()

    new_task = {
        "id": tasks[-1]['id'] + 1 if len(tasks) else 1,
        "description": new_task_description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }

    tasks.append(new_task)
    post_data(tasks)
    logger.info(f"Task added successfully (ID: {new_task['id']})")

def update(id: int, new_task_description: str):
    tasks = load_data()

    if not len(tasks):
        logger.warning("There are no tasks right now. Add one before updating.")
        return

    task_to_update = None
    for task in tasks:
        if task["id"] == id:
            task_to_update = task
    
    if not task_to_update:
        logger.error(f"No task with ID {id} found.")
        return
    
    task_to_update["description"] = new_task_description
    task_to_update["updatedAt"] = datetime.now().isoformat()

    post_data(tasks)
    logger.info(f"Task updated successfully (ID: {id})")

def delete(id: int):
    tasks = load_data()

    index_to_remove = None
    for index, task in enumerate(tasks):
        if task["id"] == id:
            index_to_remove = index
    
    if index_to_remove is None:
        logger.error(f"There is no such task with ID {id}.")
        return 
    
    tasks.pop(index_to_remove)
    post_data(tasks)
    logger.info(f"Task deleted successfully (ID: {id})")

def list():
    tasks = load_data()
    if not tasks:
        logger.info("No tasks found.")
        return

    print("-" * 85)
    print(f"{'ID':<5} | {'Status':<12} | {'Description':<40} | {'Last Updated':<18}")
    print("-" * 85)
    for task in tasks:
        task_id = task.get("id", "")
        status = task.get("status", "")
        desc = task.get("description", "")
        
        # Handle timestamp keys
        updated = task.get("updatedAt") or task.get("createdAt") or ""
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
        logger.error(f"There is no such task with ID {id}.")
        return 

    task_to_mark["status"] = "done"
    task_to_mark["updatedAt"] = datetime.now().isoformat()

    post_data(tasks)
    logger.info(f"Task marked as done (ID: {id})")

def mark_in_progress(id: int):
    tasks = load_data()

    task_to_mark = None
    for task in tasks:
        if task["id"] == id:
            task_to_mark = task
    
    if not task_to_mark:
        logger.error(f"There is no such task with ID {id}.")
        return 

    task_to_mark["status"] = "in-progress"
    task_to_mark["updatedAt"] = datetime.now().isoformat()

    post_data(tasks)
    logger.info(f"Task marked as in-progress (ID: {id})")

def mark_todo(id: int):
    tasks = load_data()

    task_to_mark = None
    for task in tasks:
        if task["id"] == id:
            task_to_mark = task
    
    if not task_to_mark:
        logger.error(f"There is no such task with ID {id}.")
        return 

    task_to_mark["status"] = "todo"
    task_to_mark["updatedAt"] = datetime.now().isoformat()

    post_data(tasks)
    logger.info(f"Task marked as todo (ID: {id})")

def show_all_commands():
    print("Usage: task <command> [arguments]")
    print("\nAvailable commands:")
    print("  add <task_description>          Add a new task")
    print("  update <id> <description>       Update a task's description")
    print("  delete <id>                     Delete a task")
    print("  list                            List all tasks")
    print("  mark-done <id>                  Mark a task as done")
    print("  mark-in-progress <id>           Mark a task as in-progress")
    print("  mark-todo <id>                  Mark a task as todo")
    sys.exit(0)

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        show_all_commands()

    command = args[0]

    if command == "add":
        if len(args) != 2:
            logger.error("Invalid command usage.\nCorrect usage: task add <task_description>")
            sys.exit(1)

        new_task_description = args[1]
        add(new_task_description)

    elif command == "update":
        if len(args) != 3:
            logger.error("Invalid command usage.\nCorrect usage: task update <id> <new_task_description>")
            sys.exit(1)
        try:
            id = int(args[1])
            new_task_description = args[2]
            update(id, new_task_description)
        except ValueError:
            logger.error("id has to be an integer")
            sys.exit(1)

    elif command == "delete":
        if len(args) != 2:
            logger.error("Invalid command usage.\nCorrect usage: task delete <id>")
            sys.exit(1)
        
        try:
            id = int(args[1])
            delete(id)
        except ValueError:
            logger.error("id has to be an integer")
            sys.exit(1)

    elif command == "list":
        list()

    elif command == "mark-done":
        if len(args) != 2:
            logger.error("Invalid command usage.\nCorrect usage: task mark-done <id>")
            sys.exit(1)

        try:
            id = int(args[1])
            mark_done(id)
        except ValueError:
            logger.error("id has to be an integer")
            sys.exit(1)

    elif command == "mark-in-progress":
        if len(args) != 2:
            logger.error("Invalid command usage.\nCorrect usage: task mark-in-progress <id>")
            sys.exit(1)

        try:
            id = int(args[1])
            mark_in_progress(id)
        except ValueError:
            logger.error("id has to be an integer")
            sys.exit(1)

    elif command == "mark-todo":
        if len(args) != 2:
            logger.error("Invalid command usage.\nCorrect usage: task mark-todo <id>")
            sys.exit(1)

        try:
            id = int(args[1])
            mark_todo(id)
        except ValueError:
            logger.error("id has to be an integer")
            sys.exit(1)
            
    else:
        logger.error(f"Invalid command '{command}'.")
        show_all_commands()