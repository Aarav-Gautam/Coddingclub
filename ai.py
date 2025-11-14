'''
1. add task ---we will use list
2. view task ---view the list
3. delete task --list.pop(),list.delete()
4. save layout ---tasks.txt
5. load layout ---file handling file i/0
'''

tasks = []
print('''
1. Add task 
2. View task 
3. Delete task 
4. Save layout 
5. Load layout 
6. Exit
Enter the Choice (1/2/3/4/5/6)
''')
while True:

    choice = int(input("Choice: "))
    if choice == 1:
        addedtask = input("Add task: ")
        tasks.append(addedtask)  # adds the use's task to task list
        # print(tasks)

    elif choice == 2:
        '''
        1. eat
        2. play

        '''
        if len(tasks) == 0:
            print("No tasks added. You have no tasks")

        else:
            taskno = 1
            for task in tasks:
                print(str(taskno) + ".", task)
                taskno += 1

    elif choice == 3:

        if len(tasks) == 0:
            print("No tasks added. You have no tasks")

        else:
            taskno = 1
            for task in tasks:
                print(str(taskno) + ".", task)
                taskno += 1
        remove = int(input("enter task number to remove: "))
        try:
            print(f"The removed task is {tasks.pop(remove - 1)}.")
        except IndexError as e:
            print(f"Please enter a valid task number.", e)

    elif choice == 4:
        with open("tasks.txt", "w") as f:
            f.write("")
        with open("tasks.txt", "a") as f:
            for task in tasks:
                f.write(task + "\n")
    elif choice == 5:
        try:
            with open("tasks.txt", "r") as f:
                tasks = [line.strip() for line in f]
            print("Tasks loaded:", tasks)
        except FileNotFoundError:
            print("tasks.txt not found! Save tasks first.")

    elif choice == 6:
        break
