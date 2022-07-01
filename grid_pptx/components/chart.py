from __future__ import annotations
from typing import TYPE_CHECKING, Union

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


class ChartAxis:
    # Options for tick mark placement on either the x or y axes. Values are the constants
    # used in the python-pptx package, but are used in the code as ``XL_CHART_TYPE.LINE``, etc.
    tick_mark_options = {
        'none': XL_TICK_MARK.NONE,
        'cross': XL_TICK_MARK.CROSS,
        'inside': XL_TICK_MARK.INSIDE,
        'outside': XL_TICK_MARK.OUTSIDE,
    }

    inv_tick_mark_options = {v: k for k, v in tick_mark_options.items()}

    tick_label_positions = {
        'high': XL_TICK_LABEL_POSITION.HIGH,
        'low': XL_TICK_LABEL_POSITION.LOW,
        'next_to_axis': XL_TICK_LABEL_POSITION.NEXT_TO_AXIS,
        'none': XL_TICK_LABEL_POSITION.NONE,
    }

    inv_tick_label_positions = {v: k for k, v in tick_label_positions.items()}

    def __init__(
            self, *,
            gridchart: GridChart,
            axis_type: str,
    ) -> None:

        self.gridchart = gridchart
        self.axis_type = axis_type
        self.axis = None  # populated later when adding the chart to the pptx slide

    def add_to_slide(
            self, *,
            minor_tick_marks: str = 'none',
            major_tick_marks: str = 'inside',
            has_minor_gridlines: bool = False,
            has_major_gridlines: bool = False,
            tick_label_position: str = 'next_to_axis',
            tick_label_italic: bool = False,
            tick_label_fontsize: int = 16
    ) -> None:

        # set self.axis if possible, or raise an exception if axis_type is something other than 'x' or 'y'
        if self.axis_type == 'x':
            self.axis = self.gridchart.chart.value_axis
        elif self.axis_type == 'y':
            self.axis = self.gridchart.chart.category_axis

        self.minor_tick_marks = minor_tick_marks
        self.major_tick_marks = major_tick_marks
        self.has_minor_gridlines = has_minor_gridlines
        self.has_major_gridlines = has_major_gridlines
        self.tick_label_position = tick_label_position
        self.tick_label_italic = tick_label_italic
        self.tick_label_fontsize = tick_label_fontsize

    @property
    def minor_tick_marks(self):
        return self.inv_tick_mark_options[self.axis.minor_tick_mark]

    @minor_tick_marks.setter
    def minor_tick_marks(self, value):
        self.axis.minor_tick_mark = self.tick_mark_options[value]

    @property
    def major_tick_marks(self):
        return self.inv_tick_mark_options[self.axis.major_tick_mark]

    @major_tick_marks.setter
    def major_tick_marks(self, value):
        self.axis.major_tick_mark = self.tick_mark_options[value]

    @property
    def has_minor_gridlines(self):
        return self.axis.has_minor_gridlines

    @has_minor_gridlines.setter
    def has_minor_gridlines(self, value):
        self.axis.has_minor_gridlines = value

    @property
    def has_major_gridlines(self):
        return self.axis.has_major_gridlines

    @has_major_gridlines.setter
    def has_major_gridlines(self, value):
        self.axis.has_major_gridlines = value

    @property
    def tick_label_position(self):
        return self.inv_tick_label_positions[self.axis.tick_label_position]

    @tick_label_position.setter
    def tick_label_position(self, value):
        self.axis.tick_label_position = self.tick_label_positions[value]

    @property
    def tick_label_italic(self):
        return self.axis.tick_labels.font.italic

    @tick_label_italic.setter
    def tick_label_italic(self, value):
        self.axis.tick_labels.font.italic = value

    @property
    def tick_label_fontsize(self):
        return self.axis.tick_labels.font.size.pt

    @tick_label_fontsize.setter
    def tick_label_fontsize(self, value):
        self.axis.tick_labels.font.size = Pt(value)


class NewInitCaller(type):
    """
    metaclass which overrides the "__call__" function to automatically call "set_chart_dat_type"
    "prep_chart_data" methods after __init__, even if __init__ has been overridden
    """

    def __call__(cls, *args, **kwargs):
        """Called when you call MyNewClass() """
        obj = type.__call__(cls, *args, **kwargs)
        # obj.add_to_slide()
        # obj.set_chart_axes()
        obj.set_chart_data_type()
        obj.prep_chart_data()
        return obj


