from lib.settings import Settings
from lib.api import CheckWebAPI
from lib.scheduler import TaskScheduler
from lib.runner import run

settings = Settings()
scheduler = TaskScheduler(settings, run)
server = CheckWebAPI(settings, scheduler=scheduler)


@server.app.on_event("startup")
def start_scheduler():
    print("Starting scheduler...")
    scheduler.start()


if __name__ == "__main__":
    server.run(host=settings.host, port=settings.port)
