"""
Utility functions for reports
"""

from reports import *
import vincent

availableReports = {}
availableReports["1"] = CustomerFamilyReport
availableReports["2"] = DependentsReport


def determineAndCreateReport(report_num):
    """Determine the report"""
    return availableReports[report_num]()


def getLineGraph(data, width=600, height=400,
                 x='Date', y='', xtype='time', title=''):
    """Convenience method for building up a line graph"""
    vis = vincent.Line(data=data, width=width, height=height)
    vis.scales[0].type = xtype
    vis.axis_titles(x=x, y=y)
    vis.legend(title=title)

    return vis.to_json()
