from __future__ import annotations
from typing import TYPE_CHECKING
from .panel import GridPanel

from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_TICK_MARK, XL_TICK_LABEL_POSITION
from pptx.util import Pt

# imports for type hints that would normally cause circular imports
if TYPE_CHECKING:
    from grid_pptx import GridSlide


class Chart(GridPanel):
    chart_type = XL_CHART_TYPE.LINE

    tick_mark_options = {
        'none': XL_TICK_MARK.NONE,
        'cross': XL_TICK_MARK.CROSS,
        'inside': XL_TICK_MARK.INSIDE,
        'outside': XL_TICK_MARK.OUTSIDE,
    }

    tick_label_positions = {
        'high': XL_TICK_LABEL_POSITION.HIGH,
        'low': XL_TICK_LABEL_POSITION.LOW,
        'next_to_axis': XL_TICK_LABEL_POSITION.NEXT_TO_AXIS,
        'none': XL_TICK_LABEL_POSITION.NONE,
    }

    def __init__(self, *, df, **kwargs) -> None:
        super().__init__(**kwargs)

        self.df = df

        self.chart_data = CategoryChartData()

        # default chart parameters
        self.has_title = False
        self.has_legend = False
        self.smooth_lines = False

        self.x_minor_tick_marks = 'none'  # options are 'none', 'cross', 'inside', 'outside
        self.x_major_tick_marks = 'none'  # options are 'none', 'cross', 'inside', 'outside
        self.x_has_minor_gridlines = False
        self.x_has_major_gridlines = False
        self.x_tick_label_position = 'none'
        self.x_tick_label_italic = False
        self.x_tick_label_fontsize = 16

        self.y_minor_tick_marks = 'none'  # options are 'none', 'cross', 'inside', 'outside'
        self.y_major_tick_marks = 'none'  # options are 'none', 'cross', 'inside', 'outside'
        self.y_has_minor_gridlines = False
        self.y_has_major_gridlines = False
        self.y_tick_label_position = 'none'  # options are 'none', 'high', 'low', 'next_to_axis'
        self.y_tick_label_italic = False
        self.y_tick_label_fontsize = 16

        # set any attributes that have been supplied in kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

        # prep chart data
        self.prep_chart_data()

    def prep_chart_data(self):
        self.chart_data.categories = self.df.index
        for column in self.df.columns:
            self.chart_data.add_series(column, self.df[column])

    def add_to_slide(self, gridslide: GridSlide) -> None:
        slide = gridslide.slide
        chart = slide.shapes.add_chart(
            self.chart_type, self.x, self.y, self.cx, self.cy, self.chart_data
        ).chart

        # format chart
        chart.has_title = self.has_title
        chart.has_legend = self.has_legend
        chart.series[0].smooth = self.smooth_lines

        # format y-axis
        y_axis = chart.value_axis
        y_axis.minor_tick_mark = self.tick_mark_options[self.x_minor_tick_marks]
        y_axis.major_tick_mark = self.tick_mark_options[self.x_major_tick_marks]
        y_axis.has_minor_gridlines = self.x_has_minor_gridlines
        y_axis.has_major_gridlines = self.x_has_major_gridlines
        y_axis.tick_label_position = self.tick_label_positions[self.x_tick_label_position]
        y_axis.tick_labels.font.italic = self.y_tick_label_italic
        y_axis.tick_labels.font.size = Pt(self.y_tick_label_fontsize)

        # format x-axis
        x_axis = chart.category_axis
        x_axis.minor_tick_mark = self.tick_mark_options[self.y_minor_tick_marks]
        x_axis.major_tick_mark = self.tick_mark_options[self.y_major_tick_marks]
        x_axis.has_minor_gridlines = self.y_has_minor_gridlines
        x_axis.has_major_gridlines = self.y_has_major_gridlines
        x_axis.tick_label_position = self.tick_label_positions[self.y_tick_label_position]
        x_axis.tick_labels.font.italic = self.x_tick_label_italic
        x_axis.tick_labels.font.size = Pt(self.x_tick_label_fontsize)

        # x_axis.tick_labels.number_format = '0%'


