"""
Utility functions for reports
"""

from .reports import FamilyTotalOverTimeReport, DependentsTotalOverTimeReport
from .reports import FamilyCheckoutsPerWeekReport, DependentCheckoutsPerWeekReport
from .reports import ItemsPerCategoryPerMonthReport, IndividualsByAgeReport
from .reports import FamiliesPerZipReport
import vincent

availableReports = {}
availableReports[1] = FamilyTotalOverTimeReport
availableReports[2] = DependentsTotalOverTimeReport
availableReports[3] = FamilyCheckoutsPerWeekReport
availableReports[4] = DependentCheckoutsPerWeekReport
availableReports[5] = ItemsPerCategoryPerMonthReport
availableReports[6] = IndividualsByAgeReport
availableReports[7] = FamiliesPerZipReport


def determineAndCreateReport(report_num, startDate='', endDate=''):
    """Determine the report"""
    return availableReports[report_num](startDate, endDate)


def getLineGraph(data, width=600, height=400,
                 x='Date', y='', xtype='time', xnice='week', title=''):
    """Convenience method for building up a line graph"""
    vis = vincent.Line(data=data, width=width, height=height)
    vis.scales['x'] = vincent.Scale(name='x', type=xtype,
                                    range='width', nice=xnice,
                                    domain=vincent.DataRef(data='table',
                                                           field="data.idx"))
    vis.axis_titles(x=x, y=y)
    vis.legend(title=title)

    return vis.to_json()
