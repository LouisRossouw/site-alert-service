import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Body

from lib.utils import read_json


load_dotenv()

# TODO; Clean this up


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
        def health():
            data_exists = os.path.exists(self.settings.service_path)
            data = {} if not data_exists else read_json(
                self.settings.service_path)
            return {"ok": True, **data}

        @self.app.get("/results")
        def get_last_results():
            # TODO; This will not work as results are saved individually for each task, i.e. sounds_limited_results.json
            # results_exists = os.path.exists(self.results_path)
            return []

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
            # TODO; Restart the service so the tasks can be re-created.
            # Prompt user to restart in the home-pie app.
            return self.settings.update_tasks(data)

        @self.app.get("/service/status")
        def _status_scheduler():
            return {"status": "TODO; Get Active jobs."}

        @self.app.post("/service/restart")
        def _restart_scheduler():
            return {"status": "TODO; Restart service"}

        @self.app.post("/service/shutdown")
        def _shutdown_scheduler():
            if self.scheduler:
                self.scheduler.scheduler.shutdown(wait=False)
                return {"status": "scheduler shutdown"}
            return {"error": "no scheduler attached"}

        @self.app.post("/service/pause")
        def _pause_job(job_id: str = Query(None, description="Job ID to pause")):
            if self.scheduler:
                if job_id:
                    self.scheduler.scheduler.pause_job(job_id)
                    return {"status": f"job {job_id} paused"}

                paused_jobs = []
                for job in self.scheduler.scheduler.get_jobs():
                    job.pause()
                    paused_jobs.append(job.id)

                return {"status": f"Paused {len(paused_jobs)} job(s)"}

            return {"error": "no scheduler attached"}

        @self.app.post("/service/resume")
        def _resume_job(job_id: str = Query(None, description="Job ID to resume")):
            if self.scheduler:
                if job_id:
                    self.scheduler.scheduler.resume_job(job_id)
                    return {"status": f"job {job_id} resumed"}

                resumed_jobs = []
                for job in self.scheduler.scheduler.get_jobs():
                    self.scheduler.scheduler.resume_job(job.id)
                    resumed_jobs.append(job.id)

                return {"status": f"Resumed {len(resumed_jobs)} job(s)"}

            return {"error": "no scheduler attached"}

    def run(self, host="0.0.0.0", port=5003):
        uvicorn.run(self.app, host=host, port=port)
