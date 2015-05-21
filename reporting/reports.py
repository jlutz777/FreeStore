"""
Do all the work for reporting
"""

import abc
import utils
import pandas as pd


REPORT_SESSION_KEY = 'report_info'


class Report:
    """Base class for reports"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, sqlQuery):
        self.sqlQuery = sqlQuery

    @abc.abstractmethod
    def getTitleAndHtml(db, bottle_session):
        pass

    @abc.abstractmethod
    def getGraph(bottle_session):
        pass


class FamilyTotalOverTimeReport(Report):
    """Get the customer family count over time"""
    description = "Families over time"

    def __init__(self):
        sqlQuery = "select customerfamily.datecreated::date, count(*)"
        sqlQuery += " from customerfamily inner join dependents on"
        sqlQuery += " customerfamily.id=dependents.family"
        sqlQuery += " where dependents.primary=True and"
        sqlQuery += " dependents.last_name not in ('User')"
        sqlQuery += " group by datecreated::date"
        sqlQuery += " order by datecreated::date"

        super(FamilyTotalOverTimeReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        categoryTotals = reader.fetchall()

        bottle_session[REPORT_SESSION_KEY] = categoryTotals

        totalFamilyCount = 0
        familyCountsHtml = '<table><tr><th>Date</th><th>Total</th></tr>'
        for row in categoryTotals:
            totalFamilyCount += row[1]
            familyCountsHtml += "<tr><td class=\"date\">"
            familyCountsHtml += row[0].strftime("%m/%d/%Y") + "</td>"
            familyCountsHtml += "<td class=\"count\">" + str(totalFamilyCount)
            familyCountsHtml += "</td></tr>"
        familyCountsHtml += "</table>"

        reportInfo = {}
        reportInfo['title'] = 'Total Families'
        reportInfo['html'] = familyCountsHtml
        return reportInfo

    def getGraph(self, bottle_session):
        categoryTotals = bottle_session[REPORT_SESSION_KEY]
        # Loop through and keep a running total to show the increase over time
        columns = ["date", "count"]
        results = []
        prevVal = 0

        for row in categoryTotals:
            prevVal = prevVal + row[1]
            results.append(dict(zip(columns, [row[0], prevVal])))

        frame = pd.DataFrame().from_records(results, index="date",
                                            columns=["date", "count"])

        title = 'Customer Count Over Time'
        return utils.getLineGraph(frame, y='Customers', title=title)


class DependentsTotalOverTimeReport(Report):
    """Get the dependents count over time"""
    description = "Dependents over time"

    def __init__(self):
        sqlQuery = "select customerfamily.datecreated::date, count(*)"
        sqlQuery += " from dependents inner join customerfamily on"
        sqlQuery += " customerfamily.id=dependents.family"
        sqlQuery += " where dependents.last_name not in ('User')"
        sqlQuery += " group by datecreated::date"
        sqlQuery += " order by datecreated::date"

        super(DependentsTotalOverTimeReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        categoryTotals = reader.fetchall()

        bottle_session[REPORT_SESSION_KEY] = categoryTotals

        totalFamilyCount = 0
        familyCountsHtml = '<table><tr><th>Date</th><th>Total</th></tr>'
        for row in categoryTotals:
            totalFamilyCount += row[1]
            familyCountsHtml += "<tr><td class=\"date\">"
            familyCountsHtml += row[0].strftime("%m/%d/%Y") + "</td>"
            familyCountsHtml += "<td class=\"count\">" + str(totalFamilyCount)
            familyCountsHtml += "</td></tr>"
        familyCountsHtml += "</table>"

        reportInfo = {}
        reportInfo['title'] = 'Total Dependents'
        reportInfo['html'] = familyCountsHtml
        return reportInfo

    def getGraph(self, bottle_session):
        categoryTotals = bottle_session[REPORT_SESSION_KEY]
        # Loop through and keep a running total to show the increase over time
        columns = ["date", "count"]
        results = []
        prevVal = 0

        for row in categoryTotals:
            prevVal = prevVal + row[1]
            results.append(dict(zip(columns, [row[0], prevVal])))

        frame = pd.DataFrame().from_records(results, index="date",
                                            columns=["date", "count"])

        title = 'Dependents Count Over Time'
        return utils.getLineGraph(frame, y='Dependents', title=title)

class FamilyCheckoutsPerWeekReport(Report):
    """Get the checkouts per week"""
    description = "Family Checkouts each week"

    def __init__(self):
        sqlQuery = "select visits.checkout::date as checkout, count(*)"
        sqlQuery += " from visits inner join customerfamily on"
        sqlQuery += " customerfamily.id=visits.family"
        sqlQuery += " inner join dependents on"
        sqlQuery += " customerfamily.id=dependents.family"
        sqlQuery += " where dependents.primary=True"
        sqlQuery += " and dependents.last_name not in ('User')"
        sqlQuery += " and checkout IS NOT NULL"
        sqlQuery += " group by checkout::date"
        sqlQuery += " order by checkout::date"

        super(FamilyCheckoutsPerWeekReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allCheckouts = reader.fetchall()

        bottle_session[REPORT_SESSION_KEY] = allCheckouts

        checkoutsHtml = '<table><tr><th>Date</th><th>Total</th></tr>'
        for row in allCheckouts:
            checkoutsHtml += "<tr><td class=\"date\">"
            checkoutsHtml += row[0].strftime("%m/%d/%Y") + "</td>"
            checkoutsHtml += "<td class=\"count\">" + str(row[1])
            checkoutsHtml += "</td></tr>"
        checkoutsHtml += "</table>"

        reportInfo = {}
        reportInfo['title'] = 'Family Checkouts'
        reportInfo['html'] = checkoutsHtml
        return reportInfo

    def getGraph(self, bottle_session):
        allCheckouts = bottle_session[REPORT_SESSION_KEY]
        # Loop through and keep a running total to show the increase over time
        columns = ["checkout", "count"]
        results = []

        for row in allCheckouts:
            results.append(dict(zip(columns, [row[0], row[1]])))

        frame = pd.DataFrame().from_records(results, index="checkout",
                                            columns=["checkout", "count"])

        title = 'Families Checked Out Per Day'
        return utils.getLineGraph(frame, y='Families', title=title)

class DependentCheckoutsPerWeekReport(Report):
    """Get the checkouts per week"""
    description = "Dependent Checkouts each week"

    def __init__(self):
        sqlQuery = "select visits.checkout::date as checkout, count(*)"
        sqlQuery += " from visits inner join customerfamily on"
        sqlQuery += " customerfamily.id=visits.family"
        sqlQuery += " inner join dependents on"
        sqlQuery += " customerfamily.id=dependents.family"
        sqlQuery += " where dependents.last_name not in ('User')"
        sqlQuery += " and checkout IS NOT NULL"
        sqlQuery += " group by checkout::date"
        sqlQuery += " order by checkout::date"

        super(DependentCheckoutsPerWeekReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allCheckouts = reader.fetchall()

        bottle_session[REPORT_SESSION_KEY] = allCheckouts

        checkoutsHtml = '<table><tr><th>Date</th><th>Total</th></tr>'
        for row in allCheckouts:
            checkoutsHtml += "<tr><td class=\"date\">"
            checkoutsHtml += row[0].strftime("%m/%d/%Y") + "</td>"
            checkoutsHtml += "<td class=\"count\">" + str(row[1])
            checkoutsHtml += "</td></tr>"
        checkoutsHtml += "</table>"

        reportInfo = {}
        reportInfo['title'] = 'Family Checkouts'
        reportInfo['html'] = checkoutsHtml
        return reportInfo

    def getGraph(self, bottle_session):
        allCheckouts = bottle_session[REPORT_SESSION_KEY]
        # Loop through and keep a running total to show the increase over time
        columns = ["checkout", "count"]
        results = []

        for row in allCheckouts:
            results.append(dict(zip(columns, [row[0], row[1]])))

        frame = pd.DataFrame().from_records(results, index="checkout",
                                            columns=["checkout", "count"])

        title = 'Dependents Checked Out Per Day'
        return utils.getLineGraph(frame, y='Dependents', title=title)