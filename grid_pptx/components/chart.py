from __future__ import annotations
from typing import TYPE_CHECKING

import pandas as pd

from pptx.chart.data import CategoryChartData, XyChartData, BubbleChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_TICK_MARK, XL_TICK_LABEL_POSITION
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT
from pptx.util import Pt

from .panel import GridPanel

# imports for type hints that would normally cause circular imports
if TYPE_CHECKING:
    from grid_pptx import GridSlide


class NewInitCaller(type):
    """
    metaclass which overrides the "__call__" function to automatically call "set_chart_dat_type"
    "prep_chart_data" methods after __init__, even if __init__ has been overridden
    """

    def __call__(cls, *args, **kwargs):
        """Called when you call MyNewClass() """
        obj = type.__call__(cls, *args, **kwargs)
        obj.set_chart_data_type()
        obj.prep_chart_data()
        return obj


class Chart(GridPanel, metaclass=NewInitCaller):
    """
    Base class for all charts
    """

    #: Options for tick mark placement on either the x or y axes. Values are the constants
    #: used in the python-pptx package, but are used in the code as ``XL_CHART_TYPE.LINE``, etc.
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

    def __init__(self, *, df: pd.DataFrame, **kwargs) -> None:
        """

        :param df: Pandas dataframe containing data for the chart.
        :param kwargs:
        """
        super().__init__(**kwargs)

        self.df = df
        self.chart_type = None
        self.chart_data = None

        # default chart parameters
        self.has_title = False
        self.has_legend = True
        self.smooth_lines = False

        self.x_minor_tick_marks = 'none'  # options are 'none', 'cross', 'inside', 'outside
        self.x_major_tick_marks = 'inside'  # options are 'none', 'cross', 'inside', 'outside
        self.x_has_minor_gridlines = False
        self.x_has_major_gridlines = False
        self.x_tick_label_position = 'next_to_axis'  # options are 'none', 'high', 'low', 'next_to_axis'
        self.x_tick_label_italic = False
        self.x_tick_label_fontsize = 16

        self.y_minor_tick_marks = 'none'  # options are 'none', 'cross', 'inside', 'outside'
        self.y_major_tick_marks = 'inside'  # options are 'none', 'cross', 'inside', 'outside'
        self.y_has_minor_gridlines = False
        self.y_has_major_gridlines = False
        self.y_tick_label_position = 'next_to_axis'  # options are 'none', 'high', 'low', 'next_to_axis'
        self.y_tick_label_italic = False
        self.y_tick_label_fontsize = 16

        # set any attributes that have been supplied in kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

    def set_chart_data_type(self) -> None:
        self.chart_data = CategoryChartData()

    def prep_chart_data(self) -> None:
        """

        :return:
        """
        self.chart_data.categories = self.df.index
        for column in self.df.columns:
            self.chart_data.add_series(column, self.df[column])

    def add_to_slide(self, gridslide: GridSlide) -> None:
        """

        :param gridslide:
        :return:
        """
        slide = gridslide.slide

        # For some chart types, XL_CHART_TYPE.<chart type> returns an EnumValue object that is all that is needed.
        # Sometimes, it returns a tuple with one integer

        chart_rendered = False
        try:
            chart = slide.shapes.add_chart(
                self.chart_type[0], self.x, self.y, self.cx, self.cy, self.chart_data
            ).chart

            chart_rendered = True
        except TypeError:
            chart = slide.shapes.add_chart(
                self.chart_type, self.x, self.y, self.cx, self.cy, self.chart_data
            ).chart

            chart_rendered = True

        except NotImplementedError as ne:
            # not all chart types are implemented in python-pptx
            # https://python-pptx.readthedocs.io/en/latest/dev/analysis/cht-chart-overview.html

            chart = slide.shapes.add_shape(
                MSO_AUTO_SHAPE_TYPE.RECTANGLE, self.x, self.y, self.cx, self.cy
            )

            # configure text
            p = chart.text_frame.paragraphs[0]
            p.alignment = PP_PARAGRAPH_ALIGNMENT.CENTER
            run = p.add_run()
            run.text = str(ne)
            font = run.font
            font.size = Pt(10)

        if chart_rendered:
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


