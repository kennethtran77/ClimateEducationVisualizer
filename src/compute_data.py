""" Visualizing Climate Change against Education

compute_data.py

A module that proves functions to perform computations on data such as calculating linear regression and predicting
future values.

written by Kenneth Tran

"""

from typing import List, Dict, Tuple
from data_classes import ClimateData, EducationData, EducationAttainment


def convert_climate_data(country_name: str, climate_data: Dict[str, List[ClimateData]]) \
        -> Dict[int, ClimateData]:
    """Convert a dict of key of country name and value of list of ClimateData to a dict with key year and value
    ClimateData.

    This assumes that the climate_data has been processed by calling process_data on it, so that every ClimateData
    instance has a unique year value.
    """
    converted_data = {row.year: row for row in climate_data[country_name]}

    return converted_data


def convert_education_data(country_name: str, start_age: int, end_age: int,
                           education_data: Dict[str, List[EducationData]]) -> Dict[int, EducationData]:
    """Convert a dict of key of country name and value of list of EducationData to a length two tuple
    with first element being a list of years and second element being a list of EducationData corresponding with its
    year and the given country, for the given age range.

    This assumes that education_data has been processed by calling process_data on it.
    """
    year_mapping = {}

    # Categorize rows into years
    for row in education_data[country_name]:
        if start_age <= row.age_from and row.age_to <= end_age:
            if row.year not in year_mapping:
                year_mapping[row.year] = [row]
            else:
                year_mapping[row.year].append(row)

    converted_data = {}

    # Take the average of all education attainment values per year
    for year in year_mapping:
        percent_no_schooling = 0
        percent_primary_schooling = 0
        percent_complete_primary_schooling = 0
        percent_secondary_schooling = 0
        percent_complete_secondary_schooling = 0
        percent_tertiary_schooling = 0
        percent_complete_tertiary_schooling = 0
        avg_years_schooling = 0
        avg_years_primary_schooling = 0
        avg_years_secondary_schooling = 0
        avg_years_tertiary_schooling = 0

        for row in year_mapping[year]:
            percent_no_schooling += row.percent_no_schooling
            percent_primary_schooling += row.percent_primary_schooling
            percent_complete_primary_schooling += row.percent_complete_primary_schooling
            percent_secondary_schooling += row.percent_secondary_schooling
            percent_complete_secondary_schooling += row.percent_complete_secondary_schooling
            percent_tertiary_schooling += row.percent_tertiary_schooling
            percent_complete_tertiary_schooling += row.percent_complete_tertiary_schooling
            avg_years_schooling += row.avg_years_schooling
            avg_years_primary_schooling += row.avg_years_primary_schooling
            avg_years_secondary_schooling += row.avg_years_secondary_schooling
            avg_years_tertiary_schooling += row.avg_years_tertiary_schooling

        percent_no_schooling /= len(year_mapping[year])
        percent_primary_schooling /= len(year_mapping[year])
        percent_complete_primary_schooling /= len(year_mapping[year])
        percent_secondary_schooling /= len(year_mapping[year])
        percent_complete_secondary_schooling /= len(year_mapping[year])
        percent_tertiary_schooling /= len(year_mapping[year])
        percent_complete_tertiary_schooling /= len(year_mapping[year])
        avg_years_schooling /= len(year_mapping[year])
        avg_years_primary_schooling /= len(year_mapping[year])
        avg_years_secondary_schooling /= len(year_mapping[year])
        avg_years_tertiary_schooling /= len(year_mapping[year])

        new_education_data = EducationData(country=country_name, year=year, age_from=start_age, age_to=end_age,
                                           percent_no_schooling=percent_no_schooling,
                                           percent_primary_schooling=percent_primary_schooling,
                                           percent_complete_primary_schooling=percent_complete_primary_schooling,
                                           percent_secondary_schooling=percent_secondary_schooling,
                                           percent_complete_secondary_schooling=percent_complete_secondary_schooling,
                                           percent_tertiary_schooling=percent_tertiary_schooling,
                                           percent_complete_tertiary_schooling=percent_complete_tertiary_schooling,
                                           avg_years_schooling=avg_years_schooling,
                                           avg_years_primary_schooling=avg_years_primary_schooling,
                                           avg_years_secondary_schooling=avg_years_secondary_schooling,
                                           avg_years_tertiary_schooling=avg_years_tertiary_schooling)

        converted_data[year] = new_education_data

    return converted_data


def create_data_relation(country_name: str, start_age: int, end_age: int, education_attainment: EducationAttainment,
                         climate_data: Dict[str, List[ClimateData]], education_data: Dict[str, List[EducationData]]) ->\
        Tuple[List[float], List[float]]:
    """Given two dicts of key of country name and value of list of data, convert the data into a tuple of two lists
     where the first list contains annual temperature and the second list contains education attainment, both
     corresponding to the same year.

    This assumes that both datasets have been processed together by calling 'process_data' on them.
    """

    # Extract years from climate data. Will work with education data since both share the same years
    years = [row.year for row in climate_data[country_name]]

    converted_climate_data = convert_climate_data(country_name, climate_data)
    converted_education_data = convert_education_data(country_name, start_age, end_age, education_data)

    x_points = []
    y_points = []

    for year in years:
        x_points.append(converted_climate_data[year].avg_temp)
        y_points.append(education_attainment.extract_data(converted_education_data[year]))

    return (x_points, y_points)


def calculate_linear_regression(x_points: List[float], y_points: List[float]) -> Tuple[float, float]:
    """Perform a linear regression on the given points.

    Return a pair of floats (a, b) such that y = a + bx is a linear function approximating the data.
    """

    x_average = sum(x_points) / len(x_points)
    y_average = sum(y_points) / len(y_points)

    n = len(x_points)

    # Calculate b
    b_numerator = sum([(x_points[i] - x_average) * (y_points[i] - y_average) for i in range(0, n)])
    b_denominator = sum([(x_points[i] - x_average) ** 2 for i in range(0, n)])

    b = b_numerator / b_denominator

    # Calculate a using the previously calculated b
    a = y_average - b * x_average

    return (a, b)
