import sqlite3
import sys
import json
import logging
from pathlib import Path
from contextlib import closing 
from datetime import datetime

DB_FILE = Path(__file__).parent / "tasks.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    with closing(get_connection()) as conn:
        with conn:
            stmt = """
                CREATE TABLE IF NOT EXISTS tasks( 
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT,
                    status      TEXT DEFAULT 'todo' CHECK(STATUS IN ('todo', 'in-progress', 'done')),
                    updated_at  TEXT DEFAULT (datetime('now', 'localtime')),
                    created_at  TEXT DEFAULT (datetime('now', 'localtime'))
                )
            """

            conn.execute(stmt)

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


def _get_all_tasks() -> list:
    """Fetches all tasks from the db and returns as a Python list or dictionaries"""
    try:
        with closing(get_connection()) as conn:
            stmt = "SELECT id, description, status, updated_at, created_at FROM tasks"

            conn.row_factory = sqlite3.Row
            with closing(conn.cursor()) as cursor:
                cursor.execute(stmt)
                return cursor.fetchall()
            
    except sqlite3.Error as e:
        logger.error(f"Falied to fetch tasks: {e}")
        return []


def add(new_task_description: str):
    try:
        with closing(get_connection()) as conn:
            with conn:
                stmt = """
                    INSERT INTO tasks (description) VALUES (?)
                """

                cursor = conn.execute(stmt, (new_task_description,))

                new_id = cursor.lastrowid

                logger.info(f"Task added successfully (ID: {new_id})")
            
    except sqlite3.Error as e:
        logger.error(f"An error occurred: {e}")    

def update(id: int, new_task_description: str):
    try:
        with closing(get_connection()) as conn:
            with conn:
                stmt = """
                    UPDATE tasks SET description = ?, updated_at = datetime('now', 'localtime') WHERE id = ?
                """
                
                cursor = conn.execute(stmt, (new_task_description, id))

                if cursor.rowcount > 0:
                    logger.info(f"Task updated successfully (ID: {id})")
                else:
                    logger.warning(f"Task not found (ID: {id})")

    except sqlite3.Error as e:
        logger.error(f"An error occurred: {e}")
    

def delete(id: int):
    try:
        with closing(get_connection()) as conn:
            with conn:
                stmt = """
                    DELETE FROM tasks WHERE ID = ?
                """

                cursor = conn.execute(stmt, (id,))

                if cursor.rowcount > 0:
                    logger.info(f"Task was deleted successfully (ID: {id})")
                else:
                    logger.warning(f"Task not found (ID: {id})")
    
    except sqlite3.Error as e:
        logger.error(f"An error occurred: {e}")

def display_tasks(status_filter: str = None):
    tasks = _get_all_tasks()
    if status_filter:
        status_filter = status_filter.lower()
        if status_filter not in ["todo", "in-progress", "done"]:
            logger.error(f"Invalid status filter '{status_filter}'. Use 'todo', 'in-progress', or 'done'.")
            return
        tasks = [t for t in tasks if t["status"] == status_filter]

    if not tasks:
        logger.info("No tasks found.")
        return

    print("-" * 85)
    print(f"{'ID':<5} | {'Status':<12} | {'Description':<40} | {'Last Updated':<18}")
    print("-" * 85)
    for task in tasks:
        task_id = task["id"]
        status = task["status"]
        desc = task["description"]
        
        # Handle timestamp keys
        updated = task["updated_at"] or task["created_at"] or ""
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
    try:
        with closing(get_connection()) as conn:
            with conn:
                stmt = """
                    UPDATE tasks SET status = 'done', updated_at = datetime('now', 'localtime') WHERE id = ?
                """

                cursor = conn.execute(stmt, (id,))

                if cursor.rowcount > 0:
                    logger.info(f"Task marked as 'done' (ID: {id})")
                else:
                    logger.warning(f"Task not found (ID: {id})")
    except sqlite3.Error as e:
        logger.error(f"An error occurred: {e}")

   

def mark_in_progress(id: int):
    try:
        with closing(get_connection()) as conn:
            with conn:
                stmt = """
                    UPDATE tasks SET status = 'in-progress', updated_at = datetime('now', 'localtime') WHERE id = ?
                """

                cursor = conn.execute(stmt, (id,))

                if cursor.rowcount > 0:
                    logger.info(f"Task marked as 'in progress' (ID: {id})")
                else:
                    logger.warning(f"Task not found (ID: {id})")
    except sqlite3.Error as e:
        logger.error(f"An error occurred: {e}")

def mark_todo(id: int):
    try:
        with closing(get_connection()) as conn:
            with conn:
                stmt = """
                    UPDATE tasks SET status = 'todo', updated_at = datetime('now', 'localtime') WHERE id = ?
                """

                cursor = conn.execute(stmt, (id,))

                if cursor.rowcount > 0:
                    logger.info(f"Task marked as 'todo' (ID: {id})")
                else:
                    logger.warning(f"Task not found (ID: {id})")

    except sqlite3.Error as e:
        logger.error(f"An error occurred: {e}")

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
    init_db()
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
        status_filter = args[1] if len(args) > 1 else None
        display_tasks(status_filter)

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