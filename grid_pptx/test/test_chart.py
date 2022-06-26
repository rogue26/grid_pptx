import pytest

import pandas as pd
from grid_pptx.components.chart import Chart


@pytest.fixture
def test_chart():
    df1 = pd.DataFrame({'a': [1, 2, 3], 'b': [9, 8, 7], 'c': [7, 3, 3]})
    return Chart(df=df1)


class TestChart:
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