class AreaChart(Chart):

    def __init__(self, df: pd.DataFrame, three_d: bool = False, stacked: bool = False, normalized: bool = False,
                 **kwargs):
        """

        :param df: Pandas dataframe containing data for the chart.
        :param three_d: Whether a 3-D version of the chart should be used
        :param stacked:
        :param normalized:
        :param kwargs:
        """

        super().__init__(df=df, **kwargs)

        if three_d:
            if stacked:
                if normalized:
                    self.chart_type = XL_CHART_TYPE.THREE_D_AREA_STACKED_100
                else:
                    self.chart_type = XL_CHART_TYPE.THREE_D_AREA_STACKED
            else:
                self.chart_type = XL_CHART_TYPE.THREE_D_AREA
        else:
            if stacked:
                if normalized:
                    self.chart_type = XL_CHART_TYPE.AREA_STACKED_100
                else:
                    self.chart_type = XL_CHART_TYPE.AREA_STACKED
            else:
                self.chart_type = XL_CHART_TYPE.AREA


class BarChart(Chart):

    def __init__(self, df: pd.DataFrame, three_d: bool = False, shape: str = 'rectangle', stacked: bool = False,
                 normalized: bool = False,
                 **kwargs):
        """

        :param df: Pandas dataframe containing data for the chart.
        :param three_d: Whether a 3-D version of the chart should be used
        :param shape:
        :param stacked:
        :param normalized:
        :param kwargs:
        """
        super().__init__(df=df, **kwargs)

        if three_d:
            if shape == 'rectangle':
                if stacked:
                    if normalized:
                        self.chart_type = XL_CHART_TYPE.THREE_D_BAR_STACKED_100,
                    else:
                        self.chart_type = XL_CHART_TYPE.THREE_D_BAR_STACKED,
                else:
                    self.chart_type = XL_CHART_TYPE.THREE_D_BAR_CLUSTERED,
            elif shape == 'cone':
                if stacked:
                    if normalized:
                        self.chart_type = XL_CHART_TYPE.CONE_BAR_STACKED_100,
                    else:
                        self.chart_type = XL_CHART_TYPE.CONE_BAR_STACKED,
                else:
                    self.chart_type = XL_CHART_TYPE.CONE_BAR_CLUSTERED,
            elif shape == 'cylinder':
                if stacked:
                    if normalized:
                        self.chart_type = XL_CHART_TYPE.CYLINDER_BAR_STACKED_100,
                    else:
                        self.chart_type = XL_CHART_TYPE.CYLINDER_BAR_STACKED,
                else:
                    self.chart_type = XL_CHART_TYPE.CYLINDER_BAR_CLUSTERED,
            elif shape == 'pyramid':
                if stacked:
                    if normalized:
                        self.chart_type = XL_CHART_TYPE.PYRAMID_BAR_STACKED_100,
                    else:
                        self.chart_type = XL_CHART_TYPE.PYRAMID_BAR_STACKED,
                else:
                    self.chart_type = XL_CHART_TYPE.PYRAMID_BAR_CLUSTERED,
        else:
            if stacked:
                if normalized:
                    self.chart_type = XL_CHART_TYPE.BAR_STACKED_100,
                else:
                    self.chart_type = XL_CHART_TYPE.BAR_STACKED,
            else:
                self.chart_type = XL_CHART_TYPE.BAR_CLUSTERED,


