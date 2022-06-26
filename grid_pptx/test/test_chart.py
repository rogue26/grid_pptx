import pytest

import pandas as pd
from grid_pptx.components.chart import Chart


@pytest.fixture
def test_chart():
    df1 = pd.DataFrame({'a': [1, 2, 3], 'b': [9, 8, 7], 'c': [7, 3, 3]})
    return Chart(df=df1)


class TestChart:
    def test_evaluate_dataframe(self):
        assert False

    def test_set_chart_data_type(self):
        assert False

    def test_prep_chart_data(self):
        assert False

    def test_add_to_slide(self):
        assert False


class TestAreaChart:
    def test_area_chart(self):
        assert False


class TestBarChart:
    def test_bar_chart(self):
        assert False


class TestColumnChart:
    def test_column_chart(self):
        assert False


class TestLineChart:
    def test_line_chart(self):
        assert False


class TestPieChart:
    def test_pie_chart(self):
        assert False


class TestRadarChart:
    def test_radar_chart(self):
        assert False


class TestScatterChart:
    def test_set_chart_data_type(self):
        assert False

    def test_prep_chart_data(self):
        assert False


class TestBubbleChart:
    def test_set_chart_data_type(self):
        assert False


class TestStockChart:
    def test_stock_chart(self):
        assert False


class TestSurfaceChart:
    def test_surface_chart(self):
        assert False
