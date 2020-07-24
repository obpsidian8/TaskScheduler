from ScriptRunner import jobDetails
from multiprocessing import Pool
import json


def scheduleScripts(jobDetailsObject: jobDetails):
    """
    Takes a job detail object and calls the schedule job method on it. The schedule method of the class will take care of the rest
    :param jobDetailsObject:
    :return:
    """
    jobDetailsObject.scheduleJob()
    return


def scriptRunner():
    """
    Specify the parameters of the job you want to run.
    Run this file (not this example , but the actual job details files that follows this pattern) and the scripts specified will run on the pc its set up on
    :return:
    """
    jobSettings = json.load(open('JobSettings.json'))

    listOfJobObjects = [jobDetails(setting) for setting in jobSettings]

    processTotal = 0
    for job in jobSettings:
        if job.get("Enabled"):
            processTotal = processTotal + 1

    print(f"LOG INFO: Processing {processTotal} jobs")

    multiprocessPool = Pool(processTotal)

    with multiprocessPool as p:
        p.starmap(scheduleScripts, zip(listOfJobObjects, ))


if __name__ == "__main__":
    scriptRunner()
