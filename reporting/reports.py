from models import CustomerFamily

from sqlalchemy import select
from sqlalchemy.sql import func

import pandas as pd
import vincent


REPORT_SESSION_KEY = 'report_info'


# Determine report

def getReportInfoAndSaveQuery(db, bottle_session, report_num):
    if report_num == '1':
        return getFamilyCount(db, bottle_session)
    elif report_num == '2':
        return getDependentCount(db, bottle_session)
    else:
        raise Exception("Not implemented")


def getGraphJson(db, bottle_session, report_num):
    if report_num == '1':
        return getFamilyGraphJson(bottle_session)
    elif report_num == '2':
        return getDependentGraphJson(bottle_session)
    else:
        return Exception("Not implemented")


# Family Count functions


def getFamilyCount(db, bottle_session):
    families = select([func.DATE(CustomerFamily.datecreated), func.count()])\
        .select_from(CustomerFamily.__table__)\
        .group_by(func.DATE(CustomerFamily.datecreated))\
        .order_by(func.DATE(CustomerFamily.datecreated))

    reader = db.execute(families)
    categoryTotals = reader.fetchall()

    bottle_session[REPORT_SESSION_KEY] = categoryTotals

    familyCount = 0
    for row in categoryTotals:
        familyCount += row[1]

    reportInfo = {}
    reportInfo['title'] = 'Total Families'
    reportInfo['html'] = 'Current number of families: ' + str(familyCount)
    return reportInfo


def getFamilyGraphJson(bottle_session):
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

    vis = vincent.Line(frame)
    vis.scales[0].type = 'time'
    vis.axis_titles(x='Date', y='Customers')
    vis.legend(title='Customer Count Over Time')

    return vis.to_json()


# Dependent Count functions


def getDependentCount(db, bottle_session):
    raise Exception("Not implemented")


def getDependentGraphJson(bottle_session):
    raise Exception("Not implemented")
