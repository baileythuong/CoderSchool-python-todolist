import os
import sqlite3
from termcolor import colored
from datetime import date, datetime
from tabulate import tabulate

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

conn = sqlite3.connect(DEFAULT_PATH)
cur = conn.cursor()

todo_sql = """
    CREATE TABLE IF NOT EXISTS todo_list(
    id integer PRIMARY KEY,
    tasks text not null,
    create_at datetime,
    completion not null
    )
    """
cur.execute(todo_sql)
conn.commit()

def help_menu():
    os.system("cls" if os.name == "nt" else "clear")
    print(colored("keywords:", "green", attrs=["bold"]))
    print(colored('*' * 50, 'green'))
    print(colored('1. list all todos:', 'green'))
    print(colored('\t list', 'white'))
    print(colored('2. add a new todo:', 'green'))
    print(colored('\t add', 'white'))
    print(colored('3. delete a todo:', 'green'))
    print(colored('\t delete', 'white'))
    print(colored('4. mark a todo complete:', 'green'))
    print(colored('\t done', 'white'))
    print(colored('5. mark a todo incomplete:', 'green'))
    print(colored('\t undone', 'white'))
    print(colored('*' * 50, 'green'))

def add_todo():
    now = datetime.now().strftime("%a, %d %B, %H:%M")

    add_sql = """
        INSERT INTO todo_list(tasks, create_at, completion)
        VALUES (?, ?, ?)
        """

    complete = "Incompleted"

    task_input = colored("Compose a task: ", "yellow", attrs=["underline"])
    task = input(task_input)

    cur.execute(add_sql, (task, now, complete))
    print(colored("Successfully added new task.", "yellow"))
    conn.commit()
    list_todo()


def list_todo():
    select_sql = """
        SELECT * from todo_list
    """
    cur.execute(select_sql)
    todo_result = cur.fetchall()
    print(tabulate(todo_result, headers=["ID", "Tasks", "Date", "Completion"], tablefmt="github"))

def delete_todo():
    while True:
        try:
            list_todo()
            delete_prompt=colored("Enter task's ID to delete: #",
                            "yellow", attrs=["underline"])
            delete_row_id = int(input(delete_prompt))

            delete_sql = """
                    DELETE FROM todo_list
                    WHERE id = ?
                """

            ask = input(colored("Are you sure (Y/N)? ", "red", attrs=["bold"]))
            if ask == 'Y' or ask == 'y':
                cur.execute(delete_sql, (delete_row_id,))
                conn.commit()
                print(colored("Successfully deleted.", "yellow"))
                break
            elif ask == "N" or ask == "n":
                break
        
        except ValueError:
            print(colored("Oops! That was not a valid number.", "yellow"))

def complete_todo():
    complete_prompt = colored("Enter completed task's ID: #",
                     "yellow", attrs=["underline"])
    complete_row_id = input(complete_prompt)
    
    mark_complete = """
        UPDATE todo_list
        SET completion = ?
        WHERE id = ?;
    """

    cur.execute(mark_complete, ("Completed", complete_row_id))
    conn.commit()
    print(colored("Successfully updated.", "yellow"))

def incomplete_todo():
    incomplete_prompt = colored("Enter incompleted task's ID: #",
                     "yellow", attrs=["underline"])
    incomplete_row_id = input(incomplete_prompt)
    
    mark_incomplete = """
        UPDATE todo_list
        SET completion = ?
        WHERE id = ?;
    """

    cur.execute(mark_incomplete, ("Incompleted", incomplete_row_id))
    conn.commit()
    print(colored("Successfully updated.", "yellow"))

if __name__ == "__main__":
    help_menu()
    while True:
        try:
            text=colored("What would you like to do today?",
                        "cyan", attrs=["bold"])
            print(text)
            user_input=input()

            if user_input == "add":
                add_todo()

            elif user_input == "list":
                list_todo()
            
            elif user_input == "delete":
                delete_todo()
            
            elif user_input == "done":
                list_todo()
                complete_todo()
            
            elif user_input == "undone":
                list_todo()
                incomplete_todo()

            else:
                text=colored("There was an error, please try again.",
                                "red", attrs=["blink"])
                print(text)

        except KeyboardInterrupt:
            break
