import datetime
import unittest
import os
import json
import ssl
from urllib.request import Request, urlopen


class CiscTestCase(unittest.TestCase):

    testResults = []

    def tearDown(self):
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self.defaultTestResult()  # These two methods have no side effects
            self._feedErrorsToResult(result, self._outcome.errors)
        else:  # Python 3.2 - 3.3 or 3.0 - 3.1 and 2.7
            result = getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups)
        error = self.list2reason(result.errors)
        failure = self.list2reason(result.failures)
        ok = not error and not failure
        testLocation = self.id()
        testName = testLocation[testLocation.rindex('.') + 1:]
        if not ok:
            self.addUnitTestResult(testName, False)
        else:
            self.addUnitTestResult(testName, True)

    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]

    @classmethod
    def tearDownClass(cls):
        cls.notifyGitlabService()

    @classmethod
    def notifyGitlabService(cls):
        sslContext = ssl.SSLContext()
        url = 'https://codesmell.org/CodesmellService/unit_test/add'
        gitConfigOrigin = cls.getGitOriginUrlFromGitConfig().strip()
        userName = cls.getUsernameFromGitConfigOrigin(gitConfigOrigin)
        courseName = cls.getCourseFromGitConfigOrigin(gitConfigOrigin)
        assignmentName = cls.getAssignmentFromGitConfigOrigin(gitConfigOrigin)
        unitTestExecution = cls.buildUnitTestExecution(userName, courseName, assignmentName)

        postdata = json.dumps(unitTestExecution).encode()
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        httprequest = Request(url, data=postdata, method="POST", headers=headers)

        with urlopen(httprequest, context=sslContext) as response:
            if response.code != 200:
                print('Error updating progress')


    @classmethod
    def buildUnitTestExecution(cls, userName, courseName, assignmentName):
        unitTestExecution = {}
        unitTestExecution["studentName"] = userName
        unitTestExecution["courseName"] = courseName
        unitTestExecution["assignmentName"] = assignmentName
        unitTestExecution["unitTestResults"] = cls.testResults
        unitTestExecution["date"] = str(datetime.date.today())
        return unitTestExecution

    @classmethod
    def addUnitTestResult(cls, testName, passed):
        testResult = {}
        testResult["testName"] = testName
        testResult["passed"] = passed
        cls.testResults.append(testResult)

    @classmethod
    def getGitOriginUrlFromGitConfig(cls):
        gitConfig = open('.git' + os.path.sep + 'config', 'r')
        foundLine = False
        for line in gitConfig:
            if foundLine:
                gitConfig.close()
                return line
            if line.find('[remote "origin"]') != -1:
                foundLine = True
        gitConfig.close()
        return ""

    @classmethod
    def getUsernameFromGitConfigOrigin(cls, gitConfigOrigin):
        subgroupStartIndex = gitConfigOrigin.index('/', 35)
        subgroupEndIndex = gitConfigOrigin.index('/', subgroupStartIndex + 1)
        if subgroupStartIndex != -1 and subgroupEndIndex != -1:
            return gitConfigOrigin[subgroupStartIndex + 1:subgroupEndIndex]
        else:
            return ""

    @classmethod
    def getCourseFromGitConfigOrigin(cls, gitConfigOrigin):
        classStartIndex = gitConfigOrigin.index('/', 14)
        classEndIndex = gitConfigOrigin.index('/', classStartIndex + 1)
        if classStartIndex != -1 and classEndIndex != -1:
            return gitConfigOrigin[classStartIndex + 1:classEndIndex]
        else:
            return ""

    @classmethod
    def getAssignmentFromGitConfigOrigin(cls, gitConfigOrigin):
        assignmentStartIndex = gitConfigOrigin.rindex('/')
        assignmentEndIndex = gitConfigOrigin.rindex('.')
        if assignmentStartIndex != -1 and assignmentEndIndex != -1:
            return gitConfigOrigin[assignmentStartIndex + 1:assignmentEndIndex]
        else:
            return ""
