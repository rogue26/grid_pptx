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
