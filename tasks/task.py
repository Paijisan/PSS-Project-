class Task():
    def __init__(self, name: str, task_type: str,
                 start_time: float, duration: float):
        self._name = name
        self._task_type = task_type
        self._start_time = start_time
        self._duration = duration
    
    def get_name(self) -> str:
        return self._name

    def get_task_type(self) -> str:
        return self._task_type

    def get_start_time(self) -> float:
        return self._start_time

    def get_duration(self) -> float:
        return self._duration

    def to_json(self):
        pass

    def from_json(self, json: str):
        pass

    @staticmethod
    def time_as_str(time: float):
        pass

    @staticmethod
    def date_as_str(date: int):
        pass
