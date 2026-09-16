#!/usr/bin/env python3
"""tinytodo: a persistent todo list in a single file."""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

STORE = Path.home() / ".tinytodo.json"
MARKS = {"h": "!!", "m": "!", "l": ""}


def load():
    if STORE.exists():
        return json.loads(STORE.read_text(encoding="utf-8"))
    return []


def save(tasks):
    STORE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def cmd_add(args, tasks):
    tasks.append({
        "text": args.text,
        "priority": args.priority,
        "done": False,
        "added": datetime.now().isoformat(timespec="seconds"),
        "finished": None,
    })
    save(tasks)
    print(f"Added #{len(tasks)}: {args.text}")


def cmd_list(args, tasks):
    shown = 0
    for i, task in enumerate(tasks, start=1):
        if task["done"] and not args.all:
            continue
        flag = "[x]" if task["done"] else "[ ]"
        mark = MARKS.get(task["priority"], "")
        print(f"  {flag} #{i:<3} {mark:>2} {task['text']}")
        shown += 1
    pending = sum(1 for t in tasks if not t["done"])
    print(f"\n{pending} task(s) pending.")


def cmd_done(args, tasks):
    try:
        task = tasks[args.id - 1]
    except IndexError:
        sys.exit(f"No task with id {args.id}")
    if task["done"]:
        print("Already completed.")
        return
    task["done"] = True
    task["finished"] = datetime.now().isoformat(timespec="seconds")
    save(tasks)
    print(f"Completed: {task['text']}")


def cmd_undo(args, tasks):
    try:
        task = tasks[args.id - 1]
    except IndexError:
        sys.exit(f"No task with id {args.id}")
    if not task["done"]:
        print("Not completed yet.")
        return
    task["done"] = False
    task["finished"] = None
    save(tasks)
    print(f"Reopened: {task['text']}")


def cmd_rm(args, tasks):
    try:
        removed = tasks.pop(args.id - 1)
    except IndexError:
        sys.exit(f"No task with id {args.id}")
    save(tasks)
    print(f"Removed: {removed['text']}")


def main():
    parser = argparse.ArgumentParser(prog="tinytodo", description="persistent todo list")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("text")
    p_add.add_argument("-p", "--priority", choices=MARKS.keys(), default="m",
                       help="Priority: h(igh), m(edium), l(ow)")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List pending tasks")
    p_list.add_argument("-a", "--all", action="store_true", help="Include completed tasks")
    p_list.set_defaults(func=cmd_list)

    p_done = sub.add_parser("done", help="Mark a task complete")
    p_done.add_argument("id", type=int)
    p_done.set_defaults(func=cmd_done)

    p_undo = sub.add_parser("undo", help="Reopen a completed task")
    p_undo.add_argument("id", type=int)
    p_undo.set_defaults(func=cmd_undo)

    p_rm = sub.add_parser("rm", help="Delete a task")
    p_rm.add_argument("id", type=int)
    p_rm.set_defaults(func=cmd_rm)

    args = parser.parse_args()
    tasks = load()
    args.func(args, tasks)


if __name__ == "__main__":
    main()
