"""
Do all the work for reporting
"""

import abc
import reporting
import pandas as pd
import logging

logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s',
                    level=logging.DEBUG)
log = logging.getLogger(__name__)


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
        return reporting.utils.getLineGraph(frame, y='Customers', title=title)


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
        return reporting.utils.getLineGraph(frame, y='Dependents', title=title)


class FamilyCheckoutsPerWeekReport(Report):
    """Get the checkouts per week"""
    description = "Family Checkouts each week"

    def __init__(self):
        # This groups the checkout dates by week, subtracting two to make
        # the date be on Saturday instead of Monday
        sqlQuery = "select date_trunc('week', visits.checkout::date+"
        sqlQuery += "interval '2 days')"
        sqlQuery += "-interval '2 days' as checkout2, count(*) as count"
        sqlQuery += " from visits inner join customerfamily on"
        sqlQuery += " customerfamily.id=visits.family"
        sqlQuery += " inner join dependents on"
        sqlQuery += " customerfamily.id=dependents.family"
        sqlQuery += " where dependents.primary=True"
        sqlQuery += " and dependents.last_name not in ('User')"
        sqlQuery += " and visits.checkout IS NOT NULL"
        sqlQuery += " group by checkout2"
        sqlQuery += " order by checkout2"

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
        return reporting.utils.getLineGraph(frame, y='Families', title=title)


class DependentCheckoutsPerWeekReport(Report):
    """Get the checkouts per week"""
    description = "Dependent Checkouts each week"

    def __init__(self):
        # This groups the checkout dates by week, subtracting two to make
        # the date be on Saturday instead of Monday
        sqlQuery = "select date_trunc('week', visits.checkout::date+"
        sqlQuery += "interval '2 days')"
        sqlQuery += "-interval '2 days' as checkout2, count(*) as count"
        sqlQuery += " from visits inner join customerfamily on"
        sqlQuery += " customerfamily.id=visits.family"
        sqlQuery += " inner join dependents on"
        sqlQuery += " customerfamily.id=dependents.family"
        sqlQuery += " where dependents.last_name not in ('User')"
        sqlQuery += " and visits.checkout IS NOT NULL"
        sqlQuery += " group by checkout2"
        sqlQuery += " order by checkout2"

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
        return reporting.utils.getLineGraph(frame, y='Dependents', title=title)


