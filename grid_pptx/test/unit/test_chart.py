import pytest

import pandas as pd
import numpy as np
from grid_pptx.components import chart
from grid_pptx import GridSlide, GridPresentation, Row, Column


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
        'df', 'chart_type', 'chart_data', 'x_axis', 'y_axis'
    ]

    chartclass = chart.LineChart

    @pytest.fixture
    def mygridpresentation(self):
        return GridPresentation()

    @pytest.fixture
    def mychart(self, main_df, mygridpresentation):
        c = self.chartclass(df=main_df, title='chart title')
        design = Row(12, c)
        s = mygridpresentation.add_slide(layout_num=5, design=design, title='testing')

        return c

    # @pytest.fixture
    # def mygridslide(self, mygridpresentation, mychart):
    #
    #     return mygridpresentation.add_slide(layout_num=5, design=design, title='testing')

    def test_chart_has_expected_attr(self, mychart):
        """ Test that instantiated AreaChart object has (at a minimum) all expected attributes

        :param area_chart: PyTest fixture with an instantiated Chart object
        """
        print('Missing attributes: ', *[_ for _ in self.list_of_attributes if _ not in mychart.__dict__])
        assert all(hasattr(mychart, attr) for attr in self.list_of_attributes)

    def test_minor_tickmarks(self, mychart):
        # setting minor_tick_marks should set the attribute for the chart on the python-pptx slide
        mychart.x_axis.minor_tick_marks = 'inside'
        assert mychart.x_axis.axis.minor_tick_mark == chart.ChartAxis.tick_mark_options['inside']

        # accessing the minor_tick_marks should return the corresponding value of the python-pptx chart
        assert mychart.x_axis.minor_tick_marks == 'inside'

    def test_major_tickmarks(self, mychart):
        # setting major_tick_marks should set the attribute for the chart on the python-pptx slide
        mychart.x_axis.major_tick_marks = 'inside'
        assert mychart.x_axis.axis.major_tick_mark == chart.ChartAxis.tick_mark_options['inside']

        # accessing the major_tick_marks should return the corresponding value of the python-pptx chart
        assert mychart.x_axis.major_tick_marks == 'inside'

    def test_minor_gridlines(self, mychart):
        # setting minor gridlines should set the attribute for the chart on the python-pptx slide
        mychart.x_axis.has_minor_gridlines = True
        assert mychart.x_axis.axis.has_minor_gridlines is True

        # accessing the has_minor_gridelines attribute should return the corresponding value of the python-pptx chart
        assert mychart.x_axis.has_minor_gridlines is True

        # check the same things for False
        mychart.x_axis.has_minor_gridlines = False
        assert mychart.x_axis.axis.has_minor_gridlines is False
        assert mychart.x_axis.has_minor_gridlines is False

    def test_major_gridlines(self, mychart):
        # setting major gridlines should set the attribute for the chart on the python-pptx slide
        mychart.x_axis.has_major_gridlines = True
        assert mychart.x_axis.axis.has_major_gridlines is True

        # accessing the has_major_gridelines attribute should return the corresponding value of the python-pptx chart
        assert mychart.x_axis.has_major_gridlines is True

        # check the same things for False
        mychart.x_axis.has_major_gridlines = False
        assert mychart.x_axis.axis.has_major_gridlines is False
        assert mychart.x_axis.has_major_gridlines is False

    def test_tick_label_position(self, mychart):
        # setting minor_tick_marks should set the attribute for the chart on the python-pptx slide
        mychart.x_axis.tick_label_position = 'high'
        assert mychart.x_axis.axis.tick_label_position == chart.ChartAxis.tick_label_positions['high']

        # accessing the minor_tick_marks should return the corresponding value of the python-pptx chart
        assert mychart.x_axis.tick_label_position == 'high'

    def test_tick_label_italic(self, mychart):
        # setting tick_label_italic should set the attribute for the chart on the python-pptx slide
        mychart.x_axis.tick_label_italic = True
        assert mychart.x_axis.axis.tick_labels.font.italic is True

        # accessing the tick_label_italic attribute should return the corresponding value of the python-pptx chart
        assert mychart.x_axis.tick_label_italic is True

        # check the same things for False
        mychart.x_axis.tick_label_italic = False
        assert mychart.x_axis.axis.tick_labels.font.italic is False
        assert mychart.x_axis.tick_label_italic is False

    def test_tick_label_fontsize(self, mychart):
        # setting tick_label_italic should set the attribute for the chart on the python-pptx slide
        mychart.x_axis.tick_label_fontsize = 10
        assert mychart.x_axis.axis.tick_labels.font.size.pt == 10

        # accessing the tick_label_italic attribute should return the corresponding value of the python-pptx chart
        assert mychart.x_axis.tick_label_fontsize == 10

    def test_chart_title(self, mychart):
        # setting title should set the attribute for the chart on the python-pptx slide
        mychart.title = 'new chart title'
        assert mychart.chart.chart_title.text_frame.text == 'new chart title'

        # accessing the title attribute should return the corresponding value of the python-pptx chart
        assert mychart.title == 'new chart title'

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
    def test_add_to_slide(self):
        assert True


class TestAreaChart(TestChart):
    chartclass = chart.AreaChart

    def test_set_chart_type_3d_stacked_normalized(self, mychart):
        assert True

    def test_set_chart_type_3d_stacked(self, mychart):
        assert True

class TestBarChart(TestChart):
    chartclass = chart.BarChart


class TestColumnChart(TestChart):
    chartclass = chart.ColumnChart


# class TestPieChart(TestChart):
#     chartclass = chart.PieChart
#
#
class TestRadarChart(TestChart):
    chartclass = chart.RadarChart


# class TestScatterChart(TestChart):
#     chartclass = chart.ScatterChart


# class TestBubbleChart(TestChart):
#     chartclass = chart.BubbleChart


# class TestStockChart(TestChart):
#     chartclass = chart.StockChart


# class TestSurfaceChart(TestChart):
#     chartclass = chart.SurfaceChart
