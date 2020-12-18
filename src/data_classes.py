""" Visualizing Climate Change against Education

data_classes.py

A module that defines the main classes that are used in this program.

written by Kenneth Tran

"""

from dataclasses import dataclass
from enum import Enum


class WrongFileError(Exception):
    """Exception raised when attempting to load the wrong file.

    Attributes:
        - filename: The name of the file causing this error
    """

    def __init__(self, filename) -> None:
        self.filename = filename

    def __str__(self) -> str:
        """Return a string representation of this error."""
        return f'File {self.filename} does not match the expected format.'


@dataclass
class EducationData:
    """A data class representing one row of data from the Barro-Lee Educational Attainment Dataset.

    Attributes:
        - country: The name of the country pertaining to this row of data
        - year: The year pertaining to this row of data
        - age_from: The starting age of the population pertaining to this row of
        - age_to: The ending age of the population pertaining to this row of data
        - percent_no_schooling: The percentage of the population this row represents with no schooling
        - percent_primary_schooling: The percentage of the population this row represents with (some) primary schooling
        - percent_complete_primary_schooling: The percentage of the population this row represents that
                                                completed primary schooling
        - percent_secondary_schooling: The percentage of the population this row represents with
                                                (some) secondary schooling
        - percent_complete_secondary_schooling: The percentage of the population this row represents that
                                                completed secondary schooling
        - percent_tertiary_schooling: The percentage of the population this row represents with
                                                (some) tertiary schooling
        - percent_complete_tertiary_schooling: The percentage of the population this row represents that
                                                completed tertiary schooling
        - avg_years_schooling: The average number of years of schooling attained
        - avg_years_primary_schooling: The average number of years of schooling attained
        - avg_years_secondary_schooling: The average number of years of schooling attained
        - avg_years_tertiary_schooling: The average number of years of schooling attained
    """
    country: str
    year: int
    age_from: int
    age_to: int
    percent_no_schooling: float
    percent_primary_schooling: float
    percent_complete_primary_schooling: float
    percent_secondary_schooling: float
    percent_complete_secondary_schooling: float
    percent_tertiary_schooling: float
    percent_complete_tertiary_schooling: float
    avg_years_schooling: float
    avg_years_primary_schooling: float
    avg_years_secondary_schooling: float
    avg_years_tertiary_schooling: float


@dataclass
class ClimateData:
    """ A data class representing one row of data from the Global Average Land Temperature by Country dataset.

    Attributes:
        - country: The name of the country pertaining to this row of data
        - year: The year pertaining to this row of data (in multiples of 5)
        - avg_temp: The average temperature in celsius of the past 5 years to this year
    """
    country: str
    year: int
    avg_temp: float


class EducationAttainment(Enum):
    """A class to represent enum values of types of education attainment."""
    PERCENT_NO_SCHOOLING = 'Percentage of No Schooling'
    PERCENT_PRIMARY_SCHOOLING = 'Percentage of Primary Schooling'
    PERCENT_COMPLETE_PRIMARY_SCHOOLING = 'Percentage of Complete Primary Schooling'
    PERCENT_SECONDARY_SCHOOLING = 'Percentage of Secondary Schooling'
    PERCENT_COMPLETE_SECONDARY_SCHOOLING = 'Percentage of Complete Secondary Schooling'
    PERCENT_TERTIARY_SCHOOLING = 'Percentage of Tertiary Schooling'
    PERCENT_COMPLETE_TERTIARY_SCHOOLING = 'Percentage of Complete Tertiary Schooling'
    AVERAGE_YEARS_SCHOOLING = 'Average Years of Schooling'
    AVERAGE_YEARS_PRIMARY_SCHOOLING = 'Average Years of Primary Schooling'
    AVERAGE_YEARS_SECONDARY_SCHOOLING = 'Average Years of Secondary Schooling'
    AVERAGE_YEARS_TERTIARY_SCHOOLING = 'Average Years of Tertiary Schooling'

    def extract_data(self, data: EducationData) -> float:
        """Extract the value of the education attainment from an EducationData object."""

        if self is EducationAttainment.PERCENT_NO_SCHOOLING:
            return data.percent_no_schooling
        elif self is EducationAttainment.PERCENT_PRIMARY_SCHOOLING:
            return data.percent_primary_schooling
        elif self is EducationAttainment.PERCENT_COMPLETE_PRIMARY_SCHOOLING:
            return data.percent_complete_primary_schooling
        elif self is EducationAttainment.PERCENT_SECONDARY_SCHOOLING:
            return data.percent_secondary_schooling
        elif self is EducationAttainment.PERCENT_COMPLETE_SECONDARY_SCHOOLING:
            return data.percent_complete_secondary_schooling
        elif self is EducationAttainment.PERCENT_TERTIARY_SCHOOLING:
            return data.percent_tertiary_schooling
        elif self is EducationAttainment.PERCENT_COMPLETE_TERTIARY_SCHOOLING:
            return data.percent_complete_tertiary_schooling
        elif self is EducationAttainment.AVERAGE_YEARS_SCHOOLING:
            return data.avg_years_schooling
        elif self is EducationAttainment.AVERAGE_YEARS_PRIMARY_SCHOOLING:
            return data.avg_years_primary_schooling
        elif self is EducationAttainment.AVERAGE_YEARS_SECONDARY_SCHOOLING:
            return data.avg_years_secondary_schooling
        elif self is EducationAttainment.AVERAGE_YEARS_TERTIARY_SCHOOLING:
            return data.avg_years_tertiary_schooling
