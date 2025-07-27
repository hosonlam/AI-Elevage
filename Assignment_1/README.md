# Task Manager CLI
 
This project is a simple command-line task manager written in Python. It allows users to add, view, complete, and delete tasks interactively. The interface uses the colorama library to provide colored output for better user experience.
 
## Features
 
- **Add Task:** Add a new task with a unique ID.
- **View Tasks:** List all tasks with their status (Pending/Done).
- **Complete Task:** Mark a task as complete by its ID.
- **Delete Task:** Remove a task by its ID.
- **Colored Output:** Uses colorama for a more user-friendly CLI.
 
## Approach
 
- Tasks are stored in a global list as dictionaries (`id`, `decscription`, `completed`).
- The main loop presents options and processes user input.
- Each action (`add`, `view`, `complete`, `delete`) is handled by a dedicated function.
- Input is validated and feedback is provided after each operation.
 
## Challenges & Solutions
 
- **Unique Task IDs:**  
  Ensured by incrementing from the last task's ID or starting at 1 if the list is empty.
- **Input Validation:**  
  Wrapped input parsing in `try/except` blocks to handle invalid input and provide clear error messages.
- **Task Not Found:**  
  The code checks for existence and notifies the user if the task is not found when completing or deleting.
 
## Enhancements
 
- **Colorful CLI:**  
  Used `colorama` for colored prompts and messages.
- **Immediate Feedback:**  
  After each operation, the current task list is displayed.
- **Extensible:**  
  The structure allows for easy addition of features like persistent storage or task priorities.
- **Pretty Table:**
  Used `prettytable` for print the table in cmd
 
## Usage
 
1. Install dependencies:
    ```bash
    pip install colorama
    ```
2. Run the script:
    ```bash
    python your_script.py
    ```
 
## Example

Options: add, view, complete, delete, exit
Enter command: delete
Enter task ID to delete: 1

Task ID 1 deleted if it existed

2 - Decscription: todo2, Status: Pending

Options: add, view, complete, delete, exit
Enter command: exit
Exiting the task manager.