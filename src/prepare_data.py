""" Visualizing Climate Change against Education

data_processor.py

A module that serves to read the raw datasets, and process and filter them so they are ready
for computations.

written by Kenneth Tran

"""

from typing import List, Tuple, Set, Dict
import csv

from data_classes import EducationData, ClimateData, WrongFileError


def read_raw_education_data(filename: str) -> Dict[str, List[EducationData]]:
    """ Reads the data from the Barro-Lee Educational Attainment dataset and returns
    a dict with key of country name and value of list of EducationData that each
    represent one row of raw data.

    The file should be in csv format.
    """
    with open(filename) as file:
        reader = csv.reader(file)

        # Read the header to check if this is the correct file
        header = next(reader)

        if header != 'BLcode,country,year,sex,agefrom,ageto,lu,lp,lpc,ls,lsc,lh,lhc,' \
                     'yr_sch,yr_sch_pri,yr_sch_sec,yr_sch_ter,pop,WBcode,region_code'.split(','):
            raise WrongFileError(filename)

        data_so_far = {}

        for row in reader:
            country = row[1]
            year = int(row[2])
            age_from = int(row[4])
            age_to = int(row[5])
            percent_no_schooling = float(row[6])
            percent_primary_schooling = float(row[7])
            percent_complete_primary_schooling = float(row[8])
            percent_secondary_schooling = float(row[9])
            percent_complete_secondary_schooling = float(row[10])
            percent_tertiary_schooling = float(row[11])
            percent_complete_tertiary_schooling = float(row[12])
            avg_years_schooling = float(row[13])
            avg_years_primary_schooling = float(row[14])
            avg_years_secondary_schooling = float(row[15])
            avg_years_tertiary_schooling = float(row[16])

            data = EducationData(country=country, year=year, age_from=age_from, age_to=age_to,
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

            if country not in data_so_far:
                data_so_far[country] = [data]
            else:
                data_so_far[country].append(data)

        return data_so_far


def read_raw_climate_data(filename: str) -> Dict[str, List[ClimateData]]:
    """ Reads the data from Berkley Earth's Global Average Land Temperature dataset and returns
    a dict of key of country and value of list of ClimateData instances that each represent one row of data.

    The file should be in csv format.
    """
    with open(filename) as file:
        reader = csv.reader(file)

        # Read the header to check if this is the correct file
        header = next(reader)

        if header != 'dt,AverageTemperature,AverageTemperatureUncertainty,Country'.split(','):
            raise WrongFileError(f'File {filename} does not match the expected format.')

        data_so_far = {}

        for row in reader:
            # Skip this row if missing data
            if row[1] == '':
                continue

            country = row[3]
            year = int(row[0][0:4])
            avg_temp = float(row[1])

            data = ClimateData(country, year, avg_temp)

            if country not in data_so_far:
                data_so_far[country] = [data]
            else:
                data_so_far[country].append(data)

        return data_so_far


def filter_education_data(education_data: Dict[str, List[EducationData]], countries: Set[str], years: Set[int]) ->\
        Dict[str, List[EducationData]]:
    """Return a dict with key of country name and value of list of EducationData with only rows that contain
    countries and years from the given sets.

    'climate_data' comes in the form of a dict with key of country name and value of list of ClimateData belonging to
    that country.
    """
    filtered_education_data = {}

    for country in countries:
        for row in education_data[country]:
            if row.year in years:
                if country not in filtered_education_data:
                    filtered_education_data[country] = [row]
                else:
                    filtered_education_data[country].append(row)

    return filtered_education_data


def filter_climate_data(climate_data: Dict[str, List[ClimateData]], countries: Set[str], years: Set[int]) ->\
        Dict[str, List[ClimateData]]:
    """Return a dict with key of country name and value of list of ClimateData with only rows that contain
    countries and years from the given sets.

    'climate_data' comes in the form of a dict with key of country name and value of list of ClimateData belonging to
    that country.
    """
    filtered_climate_data = {}

    for country in countries:
        for row in climate_data[country]:
            if row.year in years:
                if country not in filtered_climate_data:
                    filtered_climate_data[country] = [row]
                else:
                    filtered_climate_data[country].append(row)

    return filtered_climate_data


def calculate_yearly_avgs(climate_data: Dict[str, List[ClimateData]]) -> Dict[str, List[ClimateData]]:
    """Return a dict of key of country name and value of lists of of ClimateData with unique years
    after calculating the average temperature of the sum of all rows with the same year.
    """
    filtered_climate_data = {}

    for country in climate_data:
        year_mapping = {}

        for row in climate_data[country]:
            if row.year not in year_mapping:
                year_mapping[row.year] = [row]
            else:
                year_mapping[row.year].append(row)

        # Calculate the average temperature for rows of the same year
        # This results in every row of data having unique years
        for year in year_mapping:
            rows = year_mapping[year]

            avg_so_far = 0

            for row in rows:
                avg_so_far += row.avg_temp

            avg_so_far /= len(rows)

            # Create a new instance of ClimateData with the calculated yearly average temperature
            new_row = ClimateData(country=country, year=year, avg_temp=avg_so_far)

            if country not in filtered_climate_data:
                filtered_climate_data[country] = [new_row]
            else:
                filtered_climate_data[country].append(new_row)

    return filtered_climate_data


def process_data(education_data: Dict[str, List[EducationData]], climate_data: Dict[str, List[ClimateData]]) ->\
        Tuple[Dict[str, List[EducationData]], Dict[str, List[ClimateData]]]:
    """Return a tuple of the two dicts of key of country name and value of lists of data (in the original order)
    after filtering them and calculating yearly averages for the ClimateData.
    """
    education_countries = set(education_data.keys())
    climate_countries = set(climate_data.keys())
    filtered_countries = set.intersection(education_countries, climate_countries)

    education_years = {data.year for country in education_data for data in education_data[country]}
    climate_years = {data.year for country in climate_data for data in climate_data[country]}
    filtered_years = set.intersection(education_years, climate_years)

    # Filter the education data
    filtered_education_data = filter_education_data(education_data, filtered_countries, filtered_years)

    # Filter the climate data
    filtered_climate_data = filter_climate_data(climate_data, filtered_countries, filtered_years)

    # Calculate the average temperature for rows of the same year
    filtered_climate_data = calculate_yearly_avgs(filtered_climate_data)

    return (filtered_education_data, filtered_climate_data)