class GridChart(GridPanel, metaclass=NewInitCaller):
    """
    Base class for all charts
    """

    def __init__(
            self, *,
            df: pd.DataFrame,
            chart_data: Union[CategoryChartData, XyChartData, BubbleChartData] = None,
            title: str = None,
            has_legend: bool = True
    ) -> None:
        """

        :param df: Pandas dataframe containing data for the chart.
        :param chart_data:
        :param title:
        :param has_legend:
        """
        super().__init__()

        self.df = df
        self.chart_data = chart_data
        self.chart_type = None  # initialized in subclasses -- here as a placeholder
        self.chart = None
        self.x_axis = None
        self.y_axis = None

        # default chart parameters
        self._title = title
        self.has_legend = has_legend
        self.smooth_lines = False

        self.x_axis = ChartAxis(gridchart=self, axis_type='x')
        self.y_axis = ChartAxis(gridchart=self, axis_type='y')

    @property
    def title(self):
        return self.chart.chart_title.text_frame.text

    @title.setter
    def title(self, value):
        self.chart.chart_title.text_frame.text = value

    def set_chart_data_type(self) -> None:
        self.chart_data = CategoryChartData()

    def evaluate_dataframe(self):
        return None

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

        try:
            # For some chart types, XL_CHART_TYPE.<chart type> returns a tuple with one integer. For these, we need
            # the zeroth element of the tuple

            self.chart = slide.shapes.add_chart(
                self.chart_type[0], self.x, self.y, self.cx, self.cy, self.chart_data
            ).chart

            self.title = self._title
            self.chart.has_legend = self.has_legend
            self.chart.series[0].smooth = self.smooth_lines

            self.x_axis.add_to_slide()
            self.y_axis.add_to_slide()

        except TypeError:
            # For other chart types, XL_CHART_TYPE.<chart type> returns an EnumValue object that is all that is needed.
            # Taking the zeroth element will throw a TypeError, which is caught here
            self.chart = slide.shapes.add_chart(
                self.chart_type, self.x, self.y, self.cx, self.cy, self.chart_data
            ).chart

            self.chart.chart_title.text_frame.text = self.title
            self.chart.has_legend = self.has_legend
            self.chart.series[0].smooth = self.smooth_lines

            self.x_axis.add_to_slide()
            self.y_axis.add_to_slide()

        except NotImplementedError as ne:

            # Some chart types are not yet implemented in python-pptx. In those situations, attempting to add
            # the chart type to the slide will throw a NotImplementedError, which is caught here. For more info, see:
            # https://python-pptx.readthedocs.io/en/latest/dev/analysis/cht-chart-overview.html

            # for charts that are not implemented, a rectangle will be added to the slide with the error message
            # to alert the user to modify their chart choice.
            self.chart = slide.shapes.add_shape(
                MSO_AUTO_SHAPE_TYPE.RECTANGLE, self.x, self.y, self.cx, self.cy
            )

            # configure text for the rectangle
            p = self.chart.text_frame.paragraphs[0]
            p.alignment = PP_PARAGRAPH_ALIGNMENT.CENTER
            run = p.add_run()
            run.text = str(ne)  # text of the rectangle is the error message
            font = run.font
            font.size = Pt(10)


class AreaChart(GridChart):
    """
    A variation of a line graph, in which areas under the line are filled in.
    """

    def __init__(
            self, *,
            df: pd.DataFrame,
            chart_data: Union[CategoryChartData, XyChartData, BubbleChartData] = None,
            title: str = None,
            has_legend: bool = True,

            three_d: bool = False,
            stacked: bool = False,
            normalized: bool = False,
    ) -> None:
        """

        :param df: Pandas dataframe containing data for the chart.
        :param three_d: Whether a 3-D version of the chart should be used
        :param stacked:
        :param normalized: Whether values should be scaled such that they sum to 100%. Only applicable \
                if ``stacked=TRUE``.
        """

        super().__init__(df=df, chart_data=chart_data, title=title, has_legend=has_legend)

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


class BarChart(GridChart):
    """
    <Description of Bar Chart>
    """

    def __init__(
            self, *,
            df: pd.DataFrame,
            chart_data: Union[CategoryChartData, XyChartData, BubbleChartData] = None,
            title: str = None,
            has_legend: bool = True,

            three_d: bool = False,
            shape: str = 'rectangle',
            stacked: bool = False,
            normalized: bool = False
    ) -> None:
        """

        :param df: Pandas dataframe containing data for the chart.
        :param three_d: Whether a 3-D version of the chart should be used
        :param shape:
        :param stacked:
        :param normalized:
        """
        super().__init__(df=df, chart_data=chart_data, title=title, has_legend=has_legend)
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


class ColumnChart(GridChart):
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

    def __init__(
            self, *,
            df: pd.DataFrame,
            chart_data: Union[CategoryChartData, XyChartData, BubbleChartData] = None,
            title: str = None,
            has_legend: bool = True,

            three_d: bool = False,
            shape='rectangle',
            stacked: bool = False,
            normalized: bool = False
    ) -> None:
        """

        :param df: Pandas dataframe containing data for the chart.
        :param chart_data:
        :param title:
        :param has_legend:
        :param three_d: Whether a 3-D version of the chart should be used
        :param shape:
        :param stacked:
        :param normalized:
        """
        super().__init__(df=df, chart_data=chart_data, title=title, has_legend=has_legend)

        # set chart_type
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


