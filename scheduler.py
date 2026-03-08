from apscheduler.schedulers.background import BackgroundScheduler


class TaskScheduler:

    def __init__(self, settings, run_task):

        self.settings = settings
        self.run_task = run_task
        self.scheduler = BackgroundScheduler()

    def start(self):
        web_tasks = self.settings.get_tasks()

        for web_task in web_tasks:
            name = web_task["name"]
            frequency = web_task["frequeny"]
            interval = web_task["interval"]

            if frequency == "minute":
                self.scheduler.add_job(
                    self.run_task,
                    "interval",
                    minutes=interval,
                    args=[self.settings, web_task],
                    id=name
                )
            elif frequency == "second":
                self.scheduler.add_job(
                    self.run_task,
                    "interval",
                    seconds=interval,
                    args=[self.settings, web_task],
                    id=name
                )
            elif frequency == "hour":
                self.scheduler.add_job(
                    self.run_task,
                    "interval",
                    hours=interval,
                    args=[self.settings, web_task],
                    id=name
                )

            elif frequency == "day":
                self.scheduler.add_job(
                    self.run_task,
                    "interval",
                    days=interval,
                    args=[self.settings, web_task],
                    id=name
                )

        self.scheduler.start()
