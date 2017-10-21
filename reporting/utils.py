"""
Utility functions for reports
"""

from .reports import FamilyTotalOverTimeReport, DependentsTotalOverTimeReport
from .reports import FamilyCheckoutsPerWeekReport, DependentCheckoutsPerWeekReport
from .reports import EmptyFamilyCheckoutsPerWeekReport
from .reports import ItemsPerCategoryPerMonthReport, IndividualsByAgeReport
from .reports import FamiliesPerZipReport, CheckoutFrequencyPerMonthReport
from .reports import VolunteersHoursWorkedReport

availableReports = {}
availableReports[1] = FamilyTotalOverTimeReport
availableReports[2] = DependentsTotalOverTimeReport
availableReports[3] = FamilyCheckoutsPerWeekReport
availableReports[4] = EmptyFamilyCheckoutsPerWeekReport
availableReports[5] = DependentCheckoutsPerWeekReport
availableReports[6] = ItemsPerCategoryPerMonthReport
availableReports[7] = IndividualsByAgeReport
availableReports[8] = FamiliesPerZipReport
availableReports[9] = CheckoutFrequencyPerMonthReport
availableReports[10] = VolunteersHoursWorkedReport


def determineAndCreateReport(report_num, startDate='', endDate=''):
    """Determine the report"""
    return availableReports[report_num](startDate, endDate)
