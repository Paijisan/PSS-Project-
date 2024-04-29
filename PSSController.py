from schedule import Schedule
from viewer import Viewer
from task import Task
from typing import List
import json

class PSSController:
    def __init__(self):
        ##Initialize schedule, viewer, and other variables
        self.schedule: Schedule = Schedule()
        self.viewer: Viewer = Viewer()
        self.loaded_tasks: List[Task] = []

    def menu_and_act_loop(self) -> None:
        ##Main menu loop
        while True: ##user choice will correspond to the needed method and loop will end
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
                self.display_day()
            elif choice == "3":
                self.display_week()
            elif choice == "4":
                self.display_month()
            elif choice == "5":
                self.edit_task()
            elif choice == "6":
                self.delete_task()
            elif choice == "7":
                self.write_schedule_to_file()
            elif choice == "8":
                self.load_schedule_from_file()
            elif choice == "9":
                self.view_file()
            elif choice == "10":
                self.view_file_day()
            elif choice == "11":
                self.view_file_week()
            elif choice == "12":
                self.view_file_month()
            elif choice == "13":
                self.write_loaded_tasks_to_schedule()
            elif choice == "0":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please select a valid option.")
    
    def find_task(self, task_name: str) -> bool:
        ##Function to find a task by its name
        for task in self.schedule.tasks: ##iterate though the tasks in the schedule
            if task.get_name() == task_name:
                return True ##if task with the given task name is found, true is returned
        return False

    def add_task(self) -> None:
        ##Function to add a new task
        ##prompt user to input deatils for a new task
        print("Now adding a new task")
        task_name = input("Enter a task name: ")
        task_type = input("Enter task type: ")
        start_time = float(input("Enter start time (in hours): "))
        duration = float(input("Enter duration of time (in hours): "))
        start_date = int(input("Enter start date (in format YYYYMMDD): "))
        end_date = int(input("Enter the end date of the task (optional): "))
        frequency = int(input("Enter the frequency of the task (optional): "))
        target_task_name = input("Enter name for target task (optional): ")

         try:
            start_time = float(start_time_str)
            duration = float(duration_str)
            start_date = int(start_date_str)
            end_date = int(end_date_str) if end_date_str else None
            frequency = int(frequency_str) if frequency_str else None
        except ValueError as ve:
            print(f"Error converting input to appropriate data types: {ve}")
            return

        ##Create new task
        new_task = self.schedule.create_task(task_name, task_type, start_time, duration, start_date, end_date, frequency, target_task_name)
        
        ##Add task to schedule
        if new_task:
            try:
                if self.schedule.add_task(new_task):
                    print("Task added successfully!")
                else:
                    print("Failed to add task to the schedule.")
            except Exception as e:
                print(f"An error occurred while adding task to the schedule: {e}")
        else:
            print("Failed to create task.")

    def display_day(self) -> None:
        ##Function to display tasks for a day
        date = int(input("Enter the date in YYYYMMDD format: "))
        day_tasks = self.schedule.get_day_tasks(date)
        self.viewer.show_day(day_tasks)

    def display_week(self) -> None:
        ##Function to display tasks for a week
        ##prompt the user for an input date 
        ##rerieve tasks for the specified day from the schedule
        date = int(input("Enter any date within the week in YYYYMMDD format: "))
        week_tasks = self.schedule.get_week_tasks(date)
        self.viewer.show_week(week_tasks)

    def display_month(self) -> None:
        # Function to display tasks for a month
        ##prompt the user for an input date 
        ##retrieve tasks for the specified week from the schedule
        date = int(input("Enter any date within the month in YYYYMMDD format: "))
        month_tasks = self.schedule.get_month_tasks(date)
        self.viewer.show_month(month_tasks)

    def edit_task(self) -> None:
        ##Function to edit a task
        ##Prompt the user to input the name of the task to edit.
        ##If the task exists, prompt the user to input new details for the task (name, type, start time, duration).
        ##Create a new task object with the updated details.
        task_name = input("Enter the name of the task to edit: ")

        if self.find_task(task_name):
            new_task_name = input("Enter new task name: ")
            new_task_type = input("Enter new task type: ")
            new_task_start_time = float(input("Enter new task start time: "))
            new_task_duration = float(input("Enter new task duration: "))

            ##Create new task
            new_task = Task(new_task_name, new_task_type, new_task_start_time, new_task_duration)

            if self.schedule.edit_task(task_name, new_task):  
                print("Task edited successfully!")
            else:
                print("Failed to edit task.")
        else:
            print("Task not found.")

    def delete_task(self) -> None:
        ##Function to delete a task
        task_name = input("Enter the name of the task to delete: ")
        task = self.schedule.get_task(task_name)

        if task:
            if self.schedule.delete_task(task):
                print("Task deleted successfully!")
            else:
                print("Failed to delete task.")
        else:
            print("Task not found.")

    def write_schedule_to_file(self) -> None:
        ##Function to write schedule to a file
        file_name = input("Enter the file name to write the schedule: ")
        schedule_data = []

        for task in self.schedule.tasks:
            task_data = {
                'Name': task.get_name(),
                'Type': task.get_task_type(),
                'StartTime': task.get_start_time(),
                'Duration': task.get_duration()
            }

            if isinstance(task, RecurringTask):
                task_data['StartDate'] = task.get_start_date()
                task_data['EndDate'] = task.get_end_date()
                task_data['Frequency'] = task.get_frequency()
            elif isinstance(task, TransientTask):
                task_data['Date'] = task.get_date()

            schedule_data.append(task_data)

        try:
            with open(file_name, 'w') as file:
                json.dump(schedule_data, file, indent=4)
            print("Schedule written to file successfully.")
        except Exception as e:
            print(f"Failed to write schedule to file: {e}")

    def load_schedule_from_file(self) -> None:
        ##Function to load schedule from a file
        file_name = input("Enter the file name to load the schedule: ")

        try:
            with open(file_name, 'r') as file:
                schedule_data = json.load(file)

                for task_data in schedule_data:
                    task_name = task_data['Name']
                    task_type = task_data['Type']
                    start_time = task_data['StartTime']
                    duration = task_data['Duration']
                    start_date = task_data.get('StartDate')
                    end_date = task_data.get('EndDate')
                    frequency = task_data.get('Frequency')
                    target_task_name = task_data.get('TargetTask')

                    target_task = self.schedule.get_task(target_task_name) if target_task_name else None

                    new_task = self.schedule.create_task(task_name, task_type, start_time, duration, start_date, end_date, frequency, target_task)

                   if new_task:
                        try:
                            if not self.schedule.add_task(new_task):
                                print(f"Failed to add task '{task_name}' to the schedule.")
                        except Exception as e:
                            print(f"An error occurred while adding task '{task_name}' to the schedule: {e}")
                    else:
                        print(f"Failed to create task '{task_name}'.")
                print("Schedule loaded from file successfully.")
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in the file '{file_name}'.")

    def view_file(self) -> None:
        ##Function to view contents of a file
        file_name = input("Enter the file name to view: ")

        try:
            with open(file_name, 'r') as file:
                file_contents = file.read()
                print("File contents: ")
                print(file_contents)
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")

    def view_file_day(self) -> None:
        ##Function to view tasks for a day from a file
        file_name = input("Enter the file name to view day: ")
        date = int(input("Enter the date in YYYYMMDD format: "))

        try:
            with open(file_name, 'r') as file:
                tasks_for_date = []

                for line in file:
                    task_info = line.strip().split(',')
                    if len(task_info) >= 3:  
                        task_date = int(task_info[2])  
                        if task_date == date:
                            name = task_info[0]
                            task_type = task_info[1]
                            start_time = float(task_info[3])  
                            duration = float(task_info[4])   
                            new_task = Task(name, task_type, start_time, duration)
                            tasks_for_date.append(new_task)

                if tasks_for_date:
                    print(f"Tasks for date {date}:")
                    for task in tasks_for_date:
                        print(task)
                else:
                    print("No tasks found for the specified date.")
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")

    ##Implement other view_file functions similarly

    def write_loaded_tasks_to_schedule(self) -> None:
        ##Function to write loaded tasks to the schedule
        for task in self.loaded_tasks:
            if self.schedule.add_task(task):
                print(f"Task '{task.get_name()}' added to the schedule successfully")
            else:
                print(f"Failed to add task '{task.get_name()}' to the schedule")

##Instantiate the controller and start the program
if __name__ == "__main__":
    controller = PSSController()
    controller.menu_and_act_loop()
