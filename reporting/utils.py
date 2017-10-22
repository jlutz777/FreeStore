"""
Utility functions for reports
"""

from .reports import FamilyTotalOverTimeReport, DependentsTotalOverTimeReport
from .reports import FamilyCheckoutsPerWeekReport, DependentCheckoutsPerWeekReport
from .reports import EmptyFamilyCheckoutsPerWeekReport, FamilyCheckInsPerWeekReport
from .reports import ItemsPerCategoryPerMonthReport, IndividualsByAgeReport
from .reports import FamiliesPerZipReport, CheckoutFrequencyPerMonthReport
from .reports import VolunteersHoursWorkedReport

availableReports = {}
availableReports[1] = FamilyTotalOverTimeReport
availableReports[2] = DependentsTotalOverTimeReport
availableReports[3] = FamilyCheckoutsPerWeekReport
availableReports[4] = EmptyFamilyCheckoutsPerWeekReport
availableReports[5] = FamilyCheckInsPerWeekReport
availableReports[6] = DependentCheckoutsPerWeekReport
availableReports[7] = ItemsPerCategoryPerMonthReport
availableReports[8] = IndividualsByAgeReport
availableReports[9] = FamiliesPerZipReport
availableReports[10] = CheckoutFrequencyPerMonthReport
availableReports[11] = VolunteersHoursWorkedReport


def determineAndCreateReport(report_num, startDate='', endDate=''):
    """Determine the report"""
    return availableReports[report_num](startDate, endDate)
