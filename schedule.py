from tasks.task import Task


class Schedule:
    def __init__(self):
        self.tasks = []

    def create_task(self, task_name: str, task_type: str, start_time: float, duration: float, start_date: int,
                    end_date: int = None, frequency: int = None, target_task: int = None) -> Task:
        """
        Creates a task to add to plan
        :param task_name:
        :param task_type:
        :param start_time:
        :param duration:
        :param start_date:
        :param end_date:
        :param frequency:
        :param target_task:
        :return:
        """
        pass

    @staticmethod
    def create_task_from_json(json: str) -> Task:
        """
        Creates a task from given json
        :param json:
        :return:
        """
        pass

    def delete_task(self, task: Task) -> bool:
        pass

    def add_task(self, task: Task) -> bool:
        pass

    def add_tasks(self, tasks: list[Task]) -> bool:
        pass

    def edit_task(self, old_task: Task, new_task: Task) -> bool:
        pass

    def get_task(self, task_name: str) -> Task:
        pass

    def write_file(self, file_name: str) -> bool:
        pass

    def read_file(self, file_name: str) -> bool:
        pass

    def get_day_tasks(self, date: int) -> list[Task]:
        pass

    def get_week_tasks(self, date: int) -> list[Task]:
        pass

    def get_month_tasks(self, date: int) -> list[Task]:
        pass

    def is_allowed_entry(self, new_task: Task) -> bool:
        pass

    def is_allowed_replace(self, old_task: Task, new_task: Task) -> bool:
        pass