class ItemsPerCategoryPerMonthReport(Report):
    """Get the number of checked out items per category per month"""
    description = "Items Per Category Checked Out Per Month"

    def __init__(self):
        # This groups the checkout dates by month
        sqlQuery = "select date_trunc('month', visits.checkout::date)"
        sqlQuery += " as checkout2, shopping_category.name as name,"
        sqlQuery += " sum(shopping_item.quantity) as count"
        sqlQuery += " from visits inner join customerfamily on"
        sqlQuery += " customerfamily.id=visits.family"
        sqlQuery += " inner join dependents on"
        sqlQuery += " customerfamily.id=dependents.family"
        sqlQuery += " inner join shopping_item on"
        sqlQuery += " shopping_item.visit = visits.id"
        sqlQuery += " inner join shopping_category on"
        sqlQuery += " shopping_category.id = shopping_item.category"
        sqlQuery += " where dependents.last_name not in ('User')"
        sqlQuery += " and dependents.primary = True"
        sqlQuery += " and visits.checkout IS NOT NULL"
        sqlQuery += " group by checkout2, name"
        sqlQuery += " order by checkout2"

        super(ItemsPerCategoryPerMonthReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allCheckouts = reader.fetchall()

        # Loop through and keep a running total to show the increase over time
        results = {}

        # Create an index of all dates
        # Create a list for each item
        results['index'] = []
        for row in allCheckouts:
            if row[1] not in results:
                results[row[1]] = []
            if row[0] not in results['index']:
                results['index'].append(row[0])

        # Create a list of all categories
        cats = []
        for row in results:
            if row != 'index':
                cats.append(row)

        # Get the number of dates
        dateLen = len(results['index'])

        # Zero out the lists for all dates
        for row in cats:
            for i in range(0, dateLen):
                results[row].append(0)

        # Put in the counts where applicable
        for row in allCheckouts:
            results[row[1]][results['index'].index(row[0])] = row[2]

        bottle_session[REPORT_SESSION_KEY] = results

        checkoutsHtml = '<table style="width:800px;"><tr><th>Date</th>'
        for row in cats:
            checkoutsHtml += '<th>' + row + '</th>'
        checkoutsHtml += '</tr>'

        for i in range(0, dateLen):
            checkoutsHtml += '<tr><td>'
            checkoutsHtml += results['index'][i].strftime("%m/%d/%Y")
            checkoutsHtml += '</td>'
            for row in cats:
                checkoutsHtml += '<td>' + str(results[row][i]) + '</td>'
            checkoutsHtml += '</tr>'
        checkoutsHtml += '</table>'

        reportInfo = {}
        reportInfo['title'] = 'Items Per Category'
        reportInfo['html'] = checkoutsHtml
        return reportInfo

    def getGraph(self, bottle_session):
        itemsPerCat = bottle_session[REPORT_SESSION_KEY]

        # Hack because apparently dates on the x axis aren't allowed here
        itemsPerCat['index'] = range(0, len(itemsPerCat['index']))

        # log.debug(results)

        title = 'Items Per Category'
        import vincent
        graph = vincent.Line(itemsPerCat, width=800, height=400, iter_idx='index')
        # graph.scales[0].type = 'time'
        graph.axis_titles(x='Date', y=title)
        graph.legend(title="Categories")
        # log.debug(graph.grammar)
        return graph.to_json()


class IndividualsByAgeReport(Report):
    """Get the dependents by age"""
    description = "Individuals By Age"

    def __init__(self):
        sqlQuery = "select count(*) as count, CASE"
        sqlQuery += " when birth_year between 0 AND 2 THEN '0-2'"
        sqlQuery += " WHEN birth_year BETWEEN 3 AND 5 THEN '3-5'"
        sqlQuery += " WHEN birth_year BETWEEN 6 AND 12 THEN '6-12'"
        sqlQuery += " WHEN birth_year BETWEEN 13 AND 18  THEN '13-18'"
        sqlQuery += " WHEN birth_year BETWEEN 19 AND 29  THEN '19-29'"
        sqlQuery += " WHEN birth_year BETWEEN 30 AND 39  THEN '30-39'"
        sqlQuery += " WHEN birth_year BETWEEN 40 AND 59  THEN '40-59'"
        sqlQuery += " WHEN birth_year BETWEEN 60 AND 150  THEN '60+' END"
        sqlQuery += " as age from (select extract(year from"
        sqlQuery += " age(birthdate::date)) as birth_year from dependents"
        sqlQuery += " inner join customerfamily on"
        sqlQuery += " customerfamily.id=dependents.family"
        sqlQuery += " where last_name not in ('User')) as deps"
        sqlQuery += " group by age"
        sqlQuery += " order by count desc"
        
        super(IndividualsByAgeReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allAgeRanges = reader.fetchall()

        #bottle_session[REPORT_SESSION_KEY] = allAgeRanges
        
        checkoutsHtml = '<table><tr><th>Age Range</th><th>Total</th></tr>'
        for row in allAgeRanges:
            checkoutsHtml += "<tr><td class=\"date\">"
            checkoutsHtml += str(row[1]) + "</td>"
            checkoutsHtml += "<td class=\"count\">" + str(row[0])
            checkoutsHtml += "</td></tr>"
        checkoutsHtml += "</table>"

        reportInfo = {}
        reportInfo['title'] = 'Individuals by Age'
        reportInfo['html'] = checkoutsHtml
        reportInfo['nograph'] = 'true'
        return reportInfo
 
    def getGraph(self, bottle_session):
        raise NotImplementedError("")
