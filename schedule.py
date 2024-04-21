from task import Task, AntiTask, RecurringTask, TransientTask
import json
from datetime import datetime, timedelta


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
            case "Cancellation":
                # Create Anti task here
                return AntiTask(task_name, task_type, start_time, duration, start_date, target_task)
            case "Vist" | "Shopping" | "Appointment":
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
        j: dict = json.loads(json_string.replace("'", '"'))
        # TODO Create reject code for bad json string
        new_task: Task = Schedule.create_task(j["Name"], j["Type"], j["StartTime"], j["Duration"], j.get("StartDate", j.get("Date", None)),
                                              j.get("EndDate", None), j.get("Frequency", None))
        return new_task

    def delete_task(self, task: Task) -> bool:
        try:
            self.tasks.remove(task)
            return True
        except ValueError:
            return False

    def add_task(self, task: Task) -> bool:
        if self.is_allowed_entry(task):
            self.tasks.append(task)
            return True
        return False

    def add_tasks(self, tasks: list[Task]) -> bool:
        # Verify all tasks are valid
        temp_schedule = Schedule()
        for task in tasks:
            if not temp_schedule.add_task(task):
                return False

        # Verify all tasks are allowed in current schedule
        success = 0
        for task in temp_schedule.tasks:
            success += self.add_task(task)

        # If a task fails to add, remove all other added tasks
        if success != len(temp_schedule.tasks):
            for task in temp_schedule.tasks:
                if task in self.tasks:
                    self.tasks.remove(task)
            return False

        return True

    def edit_task(self, old_task: Task, new_task: Task) -> bool:
        if self.delete_task(old_task):
            if not self.add_task(new_task):
                self.add_task(old_task)
                return False
        # Could not delete old task (Does not exist?)
        else:
            return False
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
                all_tasks = [Schedule.create_task_from_json(str(task)) for task in j]
                self.add_tasks(all_tasks)
            return True
        except FileNotFoundError:
            return False

    def get_day_tasks(self, date: int) -> list[Task]:
        return_tasks: list = []
        target_date = datetime.fromisoformat(str(date))
        target_date = target_date.date()

        for task in self.tasks:
            for date_pair in get_date_times(task):
                if target_date == date_pair[0].date():
                    return_tasks.append(task)
                    break

        return return_tasks

    def get_week_tasks(self, date: int) -> list[Task]:
        return_tasks: list = []
        target_date = datetime.fromisoformat(str(date))
        target_year = target_date.year
        target_week = target_date.isocalendar().week
        for task in self.tasks:
            task_dates = get_date_times(task)
            for task_date_pair in task_dates:
                task_date = task_date_pair[0]
                if task_date.year == target_year and task_date.isocalendar().week == target_week:
                    return_tasks.append(task)
                    break
        return return_tasks

    def get_month_tasks(self, date: int) -> list[Task]:
        return_tasks: list = []
        target_date = datetime.fromisoformat(str(date))
        target_year = target_date.year
        target_month = target_date.month
        for task in self.tasks:
            task_dates = get_date_times(task)
            for task_date_pair in task_dates:
                task_date = task_date_pair[0]
                if task_date.year == target_year and task_date.month == target_month:
                    return_tasks.append(task)
                    break
        return return_tasks

    def is_allowed_entry(self, new_task: Task) -> bool:
        for task in self.tasks:
            if has_overlap(new_task, task):
                # AntiTask allowance case
                if type(new_task) is AntiTask and type(task) is RecurringTask:
                    perfect_fit = Schedule.is_anti_task_of_task(new_task, task)
                    is_repeat = sum(1 for task in self.tasks if type(task) is AntiTask and anti_task_equality(new_task, task))
                    return perfect_fit and not is_repeat
                # If it is Transient or Recurring
                new_task_overlaps, old_task_overlaps = get_task_overlaps(new_task, task)
                # Check if old task has an anti task fitting every overlap
                anti_task_count = 0
                for old_task_time in old_task_overlaps:
                    anti_tasks = (n for n in self.tasks if type(n) is AntiTask)
                    for anti_task in anti_tasks:
                        anti_task_time = Schedule.get_task_date(anti_task)
                        if anti_task_time == old_task_time[0]:
                            anti_task_count += 1
                is_allowed = anti_task_count == len(old_task_overlaps)
                return is_allowed

        # No overlap found!
        # A non-overlapping AntiTask is not allowed
        if type(new_task) is AntiTask:
            return False
        # All other tasks have no overlap is allowed
        else:
            return True

    def get_anti_tasks_of_same_day(self, task: Task) -> list:
        """
        Find anti tasks that occur on the same day as a TransientTask or RecurringTask
        :param task: Must be TransientTask or RecurringTask
        :return: List of AntiTasks that occur same day
        """
        task_list = []
        if type(task) is TransientTask:
            task.get_date()
            anti_tasks = (_task for _task in self.tasks() if type(_task) is AntiTask)
            for active_task in anti_tasks:
                new_task_date = Schedule.get_task_date(task)
                anti_task_date = Schedule.get_task_date(active_task)
                if new_task_date.weekday() == anti_task_date.weekday():
                   task_list.append(active_task)
        else:
            anti_tasks = (_task for _task in self.tasks if type(_task) is AntiTask)
            for active_task in anti_tasks:
                if Schedule.is_anti_task_of_task(active_task, task):
                    task_list.append(active_task)

        return task_list


    @staticmethod
    def is_anti_task_of_task(anti_task: AntiTask, task: RecurringTask):
        if has_overlap(anti_task, task):
            recur_task = task
            anti_task_start = Schedule.get_task_date(anti_task)
            anti_task_end = Schedule.get_task_end_time(anti_task)
            recur_task_start = Schedule.get_task_date(recur_task)
            recur_task_end = Schedule.get_last_recurrence_end_time(recur_task)
            recur_task_same_day_start = anti_task_start.replace(hour=recur_task_start.hour, minute=recur_task_start.minute)
            recur_task_same_day_end = anti_task_start.replace(hour=recur_task_end.hour, minute=recur_task_end.minute)
            perfect_fit = anti_task_start == recur_task_same_day_start and anti_task_end == recur_task_same_day_end
            return perfect_fit

    def is_allowed_replace(self, old_task: Task, new_task: Task) -> bool:
        self.tasks.remove(old_task)
        is_allowed = self.is_allowed_entry(new_task)
        self.tasks.append(old_task)
        return is_allowed

    @staticmethod
    def get_task_date(task: Task) -> datetime:
        hour = int(task.get_start_time())
        minute = int(task.get_start_time() % 1.0 * 60)
        match task.get_task_type():
            case "Cancellation" | "Vist" | "Shopping" | "Appointment":
                time = datetime.fromisoformat(f"{task.get_date()}T{hour:02d}{minute:02d}00")
            case _:
                time = datetime.fromisoformat(f"{task.get_start_date()}T{hour:02d}{minute:02d}00")
        return time

    @staticmethod
    def get_task_end_time(task: Task) -> datetime:
        old_time = Schedule.get_task_date(task)

        added_hours = int(task.get_duration())
        added_minutes = int(task.get_duration() % 1.0 * 60)
        time_change = timedelta(hours=added_hours, minutes=added_minutes)
        return old_time + time_change

    @staticmethod
    def get_last_recurrence_end_time(task: RecurringTask):
        hour = int(task.get_start_time())
        minute = int(task.get_start_time() % 1.0 * 60)
        time = datetime.fromisoformat(f"{task.get_end_date():06d}T{hour:02d}{minute:02d}00")
        added_hours = int(task.get_duration())
        added_minutes = int(task.get_duration() % 1.0 * 60)
        time_change = timedelta(hours=added_hours, minutes=added_minutes)
        return time + time_change

