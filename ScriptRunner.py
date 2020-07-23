from _datetime import datetime
import time
import traceback
import requests
import json
import subprocess
import platform


def get_os_python_cmd():
    opr_sys = platform.system()
    if 'windows' in opr_sys.lower():
        cmd = "python"
    elif 'linux' in opr_sys.lower():
        cmd = "python3"
    else:
        cmd = "python"
    return cmd


def get_home_dir():
    opr_sys = platform.system()
    if 'windows' in opr_sys.lower():
        root_dir = "C:"
    elif 'linux' in opr_sys.lower():
        root_dir = "/home/zoeuser"
    else:
        root_dir = "C:"
    return root_dir


def notifier_script_run_monitor(msg, channel=None, weebhookUrl=None):
    # SENDS TO ZOEZIM WORKPACE
    webhook_url_default = 'https://hooks.slack.com/services/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'

    if channel is None:
        channel = "#script_run_monitor"
    else:
        channel = channel

    if weebhookUrl is None:
        weebhookUrl = webhook_url_default
    try:
        slack_data = {'text': msg,
                      "username": "HAL9000",
                      "icon_emoji": ":robot_face:",
                      "channel": channel}
        response = requests.post(weebhookUrl, data=json.dumps(slack_data), headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s' % (response.status_code, response.text))
    except:
        print("Error sending run notification")
        traceback.print_exc()


class jobDetails:
    def __init__(self, settingsDict: dict):
        """
        Can be used to run a specific python script at a specified path.
        Can also be used to run a specific shell command if supplied.
        If shell command is supplied, it will be run over the python script (using the runDirectory)
        :param scriptName:
        :param scriptLocation:
        :param startHour:
        :param startMinute:
        :param cmdLineArgs:
        :param jobName:
        :param intervalSeconds:
        :param runOnStart:
        :param startDelay:
        :param fullCommand:
        :param runDirectory:
        """

        # INTERVAL TIME IS GIVEN IN SECONDS
        self.jobName = settingsDict.get("JobName")
        self.enabled = settingsDict.get("Enabled")
        self.startHour = settingsDict.get("StartHour")
        self.startMinute = settingsDict.get("StartMinute")
        self.startSecond = settingsDict.get("StartSecond")
        self.intervalSeconds = settingsDict.get("InstervalSeconds")
        self.runOnStart = settingsDict.get("RunOnStart")
        self.fullCommand = settingsDict.get("FullCommand")
        self.runDirectory = settingsDict.get("RunDirectory")
        self.startDelay = settingsDict.get("StartDelay")

        if not self.startDelay:
            self.startDelay = 0

    def run_job(self):
        """
        Uses the subprocess method to run the file with the name specified.
        The call method is used on subprocess because it uses locking (Will wait for a job to completed before counting
        down to its next execution).
        This method is used by the schedule job method to run the actual file
        :return:
        """
        startMsg = f"LOG MSG: Starting job {self.jobName}"
        notifier_script_run_monitor(msg=startMsg)

        if self.fullCommand:
            print(f"LOG INFO: Full Command Supplied will be run.")
            try:
                subprocess.call(self.fullCommand, cwd=self.runDirectory, shell=True)
                endMsg = f"LOG SUCCESS: Job finished: {self.jobName}"
                print(endMsg)
                notifier_script_run_monitor(msg=endMsg)
            except:
                errorMsg = f"LOG ERROR: Failed to run file at {self.jobName}"
                print(errorMsg)
                notifier_script_run_monitor(errorMsg)
                traceback.print_exc()
            return

    def scheduleJob(self):
        if not self.enabled:
            print(f"JOB NAME: {self.jobName} not enabled. Will not be run")
            return
        """
        Handles the scheduling of the runs of the python scripts. Checks time every second, implements wait and intervals in running files
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

            if (timeNowHour == self.startHour and timeNowMin == self.startMinute and timeNowSec == 0) or self.runOnStart:
                if self.runOnStart == True:
                    print(f"Run on start flag set to {self.runOnStart}. Will run {self.jobName} for the first time")

                print(f"LOG INFO: Starting job with job name {self.jobName}")
                self.run_job()

                if self.intervalSeconds:
                    # WAITING FOR INTERVAL FIRST TIME
                    for t in range(self.intervalSeconds, 0, -1):
                        time.sleep(1)
                        print(
                            f"LOG INFO: Waiting for time interval to run next instance of {self.jobName}. Time interval is {self.intervalSeconds} seconds.Timer  currently at {t}")
                    while True:
                        # INNER LOOP FOR INTERVAL
                        self.run_job()
                        # WAITING FOR SUBSEQUENT INTERVAL
                        for t in range(self.intervalSeconds, 0, -1):
                            time.sleep(1)
                            print(
                                f"LOG INFO: Waiting for time interval to run next instance of {self.jobName}. Time interval is {self.intervalSeconds} seconds.Timer  currently at {t}")
            else:
                pass

            self.runOnStart = False
            print(f"LOG INFO: Will run next instance of {self.jobName} at next time {self.startHour}:{self.startMinute} hrs")
