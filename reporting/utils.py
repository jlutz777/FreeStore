"""
Utility functions for reports
"""

from .reports import FamilyTotalOverTimeReport, IndividualsByAgeReport
from .reports import FamilyCheckoutsPerWeekReport, DependentCheckoutsPerWeekReport
from .reports import EmptyFamilyCheckoutsPerWeekReport, FamilyCheckInsPerWeekReport
from .reports import FamiliesPerZipReport, CheckoutFrequencyPerMonthReport
from .reports import VolunteersHoursWorkedReport
#from .reports import DependentsTotalOverTimeReport, ItemsPerCategoryPerMonthReport

availableReports = {}
availableReports[1] = FamilyTotalOverTimeReport
availableReports[2] = FamilyCheckoutsPerWeekReport
availableReports[3] = EmptyFamilyCheckoutsPerWeekReport
availableReports[4] = FamilyCheckInsPerWeekReport
availableReports[5] = DependentCheckoutsPerWeekReport
availableReports[6] = IndividualsByAgeReport
availableReports[7] = FamiliesPerZipReport
availableReports[8] = CheckoutFrequencyPerMonthReport
availableReports[9] = VolunteersHoursWorkedReport
#availableReports[10] = DependentsTotalOverTimeReport
#availableReports[11] = ItemsPerCategoryPerMonthReport

def determineAndCreateReport(report_num, startDate='', endDate=''):
    """Determine the report"""
    return availableReports[report_num](startDate, endDate)
