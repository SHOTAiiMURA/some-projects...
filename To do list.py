#create list of To do
def ui_tasks(list_tasks):
    if not list_tasks:
        print("There is no tasks")
    else:
        print("Current tasks:")
        for i, tasks in enumerate(list_tasks, start=1):
            print(f"Tasks{i}: {tasks}")
#add tasks
def adding_tasks(list_tasks,new_tasks):
    list_tasks.append(new_tasks)
    print(f"your {new_tasks} are added on list")

#remove tasks
def delete_tasks(list_tasks, number_tasks):
    if 1 <= number_tasks >= len(list_tasks):
        deleted_tasks = list_tasks.pop(number_tasks-1)
        print(f"{deleted_tasks} has been deleted")
    else:
        print("invalid number, please do it again")

def clear_lists(list_tasks):
    list_tasks.clear()
    print("all of tasks have been deleted")


#input tasks
def main():
    list_tasks=[]

    while True:
        print("1: show tasks")
        print("2: add tasks")
        print("3: remove tasks")
        print("4: delete tasks and close")

        user_int_tasks=input("Please input number: ")

        if user_int_tasks == "1":
            ui_tasks(list_tasks)
        elif user_int_tasks == "2":
            new_tasks=input("please input new tasks here: ")
            adding_tasks(list_tasks, new_tasks)
        elif user_int_tasks == "3":
            user_int_tasks == input("input number that you want to delete: ")
            delete_tasks(list_tasks, number_tasks)
        elif user_int_tasks == "4":
            clear_lists(list_tasks)
            break
        else:
            print("invalid number")
if __name__ == "__main__":
    main()