class ColumnChart(Chart):
    chart_types = {
        'THREE_D_COLUMN': XL_CHART_TYPE.THREE_D_COLUMN,  # 3D Column.
        # 'THREE_D_COLUMN_CLUSTERED': XL_CHART_TYPE.,  # 3D Clustered Column.
        # 'THREE_D_COLUMN_STACKED': XL_CHART_TYPE.,  # 3D Stacked Column.
        # 'THREE_D_COLUMN_STACKED_100': XL_CHART_TYPE.,  # 3D 100% Stacked Column.
        # 'COLUMN_CLUSTERED': XL_CHART_TYPE.,  # Clustered Column.
        # 'COLUMN_STACKED': XL_CHART_TYPE.,  # Stacked Column.
        # 'COLUMN_STACKED_100': XL_CHART_TYPE.,  # 100% Stacked Column.
        'CONE_COL': XL_CHART_TYPE.CONE_COL,  # 3D Cone Column.
        # 'CONE_COL_CLUSTERED': XL_CHART_TYPE.,  # Clustered Cone Column.
        # 'CONE_COL_STACKED': XL_CHART_TYPE.,  # Stacked Cone Column.
        # 'CONE_COL_STACKED_100': XL_CHART_TYPE.,  # 100% Stacked Cone Column.
        # 'CYLINDER_COL': XL_CHART_TYPE.CYLINDER_COL,  # 3D Cylinder Column.
        # 'CYLINDER_COL_CLUSTERED': XL_CHART_TYPE.,  # Clustered Cone Column.
        # 'CYLINDER_COL_STACKED': XL_CHART_TYPE.,  # Stacked Cone Column.
        # 'CYLINDER_COL_STACKED_100': XL_CHART_TYPE.,  # 100% Stacked Cylinder Column.
        # 'PYRAMID_COL': XL_CHART_TYPE.PYRAMID_COL,  # 3D Pyramid Column.
        # 'PYRAMID_COL_CLUSTERED': XL_CHART_TYPE.,  # Clustered Pyramid Column.
        # 'PYRAMID_COL_STACKED': XL_CHART_TYPE.,  # Stacked Pyramid Column.
        # 'PYRAMID_COL_STACKED_100': XL_CHART_TYPE.,  # 100% Stacked Pyramid Column.
    }

    def __init__(self, df: pd.DataFrame, three_d: bool = False, shape='rectangle', stacked: bool = False,
                 normalized: bool = False,
                 **kwargs):
        """

        :param df: Pandas dataframe containing data for the chart.
        :param three_d: Whether a 3-D version of the chart should be used
        :param shape:
        :param stacked:
        :param normalized:
        :param kwargs:
        """
        super().__init__(df=df, **kwargs)

        if three_d:
            if shape == 'rectangle':
                if stacked:
                    if normalized:
                        self.chart_type = XL_CHART_TYPE.THREE_D_COLUMN_STACKED_100,
                    else:
                        self.chart_type = XL_CHART_TYPE.THREE_D_COLUMN_STACKED,
                else:
                    self.chart_type = XL_CHART_TYPE.THREE_D_COLUMN_CLUSTERED,
            elif shape == 'cone':
                if stacked:
                    if normalized:
                        self.chart_type = XL_CHART_TYPE.CONE_COL_STACKED_100,
                    else:
                        self.chart_type = XL_CHART_TYPE.CONE_COL_STACKED,
                else:
                    self.chart_type = XL_CHART_TYPE.CONE_COL_CLUSTERED,
            elif shape == 'cylinder':
                if stacked:
                    if normalized:
                        self.chart_type = XL_CHART_TYPE.CYLINDER_COL_STACKED_100,
                    else:
                        self.chart_type = XL_CHART_TYPE.CYLINDER_COL_STACKED,
                else:
                    self.chart_type = XL_CHART_TYPE.CYLINDER_COL_CLUSTERED,
            elif shape == 'pyramid':
                if stacked:
                    if normalized:
                        self.chart_type = XL_CHART_TYPE.PYRAMID_COL_STACKED_100,
                    else:
                        self.chart_type = XL_CHART_TYPE.PYRAMID_COL_STACKED,
                else:
                    self.chart_type = XL_CHART_TYPE.PYRAMID_COL_CLUSTERED,
        else:
            if stacked:
                if normalized:
                    self.chart_type = XL_CHART_TYPE.COLUMN_STACKED_100,
                else:
                    self.chart_type = XL_CHART_TYPE.COLUMN_STACKED,
            else:
                self.chart_type = XL_CHART_TYPE.COLUMN_CLUSTERED,


