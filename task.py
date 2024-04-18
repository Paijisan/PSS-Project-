import json
import datetime

class Task():
    def __init__(self, name: str, task_type: str,
                 start_time: float, duration: float):
        self._name = name
        self._task_type = task_type
        self._start_time = start_time
        self._duration = duration
    
    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> bool:
        self._name = name
        return True;

    def get_task_type(self) -> str:
        return self._task_type

    def set_task_type(self, tast_type: str) -> bool:
        self._task_type = tast_type
        return True

    def get_start_time(self) -> float:
        return self._start_time

    def set_start_time(self, start_time: float) -> bool:
        self._start_time = start_time
        return True

    def get_duration(self) -> float:
        return self._duration

    def set_duration(self, duration: float) -> bool:
        self._duration = duration
        return True

    def to_json(self) -> str:
        j: dict = {
            'Name': self._name,
            'Type': self._task_type,
            'StartTime': self._start_time,
            'Duration': self._duration,
        }
        return json.dumps(j)

    @staticmethod
    def time_as_str(time: float) -> str:
        '''
        Convert a positive number, that is a multiple of 0.25
        and in the range of 0 (midnight) to 23.75 (11:45 pm) to
        a pretty string representation
        :param time: number to be converted
        :return: a pretty string representation of the time
        '''
        hours = int(time)
        mins = int((time - hours) * 60)
        hm = datetime.time(hours, mins)
        return hm.strftime("%I:%M %p")

    @staticmethod
    def date_as_str(date: int) -> str:
        '''
        Convert an integer in the form YYYYMMDD
        to ISO format
        :param date: integer to be converted
        :return: ISO format string representation of integer
        '''
        return datetime.datetime.strptime(str(date), "%Y%m%d").isoformat()

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

    def set_start_date(self, start_date: int) -> bool:
        self._start_date = start_date
        return True

    def get_end_date(self) -> int:
        return self._end_date

    def set_end_date(self, end_date: int) -> bool:
        self._end_date = end_date
        return True

    def get_frequency(self) -> int:
        return self._frequency

    def set_frequency(self, frequency: int) -> bool:
        self._frequency = frequency
        return True

    def to_json(self) -> str:
        j: dict = {
            'Name': self._name,
            'Type': self._task_type,
            'StartDate': self._start_date,
            'StartTime': self._start_time,
            'Duration': self._duration,
            'EndDate': self._end_date,
            'Frequency': self._frequency,
        }
        return json.dumps(j)

    @staticmethod
    def frequency_as_str(frequency: int) -> str:
        """
        Convert the frequency integer to its string representation
        :param frequency: integer to convert
        :return: frequency in string representation
        """        
        match frequency:
            case 1:
                return 'Daily'
            case 7:
                return 'Weekly'
            case _:
                return 'invalid_frequency'

    
class TransientTask(Task):
    def __init__(self, name: str, task_type: str,
                 start_time: float, duration: float,
                 date: int):
        super().__init__(name, task_type, start_time, duration)
        self._date = date
    
    def get_date(self) -> int:
        return self._date
    
    def set_date(self, date: int) -> bool:
        self._date = date
        return True

    def to_json(self) -> str:
        j: dict = {
            'Name': self._name,
            'Type': self._task_type,
            'Date': self._date,
            'StartTime': self._start_time,
            'Duration': self._duration,
        }
        return json.dumps(j)

class AntiTask(TransientTask):
    def __init__(self, name: str, task_type: str,
                 start_time: float, duration: float,
                 date: int, target_task: RecurringTask | None = None):
        super().__init__(name, task_type, start_time, duration, date)
        self._target_task = target_task

    def get_target_task(self) -> RecurringTask | None:
        return self._target_task
