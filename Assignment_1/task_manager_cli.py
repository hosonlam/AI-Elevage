from colorama import Fore, init
from prettytable import PrettyTable

tasks = []
table = PrettyTable()

# Set column names (field names)
table.field_names = ["id", "Decscription", "Completed"]


def add_task(decscription):
    task_id = tasks[-1]["id"] + 1 if tasks else 1
    task = {"id": task_id, "decscription": decscription, "completed": False}
    tasks.append(task)
    print(Fore.GREEN + f"\nTask '{decscription}' added with ID {task_id}.")


def view_task():
    table.clear_rows()

    if not tasks:
        print(Fore.RED + "\nNo tasks available.")
        return

    for task in tasks:
        statusDone = "Done"
        statusPending = "Pending"
        taskDecs = task["decscription"]
        taskId = task["id"]
        status = statusDone if task["completed"] else statusPending
        table.add_row([taskId, taskDecs, status])

    print(table)


def mark_complete(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            print(Fore.GREEN + f"\nTask ID {task_id} marked as complete.")
            return
    print(Fore.RED + f"\nTask ID {task_id} not found.")


def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    print(Fore.YELLOW + f"\nTask ID {task_id} deleted if it existed")


def main():
    init(autoreset=True)

    while True:
        print(Fore.CYAN + "\nOptions: add, view, complete, delete, exit")
        choice = input(Fore.YELLOW + "Enter command: " + Fore.RESET).strip().lower()
        if choice == "add":
            try:
                decs = str(
                    input(
                        Fore.YELLOW + "Enter task decscription: " + Fore.RESET
                    ).strip()
                )
                add_task(decs)
            except ValueError:
                print(Fore.RED + "\nInvalid input!")
        elif choice == "view":
            view_task()
        elif choice == "complete":
            try:
                task_id = int(
                    input(
                        Fore.YELLOW + "Enter task ID to mark as complete: " + Fore.RESET
                    )
                )
                mark_complete(task_id)
            except ValueError:
                print(Fore.RED + "\nInvalid task ID. Please enter a number.")
        elif choice == "delete":
            try:
                task_id = int(
                    input(Fore.YELLOW + "Enter task ID to delete: " + Fore.RESET)
                )
                delete_task(task_id)
            except ValueError:
                print(Fore.RED + "\nInvalid task ID. Please enter a number.")
        elif choice == "exit":
            print(Fore.GREEN + "\nExiting the task manager.")
            break
        else:
            print(Fore.RED + "\nInvalid command. Please try again.")


if __name__ == "__main__":
    main()