class LineChart(Chart):

    def __init__(self, df: pd.DataFrame, three_d: bool = False, markers: bool = False, stacked: bool = False,
                 normalized: bool = False,
                 **kwargs):
        """

        :param df: Pandas dataframe containing data for the chart.
        :param three_d: Whether a 3-D version of the chart should be used
        :param markers:
        :param stacked:
        :param normalized:
        :param kwargs:
        """
        super().__init__(df=df, **kwargs)

        if three_d:
            self.chart_type = XL_CHART_TYPE.THREE_D_LINE
        else:
            if markers:
                if stacked:
                    if normalized:
                        self.chart_type = XL_CHART_TYPE.LINE_MARKERS_STACKED_100
                    else:
                        self.chart_type = XL_CHART_TYPE.LINE_MARKERS_STACKED
                else:
                    self.chart_type = XL_CHART_TYPE.LINE_MARKERS
            else:
                if stacked:
                    if normalized:
                        self.chart_type = XL_CHART_TYPE.LINE_STACKED_100
                    else:
                        self.chart_type = XL_CHART_TYPE.LINE_STACKED
                else:
                    self.chart_type = XL_CHART_TYPE.LINE


class PieChart(Chart):

    def __init__(self, df: pd.DataFrame, three_d: bool = False, doughnut: bool = False, exploded: bool = False,
                 compound: bool = False, compound_type: str = 'bar_of_pie', **kwargs):
        """

        :param df: Pandas dataframe containing data for the chart.
        :param three_d: Whether a 3-D version of the chart should be used
        :param doughnut:
        :param exploded:
        :param compound:
        :param compound_type:
        :param kwargs:
        """
        super().__init__(df=df, **kwargs)

        if three_d:
            if exploded:
                self.chart_type = XL_CHART_TYPE.THREE_D_PIE_EXPLODED
            else:
                self.chart_type = XL_CHART_TYPE.THREE_D_PIE
        else:
            if doughnut:
                if exploded:
                    self.chart_type = XL_CHART_TYPE.DOUGHNUT_EXPLODED
                else:
                    self.chart_type = XL_CHART_TYPE.DOUGHNUT
            else:
                if compound:
                    if compound_type == 'bar_of_pie':
                        self.chart_type = XL_CHART_TYPE.BAR_OF_PIE
                    elif compound_type == 'pie_of_pie':
                        self.chart_type = XL_CHART_TYPE.PIE_OF_PIE
                elif exploded:
                    self.chart_type = XL_CHART_TYPE.PIE_EXPLODED
                else:
                    self.chart_type = XL_CHART_TYPE.PIE


class RadarChart(Chart):

    def __init__(self, df: pd.DataFrame, filled: bool = False, markers: bool = False, **kwargs):
        """

        :param df: Pandas dataframe containing data for the chart.
        :param filled:
        :param markers:
        :param kwargs:
        """
        super().__init__(df=df, **kwargs)

        if filled:
            self.chart_type = XL_CHART_TYPE.RADAR_FILLED
        elif markers:
            self.chart_type = XL_CHART_TYPE.RADAR_MARKERS
        else:
            self.chart_type = XL_CHART_TYPE.RADAR