def anti_task_equality(task1: AntiTask, task2: AntiTask):
    """
    Check if the anti-tasks are the same
    :param task1: AntiTask
    :param task2: AntiTask
    :return: True if AntiTask 1 and 2 are the same
    """
    return task1.get_duration() == task2.get_duration() and task1.get_name() == task2.get_name() and task1.get_start_time() == task2.get_start_time() and task1.get_date() ==  task2.get_date()

def get_date_times(task) -> list[(datetime, datetime)]:
    """
    Returns list with tuple(start time datetime, end time datetime) for every day task occurs
    :param task: Any type of task
    :return: list[(datetime, datetime)]
    """
    all_dates = []
    start = Schedule.get_task_date(task)
    end = Schedule.get_task_end_time(task)
    all_dates.append((start, end))
    if not type(task) is RecurringTask:
        return all_dates
    task: RecurringTask = task
    add_day = timedelta(days=task.get_frequency())
    while end <= Schedule.get_last_recurrence_end_time(task):
        start += add_day
        end += add_day
        all_dates.append((start, end))
    return all_dates


def is_datetime_pair_overlap(pair1, pair2) -> bool:
    """
    Checks if there is an overlap between one tuple(start datetime, end datetime) and another
    :param pair1: tuple(start datetime, end datetime)
    :param pair2: tuple(start datetime, end datetime)
    :return: True if there is an overlap
    """
    return pair1[0] < pair2[1] and pair2[0] < pair1[1]


def overlaps_of_datetimes(dates1: list[(datetime, datetime)], dates2: list[(datetime, datetime)]) -> tuple:
    """
    Returns a list of all start and end times of 2 list of start and end times
    :param dates1: must be list[(start datetime, end datetime)]
    :param dates2: must be list[(start datetime, end datetime)]
    :return: tuple(dates1 list[(start datetime, end datetime)]), dates2 list[(start datetime, end datetime)]))
    """
    overlap1, overlap2 = [], []
    for date1 in dates1:
        for date2 in dates2:
            if is_datetime_pair_overlap(date1, date2):
                overlap1.append(date1)
                overlap2.append(date2)
    return overlap1, overlap2

def get_task_overlaps(task1, task2):
    """
    Return tuple of 2 lists of start and end date times that overlap for each task
    :param task1:
    :param task2:
    :return: tuple(dates1 list[(start datetime, end datetime)]), dates2 list[(start datetime, end datetime)]))
    """
    task1_dates = get_date_times(task1)
    task2_dates = get_date_times(task2)
    return overlaps_of_datetimes(task1_dates, task2_dates)

def has_overlap(task1, task2):
    """
    True if there are any overlaps of time
    :param task1: any task type
    :param task2: any task type
    :return: True if there are any overlaps of time
    """
    return len(get_task_overlaps(task1, task2)[0]) > 0