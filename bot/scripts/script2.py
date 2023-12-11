import sys
from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime

sleep_time = int(sys.argv[1])


def job():
    print("SCRIPT 2 \n I'm working...")


# Create a BlockingScheduler instance
scheduler = BlockingScheduler()

# Add the job to the scheduler
scheduler.add_job(job, "interval", seconds=sleep_time)

# Modify the job to start immediately
for job in scheduler.get_jobs():
   job.modify(next_run_time=datetime.now())

# Start the scheduler
scheduler.start()