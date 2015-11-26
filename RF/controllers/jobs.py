from flask.ext.classy import FlaskView, route
from components import featureBroker
from flask import render_template, abort, request
from datetime import datetime

class JobController(FlaskView):
    route_base = '/jobs'
    scheduler = featureBroker.RequiredFeature('scheduler')

    @route('/')
    def jobs(self):
        """Renders the jobs page."""

        return render_template(
            'jobs.html',
            title='Jobs',
            year=datetime.now().year
        )
        
    @route('/scheduler/run', methods=['POST'])
    def runJob(self):
        """Removes a job from the scheduler."""
        try:
            job = self.scheduler.get_job(request.get_json(force=True)['job_id']);
            job.func(*job.args, **job.kwargs)
            return "{}", 200
        except:
            return abort(400)
        
    @route('/scheduler/remove', methods=['POST'])
    def removeJob(self):
        """Removes a job from the scheduler."""
        try:
            self.scheduler.remove_job(request.get_json(force=True)['job_id']);
            return "{}", 200
        except:
            return abort(400)
        
    @route('/scheduler/resume', methods=['POST'])
    def resumeJob(self):
        """Resumes a job in the scheduler."""
        try:
            self.scheduler.resume_job(request.get_json(force=True)['job_id']);
            return "{}", 200
        except:
            return abort(400)
        
    @route('/scheduler/pause', methods=['POST'])
    def pauseJob(self):
        """Pauses a job in the scheduler."""
        try:
            self.scheduler.pause_job(request.get_json(force=True)['job_id']);
            return "{}", 200
        except:
            return abort(400)

featureBroker.features.Provide('controller', JobController)