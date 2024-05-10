from task import Task, AntiTask, RecurringTask, TransientTask
import datetime 
from schedule import InvalidTaskException
import calendar
from datetime import date
from datetime import timedelta
class Viewer:
    def display_menu(self, menu):
        print(menu)
    def show_day(self,dayTasks):
        antitasks = []
        for task in dayTasks:
            if isinstance(task, type(AntiTask(0,0,0,0,0))):
                antitasks.append(task)
        for antitask in antitasks:
            for task in dayTasks:
                if antitask.get_start_time()==task.get_start_time():
                    if antitask.get_target_task()==task.get_name():
                        dayTasks.remove(task)
        for task in dayTasks :
            print(task.get_name(),":",task.get_start_time(),"-",task.get_start_time()+task.get_duration())
    def show_week(self,week,dateInt):
        days = [[] for i in range(7)]
        date=datetime.date(int(dateInt/10000),int(dateInt/100)%100,dateInt%100)
        date=date-timedelta(days=date.weekday())
        antitasks = []
        for currentTask in week:
            if isinstance(currentTask, type(TransientTask(0,0,0,0,0))):
                currentdateInt = currentTask.get_date()
                currentdate = datetime.date(int(currentdateInt/10000),int(currentdateInt/100)%100,currentdateInt%100)
                weekDay = currentdate.weekday()
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
                    currentdateInt = currentTask.get_start_date()
                    currentdate = datetime.date(int(currentdateInt/10000),int(currentdateInt/100)%100,currentdateInt%100)
                    weekDay = currentdate.weekday()
                    days[weekDay].append(currentTask)
            if isinstance(currentTask, type(AntiTask(0,0,0,0,0))):
                antitasks.append(currentTask)
        for antitask in antitasks:
            antiDateInt=antitask.get_date()
            weekday=datetime.date(int(antiDateInt/10000),int(antiDateInt/100)%100,antiDateInt%100).weekday()
            for task in days[weekday]:
                if (task.get_name()==antitask.get_target_task() and task.get_start_time()==antitask.get_start_time()):
                    days[weekday].remove(task)
        if len(week) > 0:
            for day in days:
                print(date)
                date=date+timedelta(days=1)
                for currentTask in day:
                    print(currentTask.get_name(),":",currentTask.get_start_time(),"-",currentTask.get_start_time()+currentTask.get_duration())
       
    def show_month(self,month,dateInt):
        monthCalendar = calendar.monthcalendar(int(dateInt/10000),int(dateInt/100)%100)
        taskCalendar = [[[] for i in range(7)] for i in range(len(monthCalendar))]
        antitasks = []
        for currentTask in month:
            if isinstance(currentTask, type(TransientTask(0,0,0,0,0))):
                currentDay=currentTask.get_date()%100
                i=0
                for week in monthCalendar:
                    j=0
                    for day in week:
                        if (currentDay==day):
                            taskCalendar[i][j].append(currentTask)
                        j=j+1
                    i=i+1
            if isinstance(currentTask, type(RecurringTask(0,0,0,0,0,0,0))):
                frequency = currentTask.get_frequency()
                i=0
                if frequency==1:
                    for week in monthCalendar:
                        j=0
                        for day in week:
                            if (day!=0):
                                taskCalendar[i][j].append(currentTask)
                            j=j+1
                        i=i+1
                if frequency==7:
                    currentDateInt=currentTask.get_start_date()
                    dayOfWeek=datetime.date(int(dateInt/10000),int(dateInt/100)%100,dateInt%100).weekday()
                    i=0
                    for week in monthCalendar:
                        taskCalendar[i][dayOfWeek].append(currentTask)
                        i=i+1
            if isinstance(currentTask, type(AntiTask(0,0,0,0,0))):
                antitasks.append(currentTask)
        for antitask in antitasks:
            currentDay=currentTask.get_date()%100
            i=0
            for week in monthCalendar:
                j=0
                for day in week:
                    if (currentDay==day):
                        tasks = taskCalendar[i][j]
                        for task in tasks:
                            if task.get_name()==antitask.get_target_task():
                                taskCalendar[i][j].remove(task)
                    j=j+1
                i=i+1
        i=0
        for week in taskCalendar:
            j=0
            for day in week:
                if (monthCalendar[i][j]!=0):
                    print(int(dateInt/10000),"-",int(dateInt/100)%100,"-",monthCalendar[i][j])
                    for currentTask in day:
                        print(currentTask.get_name(),":",currentTask.get_start_time(),"-",currentTask.get_start_time()+currentTask.get_duration())
                j=j+1
            i=i+1
    def show_all(self, allTasks):
        allTasks=allTasks.sort()
        
    def show_task_values(self, taskValues):
        for taskValue in taskValues:
            print(taskValue)
    def removeTasksTargetedByAntitask(self, tasks):
        antitasks = []
        for currentTask in tasks:
            if isinstance(currentTask, type(AntiTask(0,0,0,0,0))):
                antitasks.append(currentTask)
        for antitask in antitasks:
            taskNameToDelete=antitask.get_target_task()
            for task in tasks:
                if (task.get_name()==taskNameToDelete):
                    tasks.remove(task)
        return tasks