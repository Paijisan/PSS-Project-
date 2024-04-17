from tasks.task import Task
import json
from datetime import datetime


class Schedule:
    def __init__(self):
        self.tasks: list[Task] = []

    @staticmethod
    def create_task(task_name: str, task_type: str, start_time: float, duration: float, start_date: int,
                    end_date: int = None, frequency: int = None, target_task: Task = None) -> Task:
        """
        Creates a task to add to plan
        :param task_name: User given name as string
        :param task_type: Specific task "Type"
        :param start_time: positive number from 0 (midnight) to 23.75 (11:45 pm) to the nearest 15 minutes (0.25)
        :param duration: positive number from 0.25 to 23.75, rounded to the nearest 15 minutes.
        :param start_date: Integer, YYYYMMDD
        :param end_date: Integer, YYYYMMDD
        :param frequency: 1 is daily, 7 weekly
        :param target_task: Task to be cancelled by an "anti task"
        :return: A Task of type AntiTask, TransientTask, or Recurring Task
        """

        match task_type:
            case ["Cancellation"]:
                # Create Anti task here
                return AntiTask(task_name, task_type, start_time, duration, start_date, target_task)
            case ["Vist" | "Shopping" | "Appointment"]:
                # Create transient task here
                return TransientTask(task_name, task_type, start_time, duration, start_date)
            case _:
                # Create recurring task
                return RecurringTask(task_name, task_type, start_time, duration, start_date, end_date, frequency)



    @staticmethod
    def create_task_from_json(json_string: str) -> Task:
        """
        Creates a task from given json
        :param json_string: Expecting singular dict {} in string format
        :return:
        """
        j: dict = json.loads(json_string)
        # TODO Create reject code for bad json string
        new_task: Task = Schedule.create_task(j["Name"], j["Type"], j["StartTime"], j["Duration"],
                                              j.get("EndDate", None), j.get("Frequency", None))
        return new_task

    def delete_task(self, task: Task) -> bool:
        try:
            self.tasks.remove(task)
            return True
        except ValueError:
            return False

    def add_task(self, task: Task) -> bool:
        # TODO Check if task is valid
        self.tasks.append(task)
        return True

    def add_tasks(self, tasks: list[Task]) -> bool:
        # TODO Check if tasks are valid
        for task in tasks:
            self.add_task(task)
        return True

    def edit_task(self, old_task: Task, new_task: Task) -> bool:
        # TODO Check if new_task is valid
        if self.delete_task(old_task):
            self.tasks.append(new_task)
        return True

    def get_task(self, task_name: str) -> Task:
        for task in self.tasks:
            if task.get_name() == task_name:
                return task

    def write_file(self, file_name: str) -> bool:
        all_tasks: list = []
        for task in self.tasks:
            all_tasks.append(json.loads(task.to_json()))

        try:
            with open(file_name, "w") as out_file:
                out_file.write(str(all_tasks))
            return True
        except FileExistsError:  # This might be unreachable
            return False

    def read_file(self, file_name: str) -> bool:
        try:
            with open(file_name, "r") as in_file:
                j = json.load(in_file)
                self.add_tasks(j)
            return True
        except FileNotFoundError:
            return False

    def get_day_tasks(self, date: int) -> list[Task]:
        return_tasks: list = []
        target_date = datetime.fromisoformat(str(date))
        for task in self.tasks:
            task_date = Schedule.get_task_date(task)
            # TODO check for recurring
            if target_date == task_date:
                return_tasks.append(task)

        return return_tasks

    def get_week_tasks(self, date: int) -> list[Task]:
        return_tasks: list = []
        target_date = datetime.fromisoformat(str(date))
        target_week = target_date.isocalendar().week
        for task in self.tasks:
            task_date = Schedule.get_task_date(task)
            # TODO check for recurring
            if task_date.year == target_date.year and task_date.isocalendar().week == target_week:
                return_tasks.append(task)
        return return_tasks

    def get_month_tasks(self, date: int) -> list[Task]:
        return_tasks: list = []
        target_date = datetime.fromisoformat(str(date))
        for task in self.tasks:
            task_date = Schedule.get_task_date(task)
            # TODO check for recurring
            if target_date.year == task_date.year and target_date.month == task_date.month:
                return_tasks.append(task)

        return return_tasks

    def is_allowed_entry(self, new_task: Task) -> bool:
        pass

    def is_allowed_replace(self, old_task: Task, new_task: Task) -> bool:
        pass

    @staticmethod
    def get_task_date(task: Task) -> datetime:
        match task.get_task_type():
            case ["Cancellation" | "Vist" | "Shopping" | "Appointment"]:
                return datetime.fromisoformat(str(task.get_date()))
            case _:
                return datetime.fromisoformat(str(task.get_start_date()))
