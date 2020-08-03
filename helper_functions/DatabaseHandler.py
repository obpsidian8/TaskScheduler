import sqlite3
import os
from datetime import datetime


class Databasehandler:
    def __init__(self, databaseName):
        self.databaseName = databaseName
        print(f"DATABASE: {databaseName} connected")

    def __createConnection(self):
        try:
            self.dbConn = sqlite3.connect(self.databaseName)
            print(f"Database connection to {self.databaseName} created")
        except Exception as ex:
            print(f"Error encountered {ex}")
        return self.dbConn

    def __commitandCloseConn(self):
        self.dbConn.commit()
        self.dbConn.close()

    def createTable(self, tableName: str, column1, type):
        self.__createConnection()
        executor = self.dbConn.cursor()
        createTableQuery = f"CREATE TABLE if not exists {tableName} ({column1} {type})"
        executor.execute(createTableQuery)
        self.__commitandCloseConn()

    def addColumntoTable(self, tableName, columnName, type):
        self.__createConnection()
        addColumnQuery = f"ALTER TABLE {tableName} ADD COLUMN {columnName} {type}"
        executor = self.dbConn.cursor()
        try:
            executor.execute(addColumnQuery)
        except Exception as exp:
            print(f"Error: {exp}")
        self.__commitandCloseConn()

    def runUserQuery(self, userQuery: str):
        data = None
        self.__createConnection()
        executor = self.dbConn.cursor()
        try:
            executor.execute(userQuery)
            data = executor.fetchall()
            print(f"Query executed: {userQuery}")
        except Exception as exp:
            print(f"Error with query: {exp}")
        self.__commitandCloseConn()
        return data

    def insertIntoTable(self, tableName, value):
        self.__createConnection()
        executor = self.dbConn.cursor()
        insertQuery = f"INSERT INTO {tableName} VALUES ('{value}')"
        try:
            executor.execute(insertQuery)
        except Exception as exp:
            print(f"Error: {exp}")
        self.__commitandCloseConn()

    def listTables(self):
        self.__createConnection()
        executor = self.dbConn.cursor()
        executor.execute("SELECT name from sqlite_master where type = 'table'")
        tables = executor.fetchall()
        print(f"Tables Retrived: {tables}")
        self.__commitandCloseConn()


class JobsettingsDatabaseHandler(Databasehandler):
    def __init__(self, databaseName):
        super().__init__(databaseName)

        self.tableName = "JobSettings"
        self.databaseName = databaseName
        self.createSettingsDatabase()

    def createSettingsDatabase(self):
        self.createTable(tableName=self.tableName, column1='JobName', type='str')
        self.addColumntoTable(tableName=self.tableName, columnName='FullCommand', type='str')
        self.addColumntoTable(tableName=self.tableName, columnName='Enabled', type='str')
        self.addColumntoTable(tableName=self.tableName, columnName='RunDirectory', type='str')
        self.addColumntoTable(tableName=self.tableName, columnName='RunOnStart', type='str')
        self.addColumntoTable(tableName=self.tableName, columnName='StartHour', type='INTEGER')
        self.addColumntoTable(tableName=self.tableName, columnName='StartMinute', type='INTEGER')
        self.addColumntoTable(tableName=self.tableName, columnName='StartSecond', type='INTEGER')
        self.addColumntoTable(tableName=self.tableName, columnName='IntervalSeconds', type='INTEGER')
        self.addColumntoTable(tableName=self.tableName, columnName='StartDelay', type='INTEGER')

    def writeNewJobSettingsToDatabase(self, settingsDict):
        jobName = settingsDict.get("JobName")
        fullCommand = settingsDict.get("FullCommand")
        enabled = settingsDict.get("Enabled")
        startHour = settingsDict.get("StartHour")
        startMinute = settingsDict.get("StartMinute")
        startSecond = settingsDict.get("StartSecond")
        intervalSeconds = settingsDict.get("IntervalSeconds")
        runOnStart = settingsDict.get("RunOnStart")

        runDirectory = settingsDict.get("RunDirectory")
        startDelay = settingsDict.get("StartDelay")

        checkQuery = f"SELECT * FROM {self.tableName} WHERE JobName = '{jobName}'"
        check = self.runUserQuery(userQuery=checkQuery)
        if not check:
            print(f"LOG INFO: Inserting New job {jobName} into database")
            insertStatement = f"INSERT INTO {self.tableName} VALUES ('{jobName}','{fullCommand}','{enabled}','{runDirectory}','{runOnStart}','{startHour}','{startMinute}','{startSecond}','{intervalSeconds}','{startDelay}')"
            self.runUserQuery(insertStatement)
        else:
            print(f"LOG INFO: Job {jobName} exists in database")

    def updateJobSettingsInDatabase(self, jobName, fullCommand=None, enabled=None, runDirectory=None, runOnStart=None, startHour=None, startMinute=None, startSecond=None,
                                    intervalSeconds=None, startDelay=None):
        updatesToMake = []
        if fullCommand is not None:
            updatesToMake.append(f" FullCommand = '{fullCommand}'")

        if enabled is not None:
            updatesToMake.append( f" Enabled = '{enabled}'")

        if runDirectory is not None:
            updatesToMake.append( f" RunDirectory = '{runDirectory}'")

        if runOnStart is not None:
            updatesToMake.append( f" RunOnStart = '{runOnStart}'")

        if startHour is not None:
            updatesToMake.append(f" StartHour = '{startHour}'")

        if runDirectory is not None:
            updatesToMake.append(f" RunDirectory = '{runDirectory}'")

        if startMinute is not None:
            updatesToMake.append(f" StartMinute = '{startMinute}'")

        if startSecond is not None:
            updatesToMake.append(f" StartSecond = '{startSecond}'")

        if startSecond is not None:
            updatesToMake.append(f" IntervalSeconds = '{intervalSeconds}'")

        if startDelay is not None:
            updatesToMake.append(f" StartDelay ='{startDelay}'")

        updateString = ",".join(updatesToMake)

        statement = f"UPDATE {self.tableName} SET {updateString} WHERE JobName = '{jobName}'"

        print(f"LOG INFO: UPDATING: {updateString}")
        print(statement)
        self.runUserQuery(statement)

    def deleteJobFromDatabase(self, jobName):
        print(f"LOG INFO: Deleting jobname {jobName} from scheduled jobs")
        deleteStatement = f"DELETE from {self.tableName} WHERE JobName  = '{jobName}'"
        self.runUserQuery(deleteStatement)

    def getJobsSettingsFromDatabase(self):
        allJobsSelectStatement = f'SELECT * FROM {self.tableName}'
        allJobsData = self.runUserQuery(allJobsSelectStatement)
        return allJobsData
