import pytest

import pandas as pd
import numpy as np
from grid_pptx.components import chart


@pytest.fixture
def main_df():
    return pd.DataFrame({'a': [1, 2, 3], 'b': [9, 8, 7], 'c': [7, 3, 3]})


@pytest.fixture
def bad_dfs():
    """
    A list of dfs that should cause the validate_df method to throw a helpful error
    """
    dfs = [
        pd.DataFrame({'a': [1, 2, 'a'], 'b': [9, 8, 7], 'c': [7, 3, 3]}),
    ]

    return dfs


@pytest.fixture
def good_dfs():
    """
    A list of good, but possibly atypical dfs that GridChart methods should be able to work with
    """
    dfs = [
        pd.DataFrame({'a': [1, 2, 3], 'b': [9, 8, 7], 'c': [7, 3, 3]}),
        pd.DataFrame({'a': [1, 2, np.nan], 'b': [9, 8, 7], 'c': [7, 3, 3]})
    ]

    return dfs


# @pytest.fixture(params=chart.GridChart.__subclasses__())
# def mychart(request, main_df):
#     return request.param(df=main_df)
#
#

#
#
# @pytest.fixture(params=chart.GridChart.__subclasses__())
# def mychart_bad_x_axis(request, main_df):
#     x_axis = 'some string'
#     return request.param(df=main_df, x_axis=x_axis)
#
#
# @pytest.fixture(params=chart.GridChart.__subclasses__())
# def mychart_bad_y_axis(request, main_df):
#     y_axis = 'some string'
#     return request.param(df=main_df, y_axis=y_axis)


#
# @pytest.fixture
# def area_chart_bad_axes(main_df):
#     x_axis = 'some string'
#     y_axis = 'some string'
#     return chart.AreaChart(df=main_df, x_axis=x_axis, y_axis=y_axis)  # IDE should warn about types in this instantiation
#

class TestChart:
    list_of_attributes = [
        'df', 'chart_type', 'chart_data', 'has_title', 'has_legend', 'smooth_lines', 'x_axis', 'y_axis'
    ]

    chartclass = chart.GridChart

    @pytest.fixture
    def mychart(self, main_df):
        return self.chartclass(df=main_df)

    @pytest.fixture
    def mychart_manual_axes(self, main_df):
        x_axis = chart.ChartAxis()
        y_axis = chart.ChartAxis()
        return self.chartclass(df=main_df, x_axis=x_axis, y_axis=y_axis)

    def test_chart_has_expected_attr(self, mychart):
        """ Test that instantiated AreaChart object has (at a minimum) all expected attributes

        :param area_chart: PyTest fixture with an instantiated Chart object
        :return:
        """

        # check if chart object has all expected attributes
        print('Missing attributes: ', *[_ for _ in self.list_of_attributes if _ not in mychart.__dict__])
        assert all(hasattr(mychart, attr) for attr in self.list_of_attributes)

    def test_chart_manual_axes(self, mychart_manual_axes):
        assert isinstance(mychart_manual_axes.x_axis, chart.ChartAxis)
        assert isinstance(mychart_manual_axes.y_axis, chart.ChartAxis)

    def test_chart_bad_axes(self, main_df):
        # check if helpful error is thrown if x_axis or y_axis are provided, but not ChartAxis objects
        with pytest.raises(ValueError, match=r'.*must be an instance of ChartAxis or left blank.'):
            self.chartclass(df=main_df, x_axis='some string')

        with pytest.raises(ValueError, match=r'.*must be an instance of ChartAxis or left blank.'):
            self.chartclass(df=main_df, y_axis='some string')

    # check that chart object has only expected attributesthe
    # assert all(attr in test_chart.__dict__.keys() for attr in list_of_attributes)

    # def test_evaluate_dataframe(self):
    #     assert True
    #
    # def test_set_chart_data_type(self):
    #     assert True
    #
    # def test_prep_chart_data(self):
    #     assert True
    #
    # def test_add_to_slide(self):
    #     assert True


class TestAreaChart(TestChart):
    chartclass = chart.AreaChart


class TestBarChart(TestChart):
    chartclass = chart.BarChart


class TestColumnChart(TestChart):
    chartclass = chart.ColumnChart


class TestLineChart(TestChart):
    chartclass = chart.LineChart


class TestPieChart(TestChart):
    chartclass = chart.PieChart


class TestRadarChart(TestChart):
    chartclass = chart.RadarChart


# class TestScatterChart(TestChart):
#     chartclass = chart.ScatterChart


# class TestBubbleChart(TestChart):
#     chartclass = chart.BubbleChart


class TestStockChart(TestChart):
    chartclass = chart.StockChart


class TestSurfaceChart(TestChart):
    chartclass = chart.SurfaceChart
