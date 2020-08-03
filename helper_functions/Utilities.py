import json
from helper_functions.DatabaseHandler import JobsettingsDatabaseHandler


def convertDatabaseResultstoJson(record: tuple):
    settingDict = {}

    settingDict['JobName'] = record[0]
    settingDict['FullCommand'] = record[1]

    if record[2] == 'True':
        settingDict['Enabled'] = True
    else:
        settingDict['Enabled'] = False

    settingDict['RunDirectory'] = record[3]

    if record[4] == 'True':
        settingDict['RunOnStart'] = True
    else:
        settingDict['RunOnStart'] = False

    settingDict['StartHour'] = record[5]
    settingDict['StartMinute'] = record[6]
    settingDict['StartSecond'] = record[7]
    settingDict['IntervalSeconds'] = record[8]

    if record[9] == 'None':
        settingDict['StartDelay'] = None
    else:
        settingDict['StartDelay'] = record[9]

    print(f"CONVERSION DONE: {settingDict}")
    return settingDict


def loadJsonSettingsToDatabase():
    jsonFile = 'C:/pythonscripts/PurchasingScripts/DealScriptsSettingsZim/ScriptRunner/JobSettings.json'
    jobSettingsDb = JobsettingsDatabaseHandler(databaseName="C:/pythonscripts/PurchasingScripts/DealScriptsSettingsZim/ScriptRunner/JobSettings.db")

    # jobSettingsDb.deleteJobFromDatabase("GitStatus")
    # jobSettingsDb.deleteJobFromDatabase("TestJobCircle")
    # jobSettingsDb.updateJobSettingsInDatabase(jobName='GitStatus', enabled=True)

    jobSettingsFromJson = json.load(open(jsonFile))
    for setting in jobSettingsFromJson:
        jobSettingsDb.writeNewJobSettingsToDatabase(setting)

    databaseLoadedJobs = jobSettingsDb.getJobsSettingsFromDatabase()
    print(f"RESULTS: {databaseLoadedJobs}")

    return databaseLoadedJobs


def getDatabaseJobSettingsasJsonList():
    jobSettingsDb = JobsettingsDatabaseHandler(databaseName="C:/pythonscripts/PurchasingScripts/DealScriptsSettingsZim/ScriptRunner/JobSettings.db")
    jobSettingsDb.updateJobSettingsInDatabase(jobName='GitStatus', enabled=True, startDelay=0)
    databaseLoadedJobs = jobSettingsDb.getJobsSettingsFromDatabase()

    jobJsonList = [convertDatabaseResultstoJson(r) for r in databaseLoadedJobs]
    return jobJsonList


if __name__ == "__main__":
    # loadJsonSettingsToDatabase()
    jobs = getDatabaseJobSettingsasJsonList()
    print(jobs)
