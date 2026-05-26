# Task Tracker CLI

A lightweight command-line interface (CLI) task tracker built in Python. Tasks are persisted globally in a `tasks.json` file.

## Usage

Run `task` followed by one of the commands below:

### 1. Add a Task
Adds a new task (defaults to status `todo`).
```bash
task add "Buy groceries"
```

### 2. Update a Task
Updates the description of an existing task.
```bash
task update <id> "Buy groceries and prep dinner"
```

### 3. Delete a Task
Removes a task from the list.
```bash
task delete <id>
```

### 4. Update Task Status
Mark a task as todo, in-progress, or completed.
```bash
task mark-todo <id>
task mark-in-progress <id>
task mark-done <id>
```

### 5. List Tasks
List all tasks or filter them by status (`todo`, `in-progress`, `done`).
```bash
task list
task list todo
task list in-progress
task list done
```

## Data Storage
All tasks are stored in `tasks.json` inside the directory where `task_manager.py` resides.
