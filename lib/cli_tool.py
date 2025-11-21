# cli_tool.py
# cli_tool.py

import argparse
from models import Task, User

# In-memory storage for the session
users = {}

# ---------------------------
# Command Handlers
# ---------------------------

def add_task(args):
    """Handles: add-task <user> <title>"""
    user = users.get(args.user) or User(args.user)
    users[args.user] = user

    task = Task(args.title)
    user.add_task(task)


def complete_task(args):
    """Handles: complete-task <user> <title>"""
    user = users.get(args.user)

    if not user:
        print("❌ User not found.")
        return

    for task in user.tasks:
        if task.title == args.title:
            task.complete()
            return

    print("❌ Task not found.")


def list_tasks(args):
    """Handles: list-tasks <user>"""
    user = users.get(args.user)

    if not user:
        print("❌ User not found.")
        return

    if not user.tasks:
        print(f"📭 No tasks for {user.name}.")
        return

    print(f"\n📝 Tasks for {user.name}:")
    for t in user.tasks:
        status = "✔️" if t.completed else "❗"
        print(f"  {status} {t.title}")
    print()


# ---------------------------
# CLI SETUP
# ---------------------------

parser = argparse.ArgumentParser(description="Task Manager CLI")
subparsers = parser.add_subparsers(dest="command")

# add-task
add_parser = subparsers.add_parser("add-task", help="Add a new task")
add_parser.add_argument("user")
add_parser.add_argument("title")
add_parser.set_defaults(func=add_task)

# complete-task
complete_parser = subparsers.add_parser("complete-task", help="Complete a task")
complete_parser.add_argument("user")
complete_parser.add_argument("title")
complete_parser.set_defaults(func=complete_task)

# list-tasks
list_parser = subparsers.add_parser("list-tasks", help="List all tasks for a user")
list_parser.add_argument("user")
list_parser.set_defaults(func=list_tasks)

# Parse & Execute
args = parser.parse_args()

if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()
