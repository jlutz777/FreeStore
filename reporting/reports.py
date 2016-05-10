"""
Do all the work for reporting
"""

import abc
import logging
import os
import pandas as pd
import pickle
import reporting
import tempfile

logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s',
                    level=logging.DEBUG)
log = logging.getLogger(__name__)


REPORT_SESSION_KEY = 'report_info'


def storeCookieInfo(sess, data):
    fd, temp_path = tempfile.mkstemp()
    pickled = pickle.dumps(data, 2)
    os.write(fd, pickled)
    os.close(fd)
    sess[REPORT_SESSION_KEY] = temp_path


def retrieveCookieInfo(sess):
    fileName = sess[REPORT_SESSION_KEY]
    with open(fileName, 'rb') as f:
        data = pickle.loads(f.read())
    
    if fileName.startswith('/tmp/'):
        os.remove(fileName)
    else:
        log.debug("Couldn't delete: " + fileName)
    
    return data


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

    def __init__(self, start_date='', end_date=''):
        
        # Convert start_date and end_date into dates!
        sqlQuery = "select customerfamily.datecreated::date, count(*)"
        sqlQuery += " from customerfamily inner join dependents on"
        sqlQuery += " customerfamily.id=dependents.family"
        sqlQuery += " where dependents.primary=True and"
        sqlQuery += " dependents.last_name not in ('User') and"
        sqlQuery += " datecreated > '" + start_date + "' and "
        sqlQuery += " datecreated < '" + end_date + "'"
        sqlQuery += " group by datecreated::date"
        sqlQuery += " order by datecreated::date"

        super(FamilyTotalOverTimeReport, self).__init__(sqlQuery)

    def getData(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        categoryTotals = reader.fetchall()
        totalFamilyCount = 0
        arr = []
        for row in categoryTotals:
            totalFamilyCount += row[1]
            keyVal = {}
            keyVal["date"] = row[0].strftime("%m/%d/%Y")
            keyVal["count"] = str(totalFamilyCount)
            arr.append(keyVal)
            #familyCountsHtml += "<tr><td class=\"date\">"
            #familyCountsHtml += row[0].strftime("%m/%d/%Y") + "</td>"
            #familyCountsHtml += "<td class=\"count\">" + str(totalFamilyCount)
            #familyCountsHtml += "</td></tr>"
        #familyCountsHtml += "</table>"
        return arr

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        categoryTotals = reader.fetchall()
        
        storeCookieInfo(bottle_session, categoryTotals)

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
        reportInfo['title'] = 'Total Families Over Time'
        reportInfo['html'] = familyCountsHtml
        return reportInfo

    def getGraph(self, bottle_session):
        categoryTotals = retrieveCookieInfo(bottle_session)
        
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

    def __init__(self, start_date='', end_date=''):
        sqlQuery = "select customerfamily.datecreated::date, count(*)"
        sqlQuery += " from dependents inner join customerfamily on"
        sqlQuery += " customerfamily.id=dependents.family"
        sqlQuery += " where dependents.last_name not in ('User') and"
        sqlQuery += " datecreated > '" + start_date + "' and "
        sqlQuery += " datecreated < '" + end_date + "'"
        sqlQuery += " group by datecreated::date"
        sqlQuery += " order by datecreated::date"

        super(DependentsTotalOverTimeReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        categoryTotals = reader.fetchall()

        storeCookieInfo(bottle_session, categoryTotals)

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
        categoryTotals = retrieveCookieInfo(bottle_session)
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

    def __init__(self, start_date='', end_date=''):
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
        sqlQuery += " and visits.checkout IS NOT NULL and"
        sqlQuery += " visits.checkout > '" + start_date + "' and "
        sqlQuery += " visits.checkout < '" + end_date + "'"
        sqlQuery += " group by checkout2"
        sqlQuery += " order by checkout2"

        super(FamilyCheckoutsPerWeekReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allCheckouts = reader.fetchall()

        storeCookieInfo(bottle_session, allCheckouts)

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
        allCheckouts = retrieveCookieInfo(bottle_session)
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

    def __init__(self, start_date='', end_date=''):
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
        sqlQuery += " and visits.checkout IS NOT NULL and"
        sqlQuery += " visits.checkout > '" + start_date + "' and "
        sqlQuery += " visits.checkout < '" + end_date + "'"
        sqlQuery += " group by checkout2"
        sqlQuery += " order by checkout2"

        super(DependentCheckoutsPerWeekReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allCheckouts = reader.fetchall()

        storeCookieInfo(bottle_session, allCheckouts)

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
        allCheckouts = retrieveCookieInfo(bottle_session)
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

    def __init__(self, start_date='', end_date=''):
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
        sqlQuery += " and visits.checkout IS NOT NULL and"
        sqlQuery += " visits.checkout > '" + start_date + "' and "
        sqlQuery += " visits.checkout < '" + end_date + "'"
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

        storeCookieInfo(bottle_session, results)

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
        itemsPerCat = retrieveCookieInfo(bottle_session)

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

    def __init__(self, start_date='', end_date=''):
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
        sqlQuery += " where last_name not in ('User') and"
        sqlQuery += " customerfamily.datecreated > '" + start_date + "' and "
        sqlQuery += " customerfamily.datecreated < '" + end_date + "'"
        sqlQuery += ") as deps"
        sqlQuery += " group by age"
        sqlQuery += " order by count desc"
        
        super(IndividualsByAgeReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allAgeRanges = reader.fetchall()

        #storeCookieInfo(bottle_session, allAgeRanges)
        
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


class FamiliesPerZipReport(Report):
    """Get the number of families in each zip code"""
    description = "Familes by zip code"

    def __init__(self, start_date='', end_date=''):
        # This groups the checkout dates by week, subtracting two to make
        # the date be on Saturday instead of Monday
        sqlQuery = "select zip, count(*) as total"
        sqlQuery += " from customerfamily inner join"
        sqlQuery += " dependents on"
        sqlQuery += " customerfamily.id=dependents.family"
        sqlQuery += " where dependents.last_name not in ('User') and"
        sqlQuery += " customerfamily.datecreated > '" + start_date + "' and "
        sqlQuery += " customerfamily.datecreated < '" + end_date + "'"
        sqlQuery += " group by zip"
        sqlQuery += " order by zip"

        super(FamiliesPerZipReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allFamilies = reader.fetchall()
        
        #storeCookieInfo(bottle_session, allFamilies)

        familiesHtml = '<table><tr><th>Zip</th><th>Total</th></tr>'
        for row in allFamilies:
            familiesHtml += "<tr><td class=\"category\">"
            familiesHtml += str(row[0]) + "</td>"
            familiesHtml += "<td class=\"count\">" + str(row[1])
            familiesHtml += "</td></tr>"
        familiesHtml += "</table>"

        reportInfo = {}
        reportInfo['title'] = 'Familes by Zip Code'
        reportInfo['html'] = familiesHtml
        reportInfo['nograph'] = 'true'
        return reportInfo

    def getGraph(self, bottle_session):
        raise NotImplementedError("")


class CheckoutFrequencyPerMonthReport(Report):
    """Get the frequency of visits per family per month"""
    description = "Visit Frequency Per Month"

    def __init__(self, start_date='', end_date=''):
        # I am only counting visits that have a shopping item on them, otherwise I'm not counting it
        sqlQuery = "select checkout2 as checkout_date, count as frequency, count(count) as families"
        sqlQuery += " from (select checkout2, id, count(count)"
        sqlQuery += " from (select date_trunc('month', visits.checkout::date) as checkout2, customerfamily.id"
        sqlQuery += ", count(visits.id) as count from visits inner join customerfamily"
        sqlQuery += " on customerfamily.id=visits.family inner join dependents on"
        sqlQuery += " customerfamily.id=dependents.family inner join shopping_item on"
        sqlQuery += " shopping_item.visit=visits.id where dependents.primary=True and"
        sqlQuery += " dependents.last_name not in ('User') and visits.checkout IS NOT NULL and"
        sqlQuery += " visits.checkout >= '" + start_date + "' and visits.checkout <= '" + end_date + "'"
        sqlQuery += " group by checkout2, customerfamily.id,visits.id order by checkout2"
        sqlQuery += ") as foo group by checkout2, id) as foo2"
        sqlQuery += " group by checkout2, count order by checkout2, count"

        super(CheckoutFrequencyPerMonthReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allFrequencies = reader.fetchall()

        #storeCookieInfo(bottle_session, allFrequencies)

        frequencyHtml = '<table><tr><th>Date</th><th>Frequency</th><th>Family Count</th></tr>'
        for row in allFrequencies:
            frequencyHtml += "<tr><td class=\"date\">"
            frequencyHtml += row[0].strftime("%m/%d/%Y") + "</td>"
            frequencyHtml += "<td class=\"category\">" + str(row[1])
            frequencyHtml += "</td><td class=\"category\">" + str(row[2])
            frequencyHtml += "</td></tr>"
        frequencyHtml += "</table>"

        reportInfo = {}
        reportInfo['title'] = 'Visit Frequency Per Month'
        reportInfo['html'] = frequencyHtml
        reportInfo['nograph'] = 'true'
        return reportInfo

    def getGraph(self, bottle_session):
        raise NotImplementedError("")
