""" Visualizing Climate Change against Education

visualize_data.py

A module that serves to visualize the two datasets and computations done on them using plotly.

written by Kenneth Tran

"""

import math

from typing import Dict, List

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_classes import ClimateData, EducationData, EducationAttainment
import compute_data


def plot_two_scatter_plots(xa_points: list, ya_points: list,
                           xb_points: list, yb_points: list,
                           name_a: str, name_b: str,
                           title: str, xaxis_title: str) -> None:
    """Given two sets of data, plot them together as two scatter plots with plotly.
    """

    fig = make_subplots(2, 1)
    fig.add_trace(go.Scatter(x=xa_points, y=ya_points,
                             mode='markers',
                             name=name_a),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=xb_points, y=yb_points,
                             mode='markers',
                             name=name_b),
                  row=2, col=1)

    fig.update_layout(title=title, xaxis_title=xaxis_title)

    fig.show()


def plot_datasets(country_name: str, start_age: int, end_age: int,
                  climate_data: Dict[str, List[ClimateData]],
                  education_data: Dict[str, List[EducationData]],
                  education_attainment: EducationAttainment) -> None:
    """Plots the two datasets as scatter plots with plotly.

    'climate_data' comes in the form of a dict with key of country name and value of list of ClimateData belonging to
    that country.

    This assumes that both datasets have been processed together by calling 'process_data' on them.
    """

    # Get climate data for given country
    converted_climate_data = compute_data.convert_climate_data(country_name, climate_data)
    years = list(converted_climate_data.keys())
    rows_climate = list(converted_climate_data.values())

    avg_temps = [row.avg_temp for row in rows_climate]

    # Get education data for given country
    converted_education_data = compute_data.convert_education_data(country_name, start_age, end_age, education_data)
    rows_education = list(converted_education_data.values())

    attainment = [education_attainment.extract_data(row) for row in rows_education]

    # Plot data
    plot_two_scatter_plots(xa_points=years, ya_points=avg_temps,
                           xb_points=years, yb_points=attainment,
                           name_a='Avg Temp (Celsius)', name_b=education_attainment.value,
                           title=f'{country_name} Climate-Education Attainment Relation (Ages {start_age} - {end_age})',
                           xaxis_title='Year')


def plot_datasets_and_linear_regression(country_name: str, start_age: int, end_age: int,
                                        education_attainment: EducationAttainment,
                                        climate_data: Dict[str, List[ClimateData]],
                                        education_data: Dict[str, List[EducationData]]) -> None:
    """Plots a linear regression with the raw data.
    """

    relation = compute_data.create_data_relation(country_name, start_age, end_age,
                                                 education_attainment, climate_data, education_data)
    x_points, y_points = relation

    a, b = compute_data.calculate_linear_regression(x_points, y_points)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x_points,
                             y=y_points,
                             mode='markers',
                             name=f'(Avg Temperature, {education_attainment.value})'))

    start_x = math.floor(min(x_points))
    end_x = math.ceil(max(x_points))

    fig.add_trace(go.Scatter(x=[start_x, end_x],
                             y=[a + b * start_x, a + b * end_x],
                             mode='lines',
                             name='Regression Line'))

    fig.update_layout(title=f'{country_name}: Average Temperature (Celsius) compared to {education_attainment.value}',
                      xaxis_title='Average Temperature (Celsius)',
                      yaxis_title=education_attainment.value)

    fig.show()
