# Task Tracker CLI

A lightweight command-line interface (CLI) task tracker built in Python. Tasks are persisted in a SQLite database file (`tasks.db`).

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

All tasks are stored in a SQLite database file named `tasks.db` in the same directory as `task_manager.py`.

## Installation & Setup

To run the `task` command from anywhere in your terminal, add the project directory to your system's `PATH`.

### Windows (Add to PATH)

Run one of the following commands in your terminal (replace `C:\path\to\task-cli` with the actual folder path):

- **Command Prompt (CMD)**:

  ```cmd
  setx PATH "%PATH%;C:\path\to\task-cli"
  ```

- **PowerShell**:
  ```powershell
  [System.Environment]::SetEnvironmentVariable("PATH", [System.Environment]::GetEnvironmentVariable("PATH", "User") + ";C:\path\to\task-cli", "User")
  ```

### macOS / Linux (Add to PATH)

1. Add the directory to your shell configuration (e.g., `~/.bashrc`, `~/.zshrc`):
   ```bash
   export PATH="$PATH:/path/to/task-cli"
   ```
2. Make the script executable:
   ```bash
   chmod +x /path/to/task-cli/task
   ```
3. Restart or source your configuration (`source ~/.zshrc`), then run the command: `task <command>`.
