from ScriptRunner import jobDetails
from multiprocessing import Pool

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
    dealPriceChecker = jobDetails(jobName='TestJobCircle',scriptName='TimeWaster.py', scriptLocation='C:/pythonprojects/AdvancedPythonTopics', startHour=11, startMinute=28, intervalSeconds=10, cmdLineArgs="-s 20", runOnStart=True)

    listOfJobObjects = [dealPriceChecker]

    processTotal = len(listOfJobObjects)
    print(f"LOG INFO: Processing {processTotal} jobs")

    multiprocessPool = Pool(processTotal)

    with multiprocessPool as p:
        p.starmap(scheduleScripts, zip(listOfJobObjects, ))


if __name__ == "__main__":
    scriptRunner()
