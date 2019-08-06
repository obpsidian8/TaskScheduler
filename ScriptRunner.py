import subprocess
from _datetime import datetime
import time
from multiprocessing import Pool as ThreadPool
import traceback


class jobDetails:
    def __init__(self, jobName, scheduledStartTimeHour, scheduledStartTimeMinute, interval=None, runOnStart = False):
        self.jobName = jobName
        self.scheduledStartTimeHour = scheduledStartTimeHour
        self.scheduledStartTimeMinute = scheduledStartTimeMinute
        self.interval = interval
        self.runOnStart = runOnStart

        # self.scheduleJob()

    def jobExec(self):
        try:
            subprocess.call(self.jobName)
            print(f"LOG SUCCESS: Job finished: {self.jobName}")
        except:
            print(f"LOG ERROR: Failed to run file at {self.jobName}")
            traceback.print_exc()

    def scheduleJob(self):
        while True:
            time.sleep(0.5)
            print(f"LOG INFO: Checking current time.")
            timeNow = datetime.now().time()
            print(f"LOG INFO: Current time is {timeNow}")

            timeNowHour = timeNow.hour
            timeNowMin = timeNow.minute
            timeNowSec = timeNow.second

            if (timeNowHour == self.scheduledStartTimeHour and timeNowMin == self.scheduledStartTimeMinute and timeNowSec == 0) or self.runOnStart:
                if self.runOnStart ==True:
                    print(f"Run on start flag set to {self.runOnStart}. Will run {self.jobName} for the first time")

                print(f"LOG INFO: Starting job with job name {self.jobName}")
                self.jobExec()

                if self.interval:
                    print(f"LOG INFO: Waiting for time interval to run next instance of {self.jobName}.. Time interval is {self.interval} seconds")
                    time.sleep(self.interval)
                    while True:
                        # INNER LOOP FOR INTERVAL
                        self.jobExec()
                        # WAITING FOR INTERVAL
                        print(f"LOG INFO: Waiting for time interval to run next instance of {self.jobName}. Time interval is {self.interval} seconds")
                        time.sleep(self.interval)
            else:
                pass

            self.runOnStart = False
            print(f"LOG INFO: Will run next instance of {self.jobName} at next time {self.scheduledStartTimeHour}:{self.scheduledStartTimeMinute} hrs")


def scheduleScripts(jobDetailsObject):
    # IF USING A CLASS
    jobDetailsObject.scheduleJob()
    return


def scriptRunner():
    ListingsCheck = jobDetails("ListingsCheck.bat", 10, 37, interval=3600, runOnStart=True)
    RunUpdateRedmineIssues = jobDetails("RunUpdateRedmineIssues.bat", 15, 37)
    EmailAmazonInvoices = jobDetails("EmailAmazonInvoices.bat", 1, 30)
    LinkAmazonTracking = jobDetails("LinkAmazonTracking.bat", 4, 1)
    ScrapeNeweggGC = jobDetails("ScrapeNeweggGC.bat", 22, 3)
    CheckTrackingEmail = jobDetails("CheckTrackingEmail.bat", 6, 45)

    listOfJobObjects = [ListingsCheck,EmailAmazonInvoices, CheckTrackingEmail, LinkAmazonTracking, RunUpdateRedmineIssues, ScrapeNeweggGC]

    processTotal = len(listOfJobObjects)
    print(f"LOG INFO: Processing {processTotal} jobs")
    pool = ThreadPool(processTotal)
    pool.starmap(scheduleScripts, zip(listOfJobObjects, ))

    pool.close()
    pool.join()


if __name__ == "__main__":
    scriptRunner()
