class Viewer:
    
    def display_menu(self, menu):
        print(menu)
    def show_day(self,dayTasks):
        for task in dayTasks :
            print(tasktask.get_name(),":",task.get_start_time(),"-",task.get_start_time()+task.get_duration())
    def show_week(self,week):
        days = list[list[task]] = [[]]
       for task in week:
            choice: str = task.get_task_type().lower()
            if choice=="transient":
                dateInt = task.get_date()
                date = datetime.datetime(dateInt/1000,(dateInt/100)%100,dateInt%100)
                weekDay = date.weekday()
                days[weekDay].add(task)
            if choice=="recurring":
                frequency = task.get_frequency()
                if frequency==1:
                    days[0].add(task)
                    days[1].add(task)
                    days[2].add(task)
                    days[3].add(task)
                    days[4].add(task)
                    days[5].add(task)
                    days[6].add(task)
                if frequency==7:
                    originalDate = task.get_first_date():
                    date = datetime.datetime(dateInt/1000,(dateInt/100)%100,dateInt%100)
                    weekDay = date.weekday()
                    days[weekDay].add(task)
        for day in days:
            for task in day:
                print(task.get_name(),":",task.get_start_time(),"-",task.get_start_time()+task.get_duration())
       
    def show_month(self,month):
        print(month)
    def show_all(self, allTasks):
        print(allTasks)
    def show_task_values(self, taskValues):
        print(taskValues)