#Display list of current tasks
def display_tasks(list_of_tasks):
    if list_of_tasks:
        print("These are your tasks: \n")
        for i, tasks in enumerate(list_of_tasks,start=1):
            print(f"Task{i}: {tasks}")
    else:
        print("There is no tasks: ")

#function: Append tasks
def adding_tasks(list_of_tasks,new_tasks):
    list_of_tasks.append(new_tasks)
    print(f"your {new_tasks} are added on the list")

#Function: Append due day and time
def set_due_tasks(list_of_tasks, due_task):
    if due_task:
        list_of_tasks += f"Due: {due_task}"
    list_of_tasks.append(due_task)
    print(f"your {list_of_tasks} due by {due_task}.")
#Function:Append priority of tasks

#Function:Remove tasks from lists

#Feature: unfinished, ongoing, finished, expired tasks

def main_todo():
    list_of_tasks = []

    while True:
        print("1: display tasks")
        print("2: add tasks")
        print("3: add due day")

        num_ope_tasks = input("Please input number: ")

        if num_ope_tasks == "1":
            display_tasks(list_of_tasks)
        elif num_ope_tasks == "2":
            new_tasks = input("Please add your tasks: ")
            adding_tasks(list_of_tasks,new_tasks)
        elif num_ope_tasks == "3":
            due_tasks = input("select your due day: ")
            set_due_tasks(list_of_tasks, due_task)
            break
        else:
            print("Invalid number")

main_todo()