class ScatterChart(Chart):

    def __init__(self, df: pd.DataFrame, x_col: str, y_col: str, lines: bool = False, markers: bool = False,
                 smooth: bool = False, **kwargs):
        """

        :param df: Pandas dataframe containing data for the chart.
        :param x_col:
        :param y_col:
        :param lines:
        :param markers:
        :param smooth:
        :param kwargs:
        """
        super().__init__(df=df, **kwargs)

        self.axis_cols = [x_col, y_col]

        if lines:
            if markers:
                if smooth:
                    self.chart_type = XL_CHART_TYPE.XY_SCATTER_SMOOTH
                else:
                    self.chart_type = XL_CHART_TYPE.XY_SCATTER_LINES
            else:
                if smooth:
                    self.chart_type = XL_CHART_TYPE.XY_SCATTER_SMOOTH_NO_MARKERS
                else:
                    self.chart_type = XL_CHART_TYPE.XY_SCATTER_LINES_NO_MARKERS
        else:
            self.chart_type = XL_CHART_TYPE.XY_SCATTER,

    def set_chart_data_type(self) -> None:
        self.chart_data = XyChartData()

    def prep_chart_data(self) -> None:
        """

        :return:
        """

        # If multi-index, how many levels, xy or bubble plot must have either 1 or 2 levels to columns
        if self.df.columns.nlevels == 1:
            # only one series in dataset
            series = self.chart_data.add_series('Data')
            for index, row in self.df.iterrows():
                series.add_data_point(*[row[_] for _ in self.axis_cols])

        elif self.df.columns.nlevels == 2:
            # potentially multiple series in dataset

            # get the list of all the axis columns (including size for bubble charts). Grid_pptx will assume that
            # any level 1 values in the MultiIndex that have all three of these columns should be treated as
            # separate series.
            for series_candidate in self.df.columns.get_level_values(0).unique():
                axis_vals_in_series = self.df.loc[:, (series_candidate, slice(None))] \
                    .columns.get_level_values(1).tolist()

                # if all vals in the axis_vals_list are included in the axis_vals_in_series, then assume this
                # is a series and add the series and the values
                if all(_ in axis_vals_in_series for _ in self.axis_cols):
                    series = self.chart_data.add_series(series_candidate)
                    for index, row in self.df.iterrows():
                        series.add_data_point(*[(series_candidate, row[_]) for _ in self.axis_cols])

        else:
            raise ValueError('The dataframe\'s columns must have no more than 2 levels.')


class BubbleChart(ScatterChart):

    def __init__(self, df: pd.DataFrame, x_col: str, y_col: str, size_col: str, three_d: bool = False,
                 **kwargs) -> None:
        """

        :param df: Pandas dataframe containing data for the chart.
        :param x_col:
        :param y_col:
        :param size_col:
        :param three_d: Whether a 3-D version of the chart should be used
        :param kwargs:
        """
        super().__init__(df=df, x_col=x_col, y_col=y_col, **kwargs)

        self.axis_cols = [x_col, y_col, size_col]

        if three_d:
            self.chart_type = XL_CHART_TYPE.BUBBLE_THREE_D_EFFECT
        else:
            self.chart_type = XL_CHART_TYPE.BUBBLE

    def set_chart_data_type(self) -> None:
        self.chart_data = BubbleChartData()

class StockChart(Chart):

    def __init__(self, df: pd.DataFrame, incl_open: bool = False, volume: bool = False, **kwargs):
        """

        :param df: Pandas dataframe containing data for the chart.
        :param incl_open:
        :param volume:
        :param kwargs:
        """
        super().__init__(df=df, **kwargs)

        if incl_open:  #: note: "incl_open" was used instead of "open" to avoid shadowing builtin "open"
            if volume:
                self.chart_type = XL_CHART_TYPE.STOCK_VOHLC
            else:
                self.chart_type = XL_CHART_TYPE.STOCK_OHLC,
        else:
            if volume:
                self.chart_type = XL_CHART_TYPE.STOCK_VHLC
            else:
                self.chart_type = XL_CHART_TYPE.STOCK_HLC,


class SurfaceChart(Chart):

    def __init__(self, df: pd.DataFrame, top_view: bool = False, wireframe: bool = False, **kwargs):
        """

        :param df: Pandas dataframe containing data for the chart.
        :param top_view:
        :param wireframe:
        :param kwargs:
        """
        super().__init__(df=df, **kwargs)

        if top_view:
            if wireframe:
                self.chart_type = XL_CHART_TYPE.SURFACE_TOP_VIEW_WIREFRAME
            else:
                self.chart_type = XL_CHART_TYPE.SURFACE_TOP_VIEW
        else:
            if wireframe:
                self.chart_type = XL_CHART_TYPE.SURFACE_WIREFRAME
            else:
                self.chart_type = XL_CHART_TYPE.SURFACE
