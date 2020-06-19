import subprocess
from _datetime import datetime
import time
from multiprocessing import Pool as ThreadPool
import traceback


class jobDetails:
    """
    Takes in the init file , the name of the windows batch file to be run as well as the time and interval to run the batch files
    """
    def __init__(self, jobName, scheduledStartTimeHour, scheduledStartTimeMinute=0, interval=None, runOnStart=False,
                 startDelay=None):
        # INTERVAL TIME IS GIVEN IN SECONDS
        self.jobName = jobName
        self.scheduledStartTimeHour = scheduledStartTimeHour
        self.scheduledStartTimeMinute = scheduledStartTimeMinute
        self.interval = interval
        self.runOnStart = runOnStart

        if not startDelay:
            startDelay = 0

        self.startDelay = startDelay

    def run_job(self):
        """
        Uses the subprocess method to run the batch file with the job name specified.
        The call method is used on subprocess because it uses locking (Will wait for a job to completed before counting 
        down to its next execution).
        This methond is used by the schedule job method to run the actual file
        :return: 
        """
        startMsg = f"LOG MSG: Starting job {self.jobName}"
        notifier_script_run_monitor(msg=startMsg)
        try:
            subprocess.call(self.jobName)
            endMsg = f"LOG SUCCESS: Job finished: {self.jobName}"
            print(endMsg)
            notifier_script_run_monitor(msg=endMsg)
        except:
            errorMsg = f"LOG ERROR: Failed to run file at {self.jobName}"
            print(errorMsg)
            notifier_script_run_monitor(errorMsg)
            traceback.print_exc()

    def scheduleJob(self):
        """
        Handles the scheduling of the runs of the batch files. Checks time every second, implements wait and intervals in running files
        :return: 
        """
        time.sleep(self.startDelay)
        while True:
            time.sleep(1)
            print(f"LOG INFO: Checking current time.")
            timeNow = datetime.now().time()
            print(f"LOG INFO: Current time is {timeNow}")

            timeNowHour = timeNow.hour
            timeNowMin = timeNow.minute
            timeNowSec = timeNow.second

            if (
                    timeNowHour == self.scheduledStartTimeHour and timeNowMin == self.scheduledStartTimeMinute and timeNowSec == 0) or self.runOnStart:
                if self.runOnStart == True:
                    print(f"Run on start flag set to {self.runOnStart}. Will run {self.jobName} for the first time")

                print(f"LOG INFO: Starting job with job name {self.jobName}")
                self.run_job()

                if self.interval:
                    # WAITING FOR INTERVAL FIRST TIME
                    for t in range(self.interval, 0, -1):
                        time.sleep(1)
                        print(
                            f"LOG INFO: Waiting for time interval to run next instance of {self.jobName}. Time interval is {self.interval} seconds.Timer  currently at {t}")
                    while True:
                        # INNER LOOP FOR INTERVAL
                        self.run_job()
                        # WAITING FOR SUBSEQUENT INTERVAL
                        for t in range(self.interval, 0, -1):
                            time.sleep(1)
                            print(
                                f"LOG INFO: Waiting for time interval to run next instance of {self.jobName}. Time interval is {self.interval} seconds.Timer  currently at {t}")
            else:
                pass

            self.runOnStart = False
            print(
                f"LOG INFO: Will run next instance of {self.jobName} at next time {self.scheduledStartTimeHour}:{self.scheduledStartTimeMinute} hrs")


def scheduleScripts(jobDetailsObject: jobDetails):
    """
    Takes a "jobDetails" object and calls the schedulejob method on that object
    :param jobDetailsObject: 
    :return: None
    """
    jobDetailsObject.scheduleJob()
    return


def scriptRunner():
    manual_pricing_slack = jobDetails("manual_pricing_slack.bat", 6, 0, interval=2, runOnStart=True)
    DealPostSlack = jobDetails("DealPostSlack.bat", 6, 0, interval=30, runOnStart=True)
    upload_price_changes = jobDetails("manualPriceInformed.bat", 15, 30, interval=20, runOnStart=True)
    UseditemReporterSlackListener = jobDetails("UseditemReporterSlackListener.bat", 6, 30, interval=2, runOnStart=True)

    ZoeSerialToMondayUpload = jobDetails("ZoeSerialToMondayUpload.bat", 10, 0, interval=1800, runOnStart=False)
    CardBalanceUpdater = jobDetails("Run_Card_Balance_Scraper.bat", 6, 30, runOnStart=False)
    ZoePurchaseOrderToMondayUpload = jobDetails("ZoePurchaseOrderToMondayUpload.bat", 23, 0, runOnStart=False)
    ZoeProxyStatusUpdater = jobDetails("ZoeProxyStatusUpdater.bat", 4, 30, runOnStart=False)
    ZoeUploadTrackingStatusUpdater = jobDetails("ZoeUploadTrackingStatusUpdater.bat", 19, 0, runOnStart=False)

    listOfJobObjects = [
        manual_pricing_slack,
        upload_price_changes,
        UseditemReporterSlackListener,
        CardBalanceUpdater,
        ZoeSerialToMondayUpload,
        ZoePurchaseOrderToMondayUpload,
        ZoeProxyStatusUpdater,
        ZoeUploadTrackingStatusUpdater,
        DealPostSlack
    ]

    processTotal = len(listOfJobObjects)
    print(f"LOG INFO: Processing {processTotal} jobs")

    multiprocessPool = Pool(processTotal)
    with multiprocessPool as p:
        p.starmap(scheduleScripts, zip(listOfJobObjects, ))


if __name__ == "__main__":
    scriptRunner()
