from schedule import *


def scenario1():
    print("TEST SCENARIO 1")
    # 1. Read the file Set1.json.  This should work.
    s = Schedule()
    if s.read_file("Set1.json"):
        print(f"#1 Success, readfile tasks loaded:{s.tasks}")

    # 2. Delete the task "Intern Interview".  This should work.
    task = s.get_task("Intern Interview")
    if s.delete_task(task):
        print(f"#2 Success, task deleted, task list: {s.tasks}")

    # 3. Add a new transient task:
    replacement_task = s.create_task("Intern Interview", "Appointment", 17, 2.5, 20200427)
    if s.add_task(replacement_task):
        print(f"#3 Success, task added, task list: {s.tasks}")

    # 4. Add a new transient task: This should fail, as there is no transient task with type 'movie'
    try:
        new_task = s.create_task("Watch a movie", "Movie", 21.5, 2, 2020429)
    except InvalidTaskException as ex:
        print(f"#4 Test successfully failed! Error occurred!: {ex}")

    # 5. Add a new transient task: This should fail, conflict.  You should be in class!
    try:
        new_task = s.create_task("Watch a movie", "Visit", 18.5, 2, 20200430)
        s.add_task(new_task)
    except TaskOverlapException as ex:
        print(f"#5 Test successfully failed! Error occurred!: {ex}")

    # 6. Read the file Set2.json.  This should fail because of a conflict.
    try:
        print(s.read_file("Set2.json"))
    except TaskOverlapException as ex:
        print(f"#6 Test successfully failed! Error occurred!: {ex}")


def scenario2():
    print("TEST SCENARIO 2")
    # 1. Read the file Set2.json.  This should work.
    s = Schedule()
    if s.read_file("Set2.json"):
        print(f"#1 Success, readfile tasks loaded:{s.tasks}")

    # 2. Add an anti-task: This should fail, it does not exactly match a recurring task.
    new_task = s.create_task("Skip-out", "Cancellation", 19.25, .75, 20200430)
    try:
        s.add_task(new_task)
    except InvalidTaskException as ex:
        print(f"#2 Successfully failed: Error occurred!: {ex}")

    # 3. Add an anti-task: This should work
    new_task2 = s.create_task("Skip a meal", "Cancellation", 17, 1, 20200428)
    if s.add_task(new_task2):
        print(f"#3 Success, task added, task list: {s.tasks}")


    # 4. Read the file Set1.json.  This should work.
    if s.read_file("Set1.json"):
        print(f"#4 Success, file read, task list:: {s.tasks}")


if __name__ == '__main__':
    scenario1()
    scenario2()

