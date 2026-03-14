import os
from lib.utils import read_json


def pause_schedule(scheduler, job_id):
    """ Pauses a specific job id in the scheduler. """

    if scheduler:
        if job_id:
            scheduler.scheduler.pause_job(job_id)
            return {"status": f"job {job_id} paused"}

        paused_jobs = []
        for job in scheduler.scheduler.get_jobs():
            paused_jobs.append(job.id)
            job.pause()

        return {"status": f"Paused {len(paused_jobs)} job(s)"}
    return {"error": "no scheduler attached"}


def resume_job(scheduler, job_id):
    """ Resumtes a specific job id in the scheduler. """

    if scheduler:
        if job_id:
            scheduler.scheduler.resume_job(job_id)
            return {"status": f"job {job_id} resumed"}

        resumed_jobs = []
        for job in scheduler.scheduler.get_jobs():
            scheduler.scheduler.resume_job(job.id)
            resumed_jobs.append(job.id)

        return {"status": f"Resumed {len(resumed_jobs)} job(s)"}

    return {"error": "no scheduler attached"}


def shutdown_scheduler(scheduler):
    """ Stops the schduleer, can't be restarted onces stopped. """

    if scheduler:
        scheduler.scheduler.shutdown(wait=False)
        return {"status": "scheduler shutdown"}
    return {"error": "no scheduler attached"}


def restart_scheduler(scheduler):
    return {"status": "TODO; Restart service"}


def status_scheduler():
    return {"status": "TODO; Get Active jobs."}


def update_tasks(settings, data):
    # TODO; Restart the service so the tasks can be re-created.
    # Prompt user to restart in the home-pie app.
    return settings.update_tasks(data)


def get_last_results():
    # TODO; This will not work as results are saved individually for each task, i.e. sounds_limited_results.json
    # results_exists = os.path.exists(self.results_path)
    return []


def health(settings):
    """ Returns the health of the service. """

    data_exists = os.path.exists(settings.service_path)
    data = {} if not data_exists else read_json(settings.service_path)
    return {"ok": True, **data}
