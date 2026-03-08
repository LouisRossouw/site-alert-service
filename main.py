from api import CheckWebAPI
from settings import Settings
from scheduler import TaskScheduler

from runner import run

settings = Settings()
scheduler = TaskScheduler(settings, run)
server = CheckWebAPI(settings, scheduler=scheduler)


@server.app.on_event("startup")
def start_scheduler():
    print("Starting scheduler...")
    scheduler.start()


if __name__ == "__main__":
    server.run(host=settings.host, port=settings.port)
