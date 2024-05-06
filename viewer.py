from task import Task
import datetime 
class Viewer:
    def display_menu(self, menu):
        print(menu)
    def show_day(self,dayTasks):
        for task in dayTasks :
            print(task.get_name(),":",task.get_start_time(),"-",task.get_start_time()+task.get_duration())
    def show_week(self,week):
        days = [[] for i in range(7)]
        for task in week:
            taskType: str = task.get_task_type().lower()
            if taskType=="transient":
                dateInt = task.get_date()
                date = datetime.datetime(int(dateInt/10000),int(dateInt/100)%100,dateInt%100)
                weekDay = date.weekday()
                days[weekDay].append(task)
            elif taskType=="recurring":
                frequency = task.get_frequency()
                if frequency==1:
                    days[0].append(task)
                    days[1].append(task)
                    days[2].append(task)
                    days[3].append(task)
                    days[4].append(task)
                    days[5].append(task)
                    days[6].append(task)
                if frequency==7:
                    dateInt = task.get_start_date()
                    date = datetime.datetime(int(dateInt/10000),int(dateInt/100)%100,dateInt%100)
                    weekDay = date.weekday()
                    days[weekDay].append(task)
            elif taskType=="antitask":
                print("Not implemented yet!!!")
            else:
                raise Exception(taskType+" : incorrect task type")
        if len(week) > 0:
            for day in days:
                for task in day:
                    if taskType=="transient":
                        dateInt = task.get_date()
                    if taskType=="recurring":
                        dateInt=task.get_start_date()   
                    date = datetime.datetime(int(dateInt/10000),int(dateInt/100)%100,dateInt%100)
                    print(date)
                    print(task.get_name(),":",task.get_start_time(),"-",task.get_start_time()+task.get_duration())
       
    def show_month(self,month):
        print(month)
    def show_all(self, allTasks):
        print(allTasks)
    def show_task_values(self, taskValues):
        print(taskValues)