from schedule import Schedule
from viewer import Viewer
from task import Taskgit 
from typing import List

class PSSController:
    def __init__(self):
        """
        Constructor for PSSController class.
        """
        self.schedule: Schedule = Schedule()  ##Initialize schedule object
        self.viewer: Viewer = Viewer()  ##Initialize viewer object
        self.current_view = None  ##Current view state
        self.menus: List = []  ##List of menus
        self.loaded_tasks: List[Task] = []  ##List of loaded tasks

    def menu_and_act_loop(self) -> None:
        """
        Main method to display menu options and handle user actions.
        """
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

    def add_task(self) -> None:
        """
        Prompt the user to input task details.
    Create a new task using the Schedule class's create_task method.
    Add the task to the schedule using the add_task method.
    Display a success message if the task is added successfully.
        """
        print("Now adding a new task")
        task_name = input("Enter a task name: ")
        task_type = input("Enter task type: ")
        start_time = float(input("Enter start time (in hours): "))
        duration = float(input("Enter duration of time(in hours)"))
        start_date = int(input("Enter start date (in format YYYYMMDD)"))
        end_date = int(input("Enter the end date of the task (optional): "))
        frequency = int(input("Enter the frequency of the task (optional): "))
        ##If applicable, task user to input target task info(for anti-task, optional option)
        target_task_name = input("Enter name for target task: ")

        if target_task_name:
            target_task = self.schedule.get_task(target_task_name)
        else:
            target_task = None

        ##add the task to the schedule
        new_task = self.schedule.create_task(task_name, task_type, start_time, duration, start_date, end_date, target_task)
        
        if self.schedule.add_task(new_task):
            print("Task added successfully!")
        else:
            print("Failed to add task.")   

    def find_task
            

    def display_day(self, date: int): 
        """
        Asks for the specified day from the schedule using get_day_tasks method.
    Display the tasks for the day using the Viewer class's show_day method.
    :parem: date(int): The date in YYYYMMDD format
        """
    day_tasks = self.schedule.get_day_tasks(date) ##gets the tasks from the specfied day on the schedule

    ##Display the tasks using the viewer class
    self.viewer.show_day(day_tasks)
    

    def display_week(self, date: int): 
        """
  Get the tasks for the specified week from the schedule using get_week_tasks method.
  Display the tasks for the week using the Viewer class's show_week method.
  :parem: date (int): the date in YYYYMMDD format (do any day of the week to display the week)
        """

    week_tasks = self.schedule.get_week_tasks(date)

    ##display
    self.viewer.show_week(week_tasks)
    

  

    def display_month(self, date: int) 
        """
        
  Get the tasks for the specified month from the schedule using get_month_tasks method.
  Display the tasks for the month using the Viewer class's show_month method.

        """
    month_tasks = self.schedule.get_month_tasks(date)

    self.viewer.show_month(month_tasks)

      

    def edit_task(self) -> None:
        """
       Prompt the user to input the name or ID of the task to edit.
  Find the task in the schedule using find_task method.
  If the task is found, prompt the user to input new task details.
  Update the task using the Schedule class's edit_task method.
  Display a success message if the task is edited successfully.

        """
        

    def delete_task(self) -> None:
        """
       Prompt the user to input the name or ID of the task to delete.
  Find the task in the schedule using find_task method.
  If the task is found, delete the task using the Schedule class's delete_task method.
  Display a success message if the task is deleted successfully.
        """
        

    def write_schedule_to_file(self) -> None:
        """
        Prompt the user to input the file name to write the schedule.
  Write the schedule to the specified file using the Schedule class's write_file method.
  Display a success message if the schedule is written successfully.

        """
        

    def load_schedule_from_file(self) -> None:
        """
       Prompt the user to input the file name to load the schedule.
  Load the schedule from the specified file using the Schedule class's read_file method.
  Display a success message if the schedule is loaded successfully.

        """
       

    def view_file(self) -> None:
        """
        Prompt the user to input the file name to view.
  Display the contents of the specified file using the Viewer class's view_file method.

        """
        

    def view_file_day(self) -> None:
        """
        Method to view tasks for a specific day from a file.
        """

    def view_file_week(self) -> None:
        """
        Method to view tasks for a specific week from a file.
        """
        

    def view_file_month(self) -> None:
        """
        Method to view tasks for a specific month from a file.
        """
        

    def write_loaded_tasks_to_schedule(self) -> None:
        """
        Method to write loaded tasks to the schedule.
        """
        
