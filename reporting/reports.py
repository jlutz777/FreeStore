"""
Do all the work for reporting
"""

import abc
from utils.utils import *

class Report:
    """Base class for reports"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, sqlQuery):
        self.sqlQuery = sqlQuery

    @abc.abstractmethod
    def getTitleAndHtml(self, db, bottle_session):
        pass

    @abc.abstractmethod
    def getData(self, db, bottle_session, reuse):
        pass

    def getDataAndHtml(self, db, bottle_session):
        data, reuse = self.getTitleAndHtml(db, bottle_session)
        graph = None
        info = { 'data': data }
        if reuse is not None:
            graph = self.getData(db, bottle_session, reuse)
            info['graph'] = graph
        return info


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
        sqlQuery += " datecreated > '" + start_date + "' and"
        sqlQuery += " datecreated < '" + end_date + "' and"
        sqlQuery += " customerfamily.is_customer=True"
        sqlQuery += " group by datecreated::date"
        sqlQuery += " order by datecreated::date DESC"

        super(FamilyTotalOverTimeReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        categoryTotals = reader.fetchall()

        totalFamilyCount = 0
        familyCountsHtml = '<table><tr><th>Date</th><th>Total</th></tr>'
        for row in categoryTotals:
            totalFamilyCount += row[1]
            familyCountsHtml += "<tr><td class=\"date\">"
            familyCountsHtml += formatted_str_date(row[0]) + "</td>"
            familyCountsHtml += "<td class=\"count\">" + str(totalFamilyCount)
            familyCountsHtml += "</td></tr>"
        familyCountsHtml += "</table>"

        reportInfo = {}
        reportInfo['title'] = 'Family Count Over Time'
        reportInfo['html'] = familyCountsHtml
        return reportInfo, categoryTotals

    def getData(self, db, bottle_session, categoryTotals):
        totalFamilyCount = 0
        arr = []
        for row in categoryTotals:
            totalFamilyCount += row[1]
            keyVal = {}
            keyVal["date"] = formatted_str_date(row[0])
            keyVal["count"] = str(totalFamilyCount)
            arr.append(keyVal)
        return arr


class DependentsTotalOverTimeReport(Report):
    """Get the dependents count over time"""
    description = "Dependents over time"

    def __init__(self, start_date='', end_date=''):
        sqlQuery = "select customerfamily.datecreated::date, count(*)"
        sqlQuery += " from dependents inner join customerfamily on"
        sqlQuery += " customerfamily.id=dependents.family"
        sqlQuery += " where dependents.last_name not in ('User') and"
        sqlQuery += " datecreated > '" + start_date + "' and "
        sqlQuery += " datecreated < '" + end_date + "' and"
        sqlQuery += " customerfamily.is_customer=True"
        sqlQuery += " group by datecreated::date"
        sqlQuery += " order by datecreated::date DESC"

        super(DependentsTotalOverTimeReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        categoryTotals = reader.fetchall()

        totalFamilyCount = 0
        familyCountsHtml = '<table><tr><th>Date</th><th>Total</th></tr>'
        for row in categoryTotals:
            totalFamilyCount += row[1]
            familyCountsHtml += "<tr><td class=\"date\">"
            familyCountsHtml += formatted_str_date(row[0]) + "</td>"
            familyCountsHtml += "<td class=\"count\">" + str(totalFamilyCount)
            familyCountsHtml += "</td></tr>"
        familyCountsHtml += "</table>"

        reportInfo = {}
        reportInfo['title'] = 'Dependents Count Over Time'
        reportInfo['html'] = familyCountsHtml
        return reportInfo, categoryTotals

    def getData(self, db, bottle_session, categoryTotals):
        prevVal = 0
        arr = []

        for row in categoryTotals:
            prevVal = prevVal + row[1]
            keyVal = {}
            keyVal["date"] = formatted_str_date(row[0])
            keyVal["count"] = prevVal
            arr.append(keyVal)

        return arr


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
        sqlQuery += " inner join (select visit from shopping_item"
        sqlQuery += " group by visit) as b on visits.id=b.visit"
        sqlQuery += " where dependents.primary=True"
        sqlQuery += " and dependents.last_name not in ('User')"
        sqlQuery += " and visits.checkout IS NOT NULL and"
        sqlQuery += " visits.checkout > '" + start_date + "' and "
        sqlQuery += " visits.checkout < '" + end_date + "'"
        sqlQuery += " group by checkout2"
        sqlQuery += " order by checkout2 DESC"

        super(FamilyCheckoutsPerWeekReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allCheckouts = reader.fetchall()

        checkoutsHtml = '<table><tr><th>Date</th><th>Total</th></tr>'
        for row in allCheckouts:
            checkoutsHtml += "<tr><td class=\"date\">"
            checkoutsHtml += formatted_str_date(row[0]) + "</td>"
            checkoutsHtml += "<td class=\"count\">" + str(row[1])
            checkoutsHtml += "</td></tr>"
        checkoutsHtml += "</table>"

        reportInfo = {}
        reportInfo['title'] = 'Families Checked Out Per Day'
        reportInfo['html'] = checkoutsHtml
        return reportInfo, allCheckouts

    def getData(self, db, bottle_session, allCheckouts):
        arr = []

        for row in allCheckouts:
            keyVal = {}
            keyVal["date"] = formatted_str_date(row[0])
            keyVal["count"] = row[1]
            arr.append(keyVal)

        return arr


class EmptyFamilyCheckoutsPerWeekReport(Report):
    """Get the empty checkouts per week"""
    description = "Empty Family Checkouts each week"

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
        sqlQuery += " left join shopping_item on"
        sqlQuery += " visits.id=shopping_item.visit"
        sqlQuery += " where dependents.primary=True"
        sqlQuery += " and shopping_item.id IS NULL"
        sqlQuery += " and dependents.last_name not in ('User')"
        sqlQuery += " and visits.checkout IS NOT NULL and"
        sqlQuery += " visits.checkout > '" + start_date + "' and "
        sqlQuery += " visits.checkout < '" + end_date + "'"
        sqlQuery += " group by checkout2"
        sqlQuery += " order by checkout2 DESC"

        super(EmptyFamilyCheckoutsPerWeekReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allCheckouts = reader.fetchall()

        checkoutsHtml = '<table><tr><th>Date</th><th>Total</th></tr>'
        for row in allCheckouts:
            checkoutsHtml += "<tr><td class=\"date\">"
            checkoutsHtml += formatted_str_date(row[0]) + "</td>"
            checkoutsHtml += "<td class=\"count\">" + str(row[1])
            checkoutsHtml += "</td></tr>"
        checkoutsHtml += "</table>"

        reportInfo = {}
        reportInfo['title'] = 'Empty Families Checked Out Per Day'
        reportInfo['html'] = checkoutsHtml
        return reportInfo, allCheckouts

    def getData(self, db, bottle_session, allCheckouts):
        arr = []

        for row in allCheckouts:
            keyVal = {}
            keyVal["date"] = formatted_str_date(row[0])
            keyVal["count"] = row[1]
            arr.append(keyVal)

        return arr


class FamilyCheckInsPerWeekReport(Report):
    """Get the checkins per week"""
    description = "Family Checkins each week"

    def __init__(self, start_date='', end_date=''):
        # This groups the checkout dates by week, subtracting two to make
        # the date be on Saturday instead of Monday
        sqlQuery = "select date_trunc('week', visits.checkin::date+"
        sqlQuery += "interval '2 days')"
        sqlQuery += "-interval '2 days' as checkin2, count(*) as count"
        sqlQuery += " from visits inner join customerfamily on"
        sqlQuery += " customerfamily.id=visits.family"
        sqlQuery += " inner join dependents on"
        sqlQuery += " customerfamily.id=dependents.family"
        sqlQuery += " left join (select visit from shopping_item"
        sqlQuery += " group by visit) as b on visits.id=b.visit"
        sqlQuery += " where dependents.primary=True"
        sqlQuery += " and dependents.last_name not in ('User')"
        sqlQuery += " and visits.checkin > '" + start_date + "' and"
        sqlQuery += " visits.checkin < '" + end_date + "' and"
        sqlQuery += " ((b.visit IS NOT NULL and visits.checkout IS NOT NULL) or"
        sqlQuery += " visits.checkout IS NULL)"
        sqlQuery += " group by checkin2"
        sqlQuery += " order by checkin2 DESC"

        super(FamilyCheckInsPerWeekReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allCheckouts = reader.fetchall()

        checkoutsHtml = '<table><tr><th>Date</th><th>Total</th></tr>'
        for row in allCheckouts:
            checkoutsHtml += "<tr><td class=\"date\">"
            checkoutsHtml += formatted_str_date(row[0]) + "</td>"
            checkoutsHtml += "<td class=\"count\">" + str(row[1])
            checkoutsHtml += "</td></tr>"
        checkoutsHtml += "</table>"

        reportInfo = {}
        reportInfo['title'] = 'Families Checked In Per Day'
        reportInfo['html'] = checkoutsHtml
        return reportInfo, allCheckouts

    def getData(self, db, bottle_session, allCheckouts):
        arr = []

        for row in allCheckouts:
            keyVal = {}
            keyVal["date"] = formatted_str_date(row[0])
            keyVal["count"] = row[1]
            arr.append(keyVal)

        return arr


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
        sqlQuery += " inner join (select visit from shopping_item"
        sqlQuery += " group by visit) as b on visits.id=b.visit"
        sqlQuery += " where dependents.last_name not in ('User')"
        sqlQuery += " and visits.checkout IS NOT NULL and"
        sqlQuery += " visits.checkout > '" + start_date + "' and "
        sqlQuery += " visits.checkout < '" + end_date + "'"
        sqlQuery += " group by checkout2"
        sqlQuery += " order by checkout2 DESC"

        super(DependentCheckoutsPerWeekReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allCheckouts = reader.fetchall()

        checkoutsHtml = '<table><tr><th>Date</th><th>Total</th></tr>'
        for row in allCheckouts:
            checkoutsHtml += "<tr><td class=\"date\">"
            checkoutsHtml += formatted_str_date(row[0]) + "</td>"
            checkoutsHtml += "<td class=\"count\">" + str(row[1])
            checkoutsHtml += "</td></tr>"
        checkoutsHtml += "</table>"

        reportInfo = {}
        reportInfo['title'] = 'Dependents Checked Out Per Day'
        reportInfo['html'] = checkoutsHtml
        return reportInfo, allCheckouts

    def getData(self, db, bottle_session, allCheckouts):
        arr = []

        for row in allCheckouts:
            keyVal = {}
            keyVal["date"] = formatted_str_date(row[0])
            keyVal["count"] = row[1]
            arr.append(keyVal)

        return arr


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
        sqlQuery += " order by checkout2 DESC"

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

        checkoutsHtml = '<table style="width:800px;"><tr><th>Date</th>'
        for row in cats:
            checkoutsHtml += '<th>' + row + '</th>'
        checkoutsHtml += '</tr>'

        for i in range(0, dateLen):
            checkoutsHtml += '<tr><td>'
            checkoutsHtml += formatted_str_date(results['index'][i])
            checkoutsHtml += '</td>'
            for row in cats:
                checkoutsHtml += '<td>' + str(results[row][i]) + '</td>'
            checkoutsHtml += '</tr>'
        checkoutsHtml += '</table>'

        reportInfo = {}
        reportInfo['title'] = 'Items Per Category'
        reportInfo['html'] = checkoutsHtml
        return reportInfo, results

    def getData(self, db, bottle_session, itemsPerCat):
        arr = []
        dateLen = len(itemsPerCat['index'])

        # Create a list of all categories
        cats = []
        for row in itemsPerCat:
            if row != 'index':
                cats.append(row)

        for i in range(0, dateLen):
            keyVal = {}
            keyVal["date"] = formatted_str_date(itemsPerCat['index'][i])
            for row in cats:
                keyVal[row] = itemsPerCat[row][i]
            arr.append(keyVal)

        return arr


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
        sqlQuery += " customerfamily.datecreated < '" + end_date + "' and"
        sqlQuery += " customerfamily.is_customer=True"
        sqlQuery += ") as deps"
        sqlQuery += " group by age"
        sqlQuery += " order by count desc"

        super(IndividualsByAgeReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allAgeRanges = reader.fetchall()

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
        return reportInfo, None


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
        sqlQuery += " dependents.primary=True and"
        sqlQuery += " customerfamily.datecreated > '" + start_date + "' and "
        sqlQuery += " customerfamily.datecreated < '" + end_date + "' and"
        sqlQuery += " customerfamily.is_customer=True"
        sqlQuery += " group by zip"
        sqlQuery += " order by zip"

        super(FamiliesPerZipReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allFamilies = reader.fetchall()

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
        return reportInfo, None


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
        sqlQuery += " group by checkout2, count order by checkout2 DESC, count"

        super(CheckoutFrequencyPerMonthReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allFrequencies = reader.fetchall()

        frequencyHtml = '<table><tr><th>Date</th><th>Frequency</th><th>Family Count</th></tr>'
        for row in allFrequencies:
            frequencyHtml += "<tr><td class=\"date\">"
            frequencyHtml += formatted_str_date(row[0]) + "</td>"
            frequencyHtml += "<td class=\"category\">" + str(row[1])
            frequencyHtml += "</td><td class=\"category\">" + str(row[2])
            frequencyHtml += "</td></tr>"
        frequencyHtml += "</table>"

        reportInfo = {}
        reportInfo['title'] = 'Visit Frequency Per Month'
        reportInfo['html'] = frequencyHtml
        return reportInfo, None


class VolunteersHoursWorkedReport(Report):
    """Get the number of hours worked per volunteer total"""
    description = "Number of Hours Worked Per Volunteer"

    def __init__(self, start_date='', end_date=''):
        sqlQuery = "select sum(checkout-checkin) as diff, "
        sqlQuery += "dependents.first_name as fn, dependents.last_name as ln "
        sqlQuery += "from volunteervisits inner join customerfamily "
        sqlQuery += "on customerfamily.id=volunteervisits.family inner join "
        sqlQuery += "dependents on customerfamily.id=dependents.family "
        sqlQuery += "where dependents.primary=True and dependents.last_name "
        sqlQuery += "not in ('User') and volunteervisits.checkout IS NOT NULL "
        sqlQuery += "and volunteervisits.checkout >= '" + start_date
        sqlQuery += "' and volunteervisits.checkout <= '" + end_date + "' "
        sqlQuery += "and current_date+1 > volunteervisits.checkin "
        sqlQuery += "group by customerfamily.id, ln, fn order by ln, fn"
        
        super(VolunteersHoursWorkedReport, self).__init__(sqlQuery)

    def getTitleAndHtml(self, db, bottle_session):
        reader = db.execute(self.sqlQuery)
        allHours = reader.fetchall()

        frequencyHtml = '<table><tr><th>Name</th><th>Hours</th></tr>'
        for row in allHours:
            frequencyHtml += "<tr><td class=\"category\">" + str(row[1])
            frequencyHtml += " " + str(row[2])
            frequencyHtml += "</td><td class=\"category\">" + str(row[0])
            frequencyHtml += "</td></tr>"
        frequencyHtml += "</table>"

        reportInfo = {}
        reportInfo['title'] = 'Volunteer Hours'
        reportInfo['html'] = frequencyHtml
        return reportInfo, None
