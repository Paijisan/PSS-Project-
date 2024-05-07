from schedule import *
import unittest


class TestSchedule(unittest.TestCase):
    def testScenario1(self):
        print("TEST SCENARIO 1")
        # 1. Read the file Set1.json.  This should work.
        s = Schedule()
        file_read_is_success = s.read_file("Set1.json")
        # 1.1
        self.assertTrue(file_read_is_success)
        if file_read_is_success:
            print(f"#1 Success, readfile tasks loaded:{s.tasks}")

        # 2. Delete the task "Intern Interview".  This should work.
        task = s.get_task("Intern Interview")
        is_delete_success = s.delete_task(task)
        # 1.2 Assert
        self.assertTrue(is_delete_success)
        if is_delete_success:
            print(f"#2 Success, task deleted, task list: {s.tasks}")

        # 3. Add a new transient task:
        replacement_task = s.create_task("Intern Interview", "Appointment", 17, 2.5, 20200427)
        is_task_added = s.add_task(replacement_task)
        # 1.3 Assert
        self.assertTrue(is_task_added)
        if is_task_added:
            print(f"#3 Success, task added, task list: {s.tasks}")

        # 4. Add a new transient task: This should fail, as there is no transient task with type 'movie'
        try:
            new_task = s.create_task("Watch a movie", "Movie", 21.5, 2, 2020429)
            # 1.4 This should be unreachable
            self.assertTrue(False)
        except InvalidTaskException as ex:
            print(f"#4 Test successfully failed! Error occurred!: {ex}")

        # 5. Add a new transient task: This should fail, conflict.  You should be in class!
        try:
            new_task = s.create_task("Watch a movie", "Visit", 18.5, 2, 20200430)
            s.add_task(new_task)
            # 1.5 This should be unreachable
            self.assertTrue(False)
        except TaskOverlapException as ex:
            print(f"#5 Test successfully failed! Error occurred!: {ex}")

        # 6. Read the file Set2.json.  This should fail because of a conflict.
        try:
            print(s.read_file("Set2.json"))
            # 1.6 This should be unreachable
            self.assertTrue(False)
        except TaskOverlapException as ex:
            print(f"#6 Test successfully failed! Error occurred!: {ex}")

    def testScenario2(self):
        print("TEST SCENARIO 2")
        # 1. Read the file Set2.json.  This should work.
        s = Schedule()
        is_read_success = s.read_file("Set2.json")
        self.assertTrue(is_read_success)
        if is_read_success:
            print(f"#1 Success, readfile tasks loaded:{s.tasks}")

        # 2. Add an anti-task: This should fail, it does not exactly match a recurring task.
        new_task = s.create_task("Skip-out", "Cancellation", 19.25, .75, 20200430)
        try:
            s.add_task(new_task)
            # 2.2 Assert this is unreachable
            self.assertTrue(False, "Exception should have occurred before this assert")
        except InvalidTaskException as ex:
            print(f"#2 Successfully failed: Error occurred!: {ex}")

        # 3. Add an anti-task: This should work
        new_task2 = s.create_task("Skip a meal", "Cancellation", 17, 1, 20200428)
        is_add_success = s.add_task(new_task2)
        # 2.3 success
        self.assertTrue(is_add_success)
        if is_add_success:
            print(f"#3 Success, task added, task list: {s.tasks}")

        # 4. Read the file Set1.json.  This should work.
        is_read_success = s.read_file("Set1.json")
        self.assertTrue(is_read_success)
        if is_read_success:
            print(f"#4 Success, file read, task list:: {s.tasks}")


if __name__ == '__main__':
    unittest.main()

