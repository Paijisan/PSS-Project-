from task import Task, AntiTask, RecurringTask, TransientTask
import datetime 
from schedule import InvalidTaskException
class Viewer:
    def display_menu(self, menu):
        print(menu)
    def show_day(self,dayTasks):
        for task in dayTasks :
            print(task.get_name(),":",task.get_start_time(),"-",task.get_start_time()+task.get_duration())
    def show_week(self,week):
        days = [[] for i in range(7)]
        for currentTask in week:
            if isinstance(currentTask, type(TransientTask(0,0,0,0,0))):
                dateInt = currentTask.get_date()
                date = datetime.datetime(int(dateInt/10000),int(dateInt/100)%100,dateInt%100)
                weekDay = date.weekday()
                days[weekDay].append(currentTask)
            elif isinstance(currentTask, type(RecurringTask(0,0,0,0,0,0,0))):
                frequency = currentTask.get_frequency()
                if frequency==1:
                    days[0].append(currentTask)
                    days[1].append(currentTask)
                    days[2].append(currentTask)
                    days[3].append(currentTask)
                    days[4].append(currentTask)
                    days[5].append(currentTask)
                    days[6].append(currentTask)
                if frequency==7:
                    dateInt = currentTask.get_start_date()
                    date = datetime.datetime(int(dateInt/10000),int(dateInt/100)%100,dateInt%100)
                    weekDay = date.weekday()
                    days[weekDay].append(currentTask)
            elif isinstance(currentTask, AntiTask()):
                print("Not implemented yet!!!")
            else:
                raise RuntimeError(type(currentTask),": is invalid task type")
        if len(week) > 0:
            for day in days:
                for currentTask in day:
                    if isinstance(currentTask, type(TransientTask(0,0,0,0,0))):
                        dateInt = currentTask.get_date()
                    elif isinstance(currentTask, type(RecurringTask(0,0,0,0,0,0,0))):
                        dateInt=currentTask.get_start_date()   
                    date = datetime.datetime(int(dateInt/10000),int(dateInt/100)%100,dateInt%100)
                    print(date)
                    print(currentTask.get_name(),":",currentTask.get_start_time(),"-",currentTask.get_start_time()+currentTask.get_duration())
       
    def show_month(self,month):
        print(month)
    def show_all(self, allTasks):
        print(allTasks)
    def show_task_values(self, taskValues):
        print(taskValues)