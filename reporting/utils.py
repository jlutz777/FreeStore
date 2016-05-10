"""
Utility functions for reports
"""

from .reports import FamilyTotalOverTimeReport, DependentsTotalOverTimeReport
from .reports import FamilyCheckoutsPerWeekReport, DependentCheckoutsPerWeekReport
from .reports import ItemsPerCategoryPerMonthReport, IndividualsByAgeReport
from .reports import FamiliesPerZipReport, CheckoutFrequencyPerMonthReport

availableReports = {}
availableReports[1] = FamilyTotalOverTimeReport
availableReports[2] = DependentsTotalOverTimeReport
availableReports[3] = FamilyCheckoutsPerWeekReport
availableReports[4] = DependentCheckoutsPerWeekReport
availableReports[5] = ItemsPerCategoryPerMonthReport
availableReports[6] = IndividualsByAgeReport
availableReports[7] = FamiliesPerZipReport
availableReports[8] = CheckoutFrequencyPerMonthReport


def determineAndCreateReport(report_num, startDate='', endDate=''):
    """Determine the report"""
    return availableReports[report_num](startDate, endDate)
