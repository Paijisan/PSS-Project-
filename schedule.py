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
        try:
            new_task: Task = Schedule.create_task(j["Name"], j["Type"], j["StartTime"], j["Duration"], j.get("StartDate", j.get("Date", None)),
                                              j.get("EndDate", None), j.get("Frequency", None))
        except Exception:
            raise InvalidJson()
        return new_task

    def delete_task(self, task: Task) -> bool:
        """
        Deletes task from schedule, may raise AntiTaskRemoveException
        :param task: Task to delete
        :return: True if delete is success
        """
        if task in self.tasks:
            if type(task) is AntiTask:
                overlapped_tasks = []
                for stored_task in self.tasks:
                    # Ignore self in list
                    if not anti_task_equality(stored_task, task):
                        # Check all overlaps
                        if has_overlap(task, stored_task):
                            overlapped_tasks.append(stored_task)

                # Only 1 task should overlap anti-task, the RecurringTask it cancels
                if len(overlapped_tasks) > 1:
                    raise AntiTaskRemoveException(overlapped_tasks[0].get_name(), overlapped_tasks[1].get_name())
            else:
                self.tasks.remove(task)
                return True
        return False

    def add_task(self, task: Task) -> bool:
        """
        Adds task to schedule, raises Exceptions if task is not allowed
        :param task: Task to add
        :return: True if add successful
        """
        if self.is_allowed_entry(task):
            self.tasks.append(task)
            return True
        return False

    def add_tasks(self, tasks: list[Task]) -> bool:
        """
        Adds a list of Tasks, raises Exception on first non-allowed task
        Deletes all added task if 1 task in list fails
        :param tasks:
        :return:
        """
        # Verify all tasks are valid
        temp_schedule = Schedule()
        for task in tasks:
            if not temp_schedule.add_task(task):
                return False
        success = 0
        def remove_tasks():
            """
            Only removes tasks there was a single failure
            """
            if success != len(temp_schedule.tasks):
                for task in temp_schedule.tasks:
                    if task in self.tasks:
                        self.tasks.remove(task)
                return False
            return True
        try:
            # Verify all tasks are allowed in current schedule
            for task in temp_schedule.tasks:
                success += self.add_task(task)
        except Exception as ex:
            # If a task fails to add, remove all other added tasks before re-raising exception
            remove_tasks()
            raise ex
        else:  # No exception occured
            return remove_tasks()

        return True

    def edit_task(self, old_task: Task, new_task: Task) -> bool:
        if self.delete_task(old_task):
            try:
                if not self.add_task(new_task):
                    self.add_task(old_task)
                    return False
            except Exception as ex:
                # Add back unedited task on failure
                self.add_task(old_task)
                raise ex

        # Could not delete old task (Does not exist?)
        else:
            return False
        return True

    def get_task(self, task_name: str) -> Task:
        """
        Retrieve task by name
        :param task_name: A tasks string name
        :return: Task
        """
        for task in self.tasks:
            if task.get_name() == task_name:
                return task

    def write_file(self, file_name: str) -> bool:
        """
        Write to save file, may cause file write Exceptions
        :param file_name: filename or full path
        :return: True on success
        """
        all_tasks: list = []
        for task in self.tasks:
            all_tasks.append(json.loads(task.to_json()))

        with open(file_name, "w") as out_file:
            out_file.write(json.dumps(all_tasks, indent=True))
        return True

    def read_file(self, file_name: str) -> bool:
        """
        Adds given filename to schedule or raises error
        :param file_name: filename or full path
        :return: True on success
        """

        with open(file_name, "r") as in_file:
            j = json.load(in_file)
            all_tasks = [Schedule.create_task_from_json(str(task)) for task in j]
            self.add_tasks(all_tasks)
        return True

    def get_day_tasks(self, date: int) -> list[Task]:
        """
        Gets all Tasks for given date
        :param date: iso format date of YYYYMMDD
        :return: list[Task]
        """
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
        """
        Gets all Tasks for given date
        :param date: iso format date of YYYYMMDD
        :return: list[Task]
        """
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
        """
        Gets all Tasks for given date
        :param date: iso format date of YYYYMMDD
        :return: list[Task]
        """
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

    def is_name_unique(self, task: Task) -> bool:
        """
        Bool to test if Task name is unique
        :param task: Task to test
        :return: True if name is unique
        """
        for old_task in self.tasks:
            if task.get_name() == old_task.get_name():
                return False
        return True

    def is_allowed_entry(self, new_task: Task) -> bool:
        """
        Will return true if task is allowed, false or Raise Exception if not allowed
        :param new_task: Task to test
        :return: True for allowed, Exception may occur on not allowed
        """
        if not self.is_name_unique(new_task):
            raise TaskNameNotUniqueException(new_task.get_name())

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
                if is_allowed:
                    return True
                else:
                    raise TaskOverlapException(new_task.get_name())

        # No overlap found!
        # A non-overlapping AntiTask is not allowed
        if type(new_task) is AntiTask:
            raise InvalidTaskException()
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
            anti_tasks = (_task for _task in self.tasks if type(_task) is AntiTask)
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
    def is_anti_task_of_task(anti_task: AntiTask, task: RecurringTask) -> bool:
        """
        Check if anti task belongs to Recurring Task
        :param anti_task: AntiTask
        :param task: RecurringTask
        :return: True if AntiTask belongs to RecurringTask
        """
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
        """
        Check if task is allowed to replace another task, raises exception on failure
        :param old_task: Task currently in schedule
        :param new_task: Task replacing old task in schedule
        :return: True if new Task can replace old task
        """
        if old_task in self.tasks:
            self.tasks.remove(old_task)
            try:
                is_allowed = self.is_allowed_entry(new_task)
            except Exception as ex:
                # Add back old task on failure
                self.tasks.append(old_task)
                raise ex
            self.tasks.append(old_task)
        return is_allowed

    @staticmethod
    def get_task_date(task: Task) -> datetime:
        """
        Gets date no matter the task type, with task time attached
        :param task: Task
        :return: datetime of with hour and minute of first occurence of Task
        """
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
        """
        Get datetime with hour and minute at the end of a task
        :param task: Task
        :return: datetime with hours and minute of end of task
        """
        old_time = Schedule.get_task_date(task)

        added_hours = int(task.get_duration())
        added_minutes = int(task.get_duration() % 1.0 * 60)
        time_change = timedelta(hours=added_hours, minutes=added_minutes)
        return old_time + time_change

    @staticmethod
    def get_last_recurrence_end_time(task: RecurringTask) -> datetime:
        """
        Gets datetime of the last date in RecurringTask with end time
        :param task: RecurringTask
        :return: datetime of end time of RecurringTask
        """
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


