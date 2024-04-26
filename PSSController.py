from schedule import Schedule
from viewer import Viewer
from task import Task
from typing import List
import json

class PSSController:
    def __init__(self):
        self.schedule: Schedule = Schedule()
        self.viewer: Viewer = Viewer()
        self.current_view = None
        self.menus: List = []
        self.loaded_tasks: List[Task] = []

    def menu_and_act_loop(self) -> None:
        while True:
            print("\nMain Menu")
            print("1. Add Task")
            print("2. Display Day")
            print("3. Display Week")
            print("4. Display Month")
            print("5. Edit Task")
            print("6. Delete Task")
            print("7. Write Schedule to File")
            print("8. Load Schedule from File")
            print("9. View File")
            print("10. View File Day")
            print("11. View File Week")
            print("12. View File Month")
            print("13. Write Loaded Tasks to Schedule")
            print("0. Exit")

            choice: str = input("Enter your choice: ")

            if choice == "1":
                self.add_task()
            elif choice == "2":
                date = int(input("Enter the date in YYYYMMDD format: "))
                self.display_day(date)
            elif choice == "3":
                date = int(input("Enter any date within the week in YYYYMMDD format: "))
                self.display_week(date)
            elif choice == "4":
                date = int(input("Enter any date within the month in YYYYMMDD format: "))
                self.display_month(date)
            elif choice == "5":
                self.edit_task()
            elif choice == "6":
                self.delete_task()
            elif choice == "7":
                file_name = input("Enter the file name to write the schedule: ")
                self.write_schedule_to_file(file_name)
            elif choice == "8":
                file_name = input("Enter the file name to load the schedule: ")
                self.load_schedule_from_file(file_name)
            elif choice == "9":
                file_name = input("Enter the file name to view: ")
                self.view_file(file_name)
            elif choice == "10":
                file_name = input("Enter the file name to view day: ")
                date = int(input("Enter the date in YYYYMMDD format: "))
                self.view_file_day(file_name, date)
            elif choice == "11":
                file_name = input("Enter the file name to view week: ")
                date = int(input("Enter any date within the week in YYYYMMDD format: "))
                self.view_file_week(file_name, date)
            elif choice == "12":
                file_name = input("Enter the file name to view month: ")
                date = int(input("Enter any date within the month in YYYYMMDD format: "))
                self.view_file_month(file_name, date)
            elif choice == "13":
                self.write_loaded_tasks_to_schedule()
            elif choice == "0":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please select a valid option.")
    
    def find_task(self, task_name: str) -> bool:
        """
        Find a task by its name.

        Parameters:
            task_name (str): The name of the task to find.

        Returns:
            bool: True if the task is found, False otherwise.
        """
        for task in self.schedule.tasks:
            if task.get_name() == task_name:
                return True
        return False

    def add_task(self) -> None:
        print("Now adding a new task")
        task_name = input("Enter a task name: ")
        task_type = input("Enter task type: ")
        start_time = float(input("Enter start time (in hours): "))
        duration = float(input("Enter duration of time (in hours): "))
        start_date = int(input("Enter start date (in format YYYYMMDD): "))
        end_date = int(input("Enter the end date of the task (optional): "))
        frequency = int(input("Enter the frequency of the task (optional): "))
        target_task_name = input("Enter name for target task (optional): ")

        if target_task_name:
            target_task = self.schedule.get_task(target_task_name)
        else:
            target_task = None

        new_task = self.schedule.create_task(task_name, task_type, start_time, duration, start_date, end_date, frequency, target_task)
        
        if self.schedule.add_task(new_task):
            print("Task added successfully!")
        else:
            print("Failed to add task.")

    def display_day(self, date: int) -> None:
        day_tasks = self.schedule.get_day_tasks(date)
        self.viewer.show_day(day_tasks)

    def display_week(self, date: int) -> None:
        week_tasks = self.schedule.get_week_tasks(date)
        self.viewer.show_week(week_tasks)

    def display_month(self, date: int) -> None:
        month_tasks = self.schedule.get_month_tasks(date)
        self.viewer.show_month(month_tasks)

    def edit_task(self)-> None:
        task_name = input("Enter the name of the task to edit: ")

        ##check to see if task is found in schedule
        if self.find_task(task_name):
            new_task_name = input("Enter new task name: ")
            new_task_type = input("Enter new task type: ")
            new_task_start_time = float(input("Enter new task start time: "))
            new_task_duration = float(input("Enter new task duration: "))

            new_task = Task(new_task_name, new_task_type, new_task_start_time, new_task_duration)

            if self.schedule.edit_task(task_name, new_task):  
                print("Task edited successfully!")
            else:
                print("Failed to edit task.")
        else:
            print("Task not found.")
        
    def delete_task(self) -> None:
        task_name = input("Enter the name of the task to delete: ")
        task = self.schedule.get_task(task_name)
        if task:
            if self.schedule.delete_task(task):
                print("Task deleted successfully!")
            else:
                print("Failed to delete task.")
        else:
            print("Task not found.")

    def write_schedule_to_file(self, file_name: str) -> None:
        schedule_data = []

        for task in self.schedule.tasks:

            task_data = {'name': task.get_name(), 'type': task.get_task_type(), 'start_date': task.get_start_date(), 'start_time': task.get_start_time(), 'duration': task.get_duration(), 
                         'end_date': task.get_end_date(), 'frequency': task.get_frequency()}
            
            schedule_data.append(task_data)

            with open(file_name, 'w') as file:
            json.dump(schedule_data, file, indent=4)

        print("Schedule written to", file_name)

    def load_schedule_from_file(self, file_name: str) -> None:
        # Implementation goes here
        pass

    def view_file(self, file_name: str) -> None:
        # Implementation goes here
        pass

    def view_file_day(self, file_name: str, date: int) -> None:
        # Implementation goes here
        pass

    def view_file_week(self, file_name: str, date: int) -> None:
        # Implementation goes here
        pass

    def view_file_month(self, file_name: str, date: int) -> None:
        # Implementation goes here
        pass

    def write_loaded_tasks_to_schedule(self) -> None:
        # Implementation goes here
        pass
