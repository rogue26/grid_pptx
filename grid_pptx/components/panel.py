from __future__ import annotations
from typing import TYPE_CHECKING, Union

import itertools

from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_TICK_MARK, XL_TICK_LABEL_POSITION
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT
from pptx.dml.color import RGBColor

if TYPE_CHECKING:
    from grid_pptx.slide import GridSlide


class GridPanel:
    color_dict = {
        'black': RGBColor(0, 0, 0),
        'white': RGBColor(255, 255, 255),
    }

    def __init__(self, *, left: float = None, top: float = None, width: float = None, height: float = None,
                 left_margin: float = 0, top_margin: float = 0, right_margin: float = 0,
                 bottom_margin: float = 0, row_col: str = 'row'):

        self.left = left
        self.top = top
        self.width = width
        self.height = height

        self.left_margin = left_margin
        self.top_margin = top_margin
        self.right_margin = right_margin
        self.bottom_margin = bottom_margin

        self.row_col = row_col  # designates a panel as a "row" or "column"

        self.x = Inches(self.left)
        self.y = Inches(self.top)
        self.cx = Inches(self.width)
        self.cy = Inches(self.height)

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def row_col(self):
        return self._row_col

    @row_col.setter
    def row_col(self, value):
        if value in ['row', 'col']:
            self._row_col = value
        else:
            raise ValueError('Value of row_col must be either \'row\' or \'col\'')
