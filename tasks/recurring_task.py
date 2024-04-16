from task import Task

class RecurringTask(Task):
    def __init__(self, name: str, task_type: str,
                 start_time: float, duration: float,
                 start_date: int, end_date: int,
                 frequency: int):
        super().__init__(name, task_type, start_time, duration)
        self._start_date = start_date
        self._end_date = end_date
        self._frequency = frequency

    def get_start_date(self) -> int:
        return self._start_date

    def get_end_date(self) -> int:
        return self._end_date

    def get_frequency(self) -> int:
        return self._frequency

