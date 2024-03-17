#Display list of current tasks
def display_tasks(list_of_tasks, due_task):
    if list_of_tasks:
        print("These are your tasks: \n")
        for i, tasks in enumerate(list_of_tasks,start=1):
            print(f"Task{i}: {tasks} due by {due_task}")
    else:
        print("There is no tasks: ")

#function: Append tasks
def adding_tasks(list_of_tasks,new_tasks,due_task):
    list_of_tasks.update({new_tasks : due_task})
    print(f"your {new_tasks} are added on the list and due by {due_task}")

#Function: Append due day and time

#Function:Append priority of tasks
#function: remove particular tasks
def finished_tasks(list_of_tasks, complete_task=None):
    list_of_tasks.pop(complete_task)
#Function:Remove tasks from lists
def clear_tasks(list_of_tasks):
    list_of_tasks.clear()
    print("all of tasks have been deleted")
#Feature: unfinished, ongoing, finished, expired tasks

def main_todo():
    list_of_tasks = {}

    while True:
        print("1: display tasks")
        print("2: add tasks")
        print("3: remove tasks")
        print("4: delete them all")

        num_ope_tasks = input("Please input number: ")

        if num_ope_tasks == "1":
            display_tasks(list_of_tasks,due_task)
        elif num_ope_tasks == "2":
            new_tasks = input("Please add your tasks: ")
            due_task = input("Enter due of task: ")
            adding_tasks(list_of_tasks, new_tasks,due_task)
        elif num_ope_tasks == "3":
            complete_tasks = input("Please enter number: ")
            finished_tasks(list_of_tasks,complete_tasks)
        elif num_ope_tasks == "4":
            clear_tasks(list_of_tasks)
            break
        else:
            print("Invalid number")

main_todo()