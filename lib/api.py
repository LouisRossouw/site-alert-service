
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Body

from lib import api_utils as api

load_dotenv()


class CheckWebAPI:
    def __init__(self, settings, scheduler=None):

        self.app = FastAPI()

        self.settings = settings
        self.scheduler = scheduler

        self._routes()

    def _routes(self):
        @self.app.get("/")
        def root():
            return {"info": f"{self.settings.name}"}

        @self.app.get("/health")
        def _health():
            return api.health(self.settings)

        @self.app.get("/results")
        def _get_last_results():
            return api.get_last_results()

        @self.app.get("/logs")
        def _get_logs(lines: int = 20):
            return {"logs": self.settings.get_logs(lines)}

        @self.app.get("/config")
        def _get_config():
            return self.settings.get_config()

        @self.app.patch("/config")
        def _patch_config(data: dict = Body(...)):
            return self.settings.update_config(data)

        @self.app.get("/tasks")
        def _get_tasks():
            return self.settings.get_tasks()

        @self.app.patch("/tasks")
        def _update_tasks(data: list = Body(...)):
            return api.update_tasks(self.settings, data)

        @self.app.get("/service/status")
        def _status_scheduler():
            return api.status_scheduler()

        @self.app.post("/service/restart")
        def _restart_scheduler():
            return api.restart_scheduler()

        @self.app.post("/service/shutdown")
        def _shutdown_scheduler():
            return api.resume_job(self.scheduler)

        @self.app.post("/service/pause")
        def _pause_job(job_id: str = Query(None, description="Job ID to pause")):
            return api.pause_schedule(self.scheduler, job_id)

        @self.app.post("/service/resume")
        def _resume_job(job_id: str = Query(None, description="Job ID to resume")):
            return api.resume_job(self.scheduler, job_id)

    def run(self, host="0.0.0.0", port=5003):
        uvicorn.run(self.app, host=host, port=port)