class LineChart(Chart):
    chart_types = {
        'THREE_D_LINE': XL_CHART_TYPE.THREE_D_LINE,  # 3D Line.
        'LINE': XL_CHART_TYPE.LINE,  # Line.
        'LINE_MARKERS': XL_CHART_TYPE.LINE_MARKERS,  # Line with Markers.
        'LINE_MARKERS_STACKED': XL_CHART_TYPE.LINE_MARKERS_STACKED,  # Stacked Line with Markers.
        'LINE_MARKERS_STACKED_100': XL_CHART_TYPE.LINE_MARKERS_STACKED_100,  # 100% Stacked Line with Markers.
        'LINE_STACKED': XL_CHART_TYPE.LINE_STACKED,  # Stacked Line.
        'LINE_STACKED_100': XL_CHART_TYPE.LINE_STACKED_100,  # 100% Stacked Line.
    }
    chart_type = XL_CHART_TYPE.LINE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AreaChart(Chart):
    chart_types = {
        'THREE_D_AREA': XL_CHART_TYPE.THREE_D_AREA,  # 3D Area.
        'THREE_D_AREA_STACKED': XL_CHART_TYPE.THREE_D_AREA_STACKED,  # 3D Stacked Area.
        'THREE_D_AREA_STACKED_100': XL_CHART_TYPE.THREE_D_AREA_STACKED_100,  # 100% Stacked Area.
        'AREA': XL_CHART_TYPE.AREA,  # Area
        'AREA_STACKED': XL_CHART_TYPE.AREA_STACKED,  # Stacked Area.
        'AREA_STACKED_100': XL_CHART_TYPE.AREA_STACKED_100,  # 100% Stacked Area.
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.three_d = False


class PieChart(Chart):
    chart_types = {
        'THREE_D_PIE': XL_CHART_TYPE.THREE_D_PIE,  # 3D Pie.
        'THREE_D_PIE_EXPLODED': XL_CHART_TYPE.THREE_D_PIE_EXPLODED,  # Exploded 3D Pie.
        'DOUGHNUT': XL_CHART_TYPE.DOUGHNUT,  # Doughnut.
        'DOUGHNUT_EXPLODED': XL_CHART_TYPE.DOUGHNUT_EXPLODED,  # Exploded Doughnut.
        'PIE': XL_CHART_TYPE.PIE,  # Pie.
        'PIE_EXPLODED': XL_CHART_TYPE.PIE_EXPLODED,  # Exploded Pie.
        'PIE_OF_PIE': XL_CHART_TYPE.PIE_OF_PIE,  # Pie of Pie.
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class BarChart(Chart):
    chart_types = {
        'THREE_D_BAR_CLUSTERED': XL_CHART_TYPE.THREE_D_BAR_CLUSTERED,  # 3D Clustered Bar.
        'THREE_D_BAR_STACKED': XL_CHART_TYPE.THREE_D_BAR_STACKED,  # 3D Stacked Bar.
        'THREE_D_BAR_STACKED_100': XL_CHART_TYPE.THREE_D_BAR_STACKED_100,  # 3D 100% Stacked Bar.
        'BAR_CLUSTERED': XL_CHART_TYPE.BAR_CLUSTERED,  # Clustered Bar.
        'BAR_OF_PIE': XL_CHART_TYPE.BAR_OF_PIE,  # Bar of Pie.
        'BAR_STACKED': XL_CHART_TYPE.BAR_STACKED,  # Stacked Bar.
        'BAR_STACKED_100': XL_CHART_TYPE.BAR_STACKED_100,  # 100% Stacked Bar.
        'CONE_BAR_CLUSTERED': XL_CHART_TYPE.CONE_BAR_CLUSTERED,  # Clustered Cone Bar.
        'CONE_BAR_STACKED': XL_CHART_TYPE.CONE_BAR_STACKED,  # Stacked Cone Bar.
        'CONE_BAR_STACKED_100': XL_CHART_TYPE.CONE_BAR_STACKED_100,  # 100% Stacked Cone Bar.
        'CYLINDER_BAR_CLUSTERED': XL_CHART_TYPE.CYLINDER_BAR_CLUSTERED,  # Clustered Cylinder Bar.
        'CYLINDER_BAR_STACKED': XL_CHART_TYPE.CYLINDER_BAR_STACKED,  # Stacked Cylinder Bar.
        'CYLINDER_BAR_STACKED_100': XL_CHART_TYPE.CYLINDER_BAR_STACKED_100,  # 100% Stacked Cylinder Bar.
        'PYRAMID_BAR_CLUSTERED': XL_CHART_TYPE.PYRAMID_BAR_CLUSTERED,  # Clustered Pyramid Bar.
        'PYRAMID_BAR_STACKED': XL_CHART_TYPE.PYRAMID_BAR_STACKED,  # Stacked Pyramid Bar.
        'PYRAMID_BAR_STACKED_100': XL_CHART_TYPE.PYRAMID_BAR_STACKED_100,  # 100% Stacked Pyramid Bar.
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ColumnChart(Chart):
    chart_types = {
        'THREE_D_COLUMN': XL_CHART_TYPE.THREE_D_COLUMN,  # 3D Column.
        'THREE_D_COLUMN_CLUSTERED': XL_CHART_TYPE.THREE_D_COLUMN_CLUSTERED,  # 3D Clustered Column.
        'THREE_D_COLUMN_STACKED': XL_CHART_TYPE.THREE_D_COLUMN_STACKED,  # 3D Stacked Column.
        'THREE_D_COLUMN_STACKED_100': XL_CHART_TYPE.THREE_D_COLUMN_STACKED_100,  # 3D 100% Stacked Column.
        'COLUMN_CLUSTERED': XL_CHART_TYPE.COLUMN_CLUSTERED,  # Clustered Column.
        'COLUMN_STACKED': XL_CHART_TYPE.COLUMN_STACKED,  # Stacked Column.
        'COLUMN_STACKED_100': XL_CHART_TYPE.COLUMN_STACKED_100,  # 100% Stacked Column.
        'CONE_COL': XL_CHART_TYPE.CONE_COL,  # 3D Cone Column.
        'CONE_COL_CLUSTERED': XL_CHART_TYPE.CONE_COL_CLUSTERED,  # Clustered Cone Column.
        'CONE_COL_STACKED': XL_CHART_TYPE.CONE_COL_STACKED,  # Stacked Cone Column.
        'CONE_COL_STACKED_100': XL_CHART_TYPE.CONE_COL_STACKED_100,  # 100% Stacked Cone Column.
        'CYLINDER_COL': XL_CHART_TYPE.CYLINDER_COL,  # 3D Cylinder Column.
        'CYLINDER_COL_CLUSTERED': XL_CHART_TYPE.CYLINDER_COL_CLUSTERED,  # Clustered Cone Column.
        'CYLINDER_COL_STACKED': XL_CHART_TYPE.CYLINDER_COL_STACKED,  # Stacked Cone Column.
        'CYLINDER_COL_STACKED_100': XL_CHART_TYPE.CYLINDER_COL_STACKED_100,  # 100% Stacked Cylinder Column.
        'PYRAMID_COL': XL_CHART_TYPE.PYRAMID_COL,  # 3D Pyramid Column.
        'PYRAMID_COL_CLUSTERED': XL_CHART_TYPE.PYRAMID_COL_CLUSTERED,  # Clustered Pyramid Column.
        'PYRAMID_COL_STACKED': XL_CHART_TYPE.PYRAMID_COL_STACKED,  # Stacked Pyramid Column.
        'PYRAMID_COL_STACKED_100': XL_CHART_TYPE.PYRAMID_COL_STACKED_100,  # 100% Stacked Pyramid Column.
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SurfaceChart(Chart):
    chart_types = {
        'SURFACE': XL_CHART_TYPE.SURFACE,  # 3D Surface.
        'SURFACE_TOP_VIEW': XL_CHART_TYPE.SURFACE_TOP_VIEW,  # Surface (Top View).
        'SURFACE_TOP_VIEW_WIREFRAME': XL_CHART_TYPE.SURFACE_TOP_VIEW_WIREFRAME,  # Surface (Top View wireframe).
        'SURFACE_WIREFRAME': XL_CHART_TYPE.SURFACE_WIREFRAME,  # 3D Surface (wireframe).
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ScatterChart(Chart):
    chart_types = {
        'XY_SCATTER': XL_CHART_TYPE.XY_SCATTER,  # Scatter.
        'XY_SCATTER_LINES': XL_CHART_TYPE.XY_SCATTER_LINES,  # Scatter with Lines.
        'XY_SCATTER_LINES_NO_MARKERS': XL_CHART_TYPE.XY_SCATTER_LINES_NO_MARKERS,
        # Scatter with Lines and No Data Markers.
        'XY_SCATTER_SMOOTH': XL_CHART_TYPE.XY_SCATTER_SMOOTH,  # Scatter with Smoothed Lines.
        'XY_SCATTER_SMOOTH_NO_MARKERS': XL_CHART_TYPE.XY_SCATTER_SMOOTH_NO_MARKERS,
        # Scatter with Smoothed Lines and No Data Markers.
        'BUBBLE': XL_CHART_TYPE.BUBBLE,  # Bubble.
        'BUBBLE_THREE_D_EFFECT': XL_CHART_TYPE.BUBBLE_THREE_D_EFFECT,  # Bubble with 3D effects.
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class StockChart(Chart):
    chart_types = {
        'STOCK_HLC': XL_CHART_TYPE.STOCK_HLC,  # High-Low-Close.
        'STOCK_OHLC': XL_CHART_TYPE.STOCK_OHLC,  # Open-High-Low-Close.
        'STOCK_VHLC': XL_CHART_TYPE.STOCK_VHLC,  # Volume-High-Low-Close.
        'STOCK_VOHLC': XL_CHART_TYPE.STOCK_VOHLC,  # Volume-Open-High-Low-Close.
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RadarChart(Chart):
    chart_types = {
        'RADAR': XL_CHART_TYPE.RADAR,  # Radar.
        'RADAR_FILLED': XL_CHART_TYPE.RADAR_FILLED,  # Filled Radar.
        'RADAR_MARKERS': XL_CHART_TYPE.RADAR_MARKERS,  # Radar with Data Markers.
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
