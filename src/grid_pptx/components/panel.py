from __future__ import annotations

from pptx.util import Inches
from pptx.dml.color import RGBColor


class GridPanel:
    color_dict = {
        'black': RGBColor(0, 0, 0),
        'white': RGBColor(255, 255, 255),
    }

    def __init__(self, *, left: float = None, top: float = None, width: float = None, height: float = None,
                 left_margin: float = 0, top_margin: float = 0, right_margin: float = 0,
                 bottom_margin: float = 0, **kwargs) -> None:
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        self.left_margin = left_margin
        self.top_margin = top_margin
        self.right_margin = right_margin
        self.bottom_margin = bottom_margin

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def x(self):
        return Inches(self.left)

    @property
    def y(self):
        return Inches(self.top)

    @property
    def cx(self):
        return Inches(self.width)

    @property
    def cy(self):
        return Inches(self.height)
