from ETS2LA.backend.classes import Job, CancelledJob, FinishedJob, Refuel
import ETS2LA.modules.TruckSimAPI.main as API
import ETS2LA.backend.controls as controls
import ETS2LA.backend.backend as backend
import ETS2LA.networking.cloud as cloud
import threading
import logging
import time

API.Initialize()
API.CHECK_EVENTS = True # DO NOT DO THIS ANYWHERE ELSE!!! PLEASE USE THE EVENTS SYSTEM INSTEAD!!!
    
# Events
class ToggleSteering():
    steering = True
    def ToggleSteering(self):
        self.steering = not self.steering
        backend.CallEvent('ToggleSteering', self.steering, {})
    def __init__(self):
        controls.RegisterKeybind('ToggleSteering', lambda self=self: self.ToggleSteering(), defaultButtonIndex="n")
        
last_started_job = None
        
class JobStarted():
    def JobStarted(self, data):
        global last_started_job
        job = Job()
        job.fromAPIData(data)
        backend.CallEvent('JobStarted', job, {})
        logging.info("Triggered event: JobStarted")
        cloud.StartedJob(job)
        last_started_job = job
    def __init__(self):
        API.listen('jobStarted', self.JobStarted)
        
class JobFinished():
    def JobFinished(self, data):
        job = FinishedJob()
        job.fromAPIData(data)
        if job.cargo_id == '' and job.cargo == '' and job.unit_count == 0 and job.unit_mass == 0 and last_started_job != None:
            job.cargo_id = last_started_job.cargo_id
            job.cargo = last_started_job.cargo
            job.unit_count = last_started_job.unit_count
            job.unit_mass = last_started_job.unit_mass
        backend.CallEvent('JobFinished', job, {})
        logging.info("Triggered event: JobFinished")
        cloud.FinishedJob(job)
    def __init__(self):
        API.listen('jobFinished', self.JobFinished)
        
class JobDelivered():
    def JobDelivered(self, data):
        job = FinishedJob()
        job.fromAPIData(data)
        backend.CallEvent('JobDelivered', job, {})
        logging.info("Triggered event: JobDelivered")
    def __init__(self):
        API.listen('jobDelivered', self.JobDelivered)
        
class JobCancelled():
    def JobCancelled(self, data):
        job = CancelledJob()
        job.fromAPIData(data)
        backend.CallEvent('JobCancelled', job, {})
        logging.info("Triggered event: JobCancelled")
        cloud.CancelledJob(job)
    def __init__(self):
        API.listen('jobCancelled', self.JobCancelled)
        
class RefuelStarted():
    def RefuelStarted(self, data):
        refuel = Refuel()
        refuel.fromAPIData(data)
        backend.CallEvent('RefuelStarted', refuel, {})
        logging.info("Triggered event: RefuelStarted")
    def __init__(self):
        API.listen('refuelStarted', self.RefuelStarted)
        
class RefuelPayed():
    def RefuelPayed(self, data):
        refuel = Refuel()
        refuel.fromAPIData(data)
        backend.CallEvent('RefuelPayed', refuel, {})
        logging.info("Triggered event: RefuelPayed")
    def __init__(self):
        API.listen('refuelPayed', self.RefuelPayed)
        
# Start monitoring
def ApiThread():
    while True:
        API.run()
        time.sleep(0.1)

def run():
    ToggleSteering()
    JobStarted()
    JobFinished()
    JobDelivered()
    JobCancelled()
    RefuelStarted()
    RefuelPayed()
    
    threading.Thread(target=ApiThread, daemon=True).start()
    logging.info("Event monitor started.")