class LineChart(GridChart):

    def __init__(
            self, *,
            df: pd.DataFrame,
            chart_data: Union[CategoryChartData, XyChartData, BubbleChartData] = None,
            title: str = None,
            has_legend: bool = True,

            three_d: bool = False,
            markers: bool = False,
            stacked: bool = False,
            normalized: bool = False
    ) -> None:
        """

        :param df: Pandas dataframe containing data for the chart.
        :param chart_data:
        :param title:
        :param has_legend:

        :param three_d: Whether a 3-D version of the chart should be used
        :param markers:
        :param stacked:
        :param normalized:
        """
        super().__init__(df=df, chart_data=chart_data, title=title, has_legend=has_legend)

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


class PieChart(GridChart):

    def __init__(
            self, *,
            df: pd.DataFrame,
            chart_data: Union[CategoryChartData, XyChartData, BubbleChartData] = None,
            title: str = None,
            has_legend: bool = True,

            three_d: bool = False,
            doughnut: bool = False,
            exploded: bool = False,
            compound: bool = False,
            compound_type: str = 'bar_of_pie'
    ) -> None:
        """

        :param df: Pandas dataframe containing data for the chart.
        :param chart_data:
        :param title:
        :param has_legend:
        :param three_d: Whether a 3-D version of the chart should be used
        :param doughnut:
        :param exploded:
        :param compound:
        :param compound_type:
        """
        super().__init__(df=df, chart_data=chart_data, title=title, has_legend=has_legend)

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


class RadarChart(GridChart):

    def __init__(
            self, *,
            df: pd.DataFrame,
            chart_data: Union[CategoryChartData, XyChartData, BubbleChartData] = None,
            title: str = None,
            has_legend: bool = True,

            filled: bool = False,
            markers: bool = False
    ) -> None:
        """

        :param df: Pandas dataframe containing data for the chart.
        :param filled:
        :param markers:
        """
        super().__init__(df=df, chart_data=chart_data, title=title, has_legend=has_legend)

        if filled:
            self.chart_type = XL_CHART_TYPE.RADAR_FILLED
        elif markers:
            self.chart_type = XL_CHART_TYPE.RADAR_MARKERS
        else:
            self.chart_type = XL_CHART_TYPE.RADAR


class ScatterChart(GridChart):

    def __init__(
            self, *,
            df: pd.DataFrame,
            chart_data: Union[CategoryChartData, XyChartData, BubbleChartData] = None,
            title: str = None,
            has_legend: bool = True,

            x_col: str,
            y_col: str,
            lines: bool = False,
            markers: bool = False,
            smooth: bool = False
    ) -> None:
        """

        :param df: Pandas dataframe containing data for the chart.
        :param x_col:
        :param y_col:
        :param lines:
        :param markers:
        :param smooth:
        """
        super().__init__(df=df, chart_data=chart_data, title=title, has_legend=has_legend)

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

    def __init__(
            self, *,
            df: pd.DataFrame,
            chart_data: Union[CategoryChartData, XyChartData, BubbleChartData] = None,
            title: str = None,
            has_legend: bool = True,

            x_col: str,
            y_col: str,
            size_col: str,
            three_d: bool = False
    ) -> None:
        """

        :param df: Pandas dataframe containing data for the chart.
        :param x_col:
        :param y_col:
        :param size_col:
        :param three_d: Whether a 3-D version of the chart should be used
        """
        super().__init__(
            df=df, chart_data=chart_data, title=title, has_legend=has_legend, x_col=x_col,
            y_col=y_col
        )

        self.axis_cols = [x_col, y_col, size_col]

        if three_d:
            self.chart_type = XL_CHART_TYPE.BUBBLE_THREE_D_EFFECT
        else:
            self.chart_type = XL_CHART_TYPE.BUBBLE

    def set_chart_data_type(self) -> None:
        self.chart_data = BubbleChartData()


class StockChart(GridChart):

    def __init__(
            self, *,
            df: pd.DataFrame,
            chart_data: Union[CategoryChartData, XyChartData, BubbleChartData] = None,
            title: str = None,
            has_legend: bool = True,

            incl_open: bool = False,
            volume: bool = False
    ) -> None:
        """

        :param df: Pandas dataframe containing data for the chart.
        :param incl_open:
        :param volume:
        """
        super().__init__(
            df=df, chart_data=chart_data, title=title, has_legend=has_legend,
        )

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


class SurfaceChart(GridChart):

    def __init__(
            self, *,
            df: pd.DataFrame,
            chart_data: Union[CategoryChartData, XyChartData, BubbleChartData] = None,
            title: str = None,
            has_legend: bool = True,

            top_view: bool = False,
            wireframe: bool = False
    ) -> None:
        """

        :param df: Pandas dataframe containing data for the chart.
        :param top_view:
        :param wireframe:
        """
        super().__init__(df=df, chart_data=chart_data, title=title, has_legend=has_legend)

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
