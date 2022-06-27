import pytest

import pandas as pd
from grid_pptx.components import chart


@pytest.fixture
def test_chart():
    df1 = pd.DataFrame({'a': [1, 2, 3], 'b': [9, 8, 7], 'c': [7, 3, 3]})
    return chart.Chart(df=df1)


class TestChart:
    def test_init_has_values(self):

        list_of_attributes = [
            'df', 'chart_type', 'chart_data', 'has_title', 'has_legend', 'smooth_lines', 'x_minor_tick_marks',
            'x_major_tick_marks', 'x_has_minor_gridlines', 'x_has_major_gridlines', 'x_tick_label_position',
            'x_tick_label_italic', 'x_tick_label_fontsize', 'y_minor_tick_marks', 'y_major_tick_marks',
            'y_has_minor_gridlines', 'y_has_major_gridlines', 'y_tick_label_position', 'y_tick_label_italic',
            'y_tick_label_fontsize']

        # check if chart object has all expected attributes
        assert all(hasattr(test_chart, attr) for attr in list_of_attributes)

        # check that chart object has only expected attributes
        # assert all(attr in test_chart.__dict__.keys() for attr in list_of_attributes)


    def test_evaluate_dataframe(self):
        assert True

    def test_set_chart_data_type(self):
        assert True

    def test_prep_chart_data(self):
        assert True

    def test_add_to_slide(self):
        assert True


class TestAreaChart:
    def test_area_chart(self):
        assert True


class TestBarChart:
    def test_bar_chart(self):
        assert True


class TestColumnChart:
    def test_column_chart(self):
        assert True


class TestLineChart:
    def test_line_chart(self):
        assert True


class TestPieChart:
    def test_pie_chart(self):
        assert True


class TestRadarChart:
    def test_radar_chart(self):
        assert True


class TestScatterChart:
    def test_set_chart_data_type(self):
        assert True

    def test_prep_chart_data(self):
        assert True


class TestBubbleChart:
    def test_set_chart_data_type(self):
        assert True


class TestStockChart:
    def test_stock_chart(self):
        assert True


class TestSurfaceChart:
    def test_surface_chart(self):
        assert True
