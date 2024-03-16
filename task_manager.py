"""
Task Manager Application

This program is a simple task manager application designed to help users manage their tasks efficiently.

It allows users to register new accounts, add tasks, view all tasks, view tasks assigned to them,
generate reports on task and user statistics, and display the generated reports.

The program reads and writes data to text files for storing user information and task details.
It provides a menu-based interface for users to interact with the application.

Please note that this program is a basic implementation and may require additional features
or improvements for production use.
"""

# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

#  Defining functions for task_manager


def reg_user(username_password):
    '''Add a new user to the user.txt file'''
    while True:
        # - Request input of a new username.
        new_username = input("New Username: ")

        if new_username in username_password:
            print("Error. Username already exists. Please choose a different username.")
            continue

        # - Request input of a new password.
        new_password = input("New Password: ")
        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password

            with open("user.txt", "w") as out_file:
                user_data = [
                    f"{k};{username_password[k]}" for k in username_password]
                out_file.write("\n".join(user_data))
            # Break out of the loop as all conditions are satisfied.
            break

        # - Otherwise you present a relevant message.
        else:
            print("Passwords do no match")


def add_task(task_list, username_password):
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(
                task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


def mark_complete(task_list, task_number):
    '''Mark a task as complete'''
    if task_number < 1 or task_number > len(task_list):
        print("Invalid task number.")
        return

    task = task_list[task_number - 1]
    if task['completed']:
        print("Task is already marked as complete.")
    else:
        task['completed'] = True
        update_tasks_file(task_list)
        print("Task marked as complete.")


def edit_task(task_list, task_number):
    '''Edit a task (username or due date)'''
    if task_number < 1 or task_number > len(task_list):
        print("Invalid task number.")
        return

    task = task_list[task_number - 1]
    if task['completed']:
        print("Cannot edit a completed task.")
    else:
        print(f"Editing Task {task_number}: {task['title']}")
        print("1. Edit assigned username")
        print("2. Edit due date")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            new_username = input("Enter new username: ")
            task['username'] = new_username
        elif choice == '2':
            while True:
                try:
                    new_due_date = input("Enter new due date (YYYY-MM-DD): ")
                    task['due_date'] = datetime.strptime(
                        new_due_date, DATETIME_STRING_FORMAT)
                    break
                except ValueError:
                    print("Invalid datetime format. Please use the format specified.")
        else:
            print("Invalid choice.")

        update_tasks_file(task_list)
        print("Task updated.")


def update_tasks_file(task_list):
    '''Update the tasks.txt file with the modified task list'''
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = [
            ";".join([
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]) for t in task_list
        ]
        task_file.write("\n".join(task_list_to_write))


def view_all(task_list):
    '''Reads the task from task.txt file and prints to the console in the 
        improved format with task numbers
    '''
    if not task_list:
        print("No tasks available.")
        return

    print("TASKS:")
    for i, t in enumerate(task_list, start=1):
        disp_str = f"{i}. Task: \t\t {t['title']}\n"
        disp_str += f"   Assigned to: \t {t['username']}\n"
        disp_str += f"   Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"   Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"   Task Description: \n   {t['description']}\n"
        disp_str += f"   Completed: \t {t['completed']}\n"
        print(disp_str)


def view_mine(task_list, curr_user):
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
    '''
    for t in task_list:
        if t['username'] == curr_user:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

    while True:
        try:
            choice = int(input(
                "Enter the number of the task to select or -1 to return to the main menu: "))
            if choice == -1:
                return
            elif 1 <= choice <= len(task_list):
                task_number = choice
                break
            else:
                print("Invalid task number. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        print(
            f"\nSelected Task {task_number}: {task_list[task_number - 1]['title']}")
        print("1. Mark as Complete")
        print("2. Edit Task")
        print("3. Return to Main Menu")
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            mark_complete(task_list, task_number)
        elif choice == '2':
            edit_task(task_list, task_number)
        elif choice == '3':
            return
        else:
            print("Invalid choice.")


def check_and_generate_reports(task_list, username_password):
    '''Check if reports exist, and if not, generate them.'''
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_task_overview(task_list)
        generate_user_overview(username_password, task_list)


def generate_task_overview(task_list):
    '''Generate task overview and save it to task_overview.txt'''
    print("Generating task_overview.txt")
    total_tasks = len(task_list)
    completed_tasks = sum(task['completed'] for task in task_list)
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'] < datetime.combine(
        date.today(), datetime.min.time()))

    incomplete_percentage = (
        incomplete_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / incomplete_tasks) * \
        100 if incomplete_tasks > 0 else 0

    task_overview = [
        f"Total tasks: {total_tasks}\n",
        f"Completed tasks: {completed_tasks}\n",
        f"Incomplete tasks: {incomplete_tasks}\n",
        f"Overdue tasks: {overdue_tasks}\n",
        f"Percentage of incomplete tasks: {incomplete_percentage:.2f}%\n",
        f"Percentage of overdue tasks: {overdue_percentage:.2f}%"
    ]

    print("Debug Information:")
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Incomplete tasks: {incomplete_tasks}")
    print(f"Overdue tasks: {overdue_tasks}")
    print(f"Percentage of incomplete tasks: {incomplete_percentage:.2f}%")
    print(f"Percentage of overdue tasks: {overdue_percentage:.2f}%")

    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("".join(task_overview))

    print("Success.")


def generate_user_overview(username_password, task_list):
    '''Generate user overview and save it to user_overview.txt'''
    print("Generating user_overview.txt")
    total_users = len(username_password)
    total_tasks = len(task_list)

    user_overview = [
        f"Total users: {total_users}\nTotal tasks: {total_tasks}\n"
    ]

    for username in username_password:
        user_tasks = [
            task for task in task_list if task['username'] == username]
        total_user_tasks = len(user_tasks)
        completed_user_tasks = sum(task['completed'] for task in user_tasks)
        incomplete_user_tasks = total_user_tasks - completed_user_tasks
        overdue_user_tasks = sum(1 for task in user_tasks if not task['completed'] and task['due_date'] < datetime.combine(
            date.today(), datetime.min.time()))

        percentage_of_total_tasks = (
            total_user_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        percentage_completed = (
            completed_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
        percentage_incomplete = (
            incomplete_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
        percentage_overdue = (overdue_user_tasks / incomplete_user_tasks) * \
            100 if incomplete_user_tasks > 0 else 0

        user_overview.extend([
            f"\nUser: {username}\n",
            f"Total tasks assigned: {total_user_tasks}\n",
            f"Percentage of total tasks: {percentage_of_total_tasks:.2f}%\n",
            f"Percentage completed: {percentage_completed:.2f}%\n",
            f"Percentage incomplete: {percentage_incomplete:.2f}%\n",
            f"Percentage overdue: {percentage_overdue:.2f}%\n"
        ])

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("".join(user_overview))

    print("Success.")


def display_reports():
    '''Display the reports on the screen.'''
    with open("task_overview.txt", "r") as task_overview_file:
        print("Task Overview:")
        print(task_overview_file.read())

    with open("user_overview.txt", "r") as user_overview_file:
        print("\nUser Overview:")
        print(user_overview_file.read())


# Create tasks.txt if it doesn't exist.
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component.
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(
        task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(
        task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


# ====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account.
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data.
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary.
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # Presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user(username_password)

    elif menu == 'a':
        add_task(task_list, username_password)

    elif menu == 'va':
        view_all(task_list)

    elif menu == 'vm':
        view_mine(task_list, curr_user)

    elif menu == 'gr':
        generate_task_overview(task_list)
        generate_user_overview(username_password, task_list)
        print("Reports generated.")

    elif menu == 'ds' and curr_user == 'admin':
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        check_and_generate_reports(task_list, username_password)
        display_reports()

    elif menu == 'ds' and curr_user != 'admin':
        '''If the user is not an admin display an error message.'''
        print("Error.This option requires admin permissions.")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