class TaskNameNotUniqueException(Exception):
    """
    Task name already exists in schedule, "CS3560-L15-The-Project (1).pdf" page 15
    """
    def __init__(self, name, *args):
        super().__init__(args)
        self.name = name

    def __str__(self):
        return f"Task {self.name} already exists, choose a unique name"


class AntiTaskRemoveException(Exception):
    """
    Removal of AntiTask would cause conflict in overlapping Tasks, "CS3560-L15-The-Project (1).pdf" page 17
    """
    def __init__(self, name1, name2, *args):
        super().__init__(args)
        self.name1 = name1
        self.name2 = name2

    def __str__(self):
        return f"AntiTask removal error, Task:{self.name1} and Task:{self.name2} rely on AntiTask"


class TaskOverlapException(Exception):
    """
    Newly requested Task overlaps with older task
    """
    def __init__(self, name, *args):
        super().__init__(args)
        self.name = name

    def __str__(self):
        return f"Can not add task, overlap with task {self.name}"


class InvalidTaskException(Exception):
    """
    Task does not have valid fields
    """
    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return f"Invalid task provided"


class InvalidJson(Exception):
    """
    Saved file is invalid, "CS3560-L15-The-Project (1).pdf" page 20
    """
    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return f"JSON save file has invalid syntax"
