from __future__ import annotations

from pptx.util import Inches


class GridPanel:
    """
    Base class for Row, Column, and all components, including charts, tables, text, images, etc.
    """

    def __init__(self, *, left: float = None, top: float = None, width: float = None, height: float = None,
                 left_margin: float = 0, top_margin: float = 0, right_margin: float = 0,
                 bottom_margin: float = 0, **kwargs) -> None:
        """
        :param left: The distance from the left side of the slide to the left side of the panel in inches.
        :param top: The distance from the top of the slide to the top of the panel in inches.
        :param width: The width of the panel in inches.
        :param height: The height of the panel in inches.
        :param left_margin:
        :param top_margin:
        :param right_margin:
        :param bottom_margin:
        :param kwargs:
        """

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
        """
        The distance from the left side of the slide to the right side of the panel in inches
        """
        return self.left + self.width

    @property
    def bottom(self):
        """
        The distance from the top of the slide to the bottom of the panel in inches
        """
        return self.top + self.height

    @property
    def x(self):
        """
        The distance from the left side of the slide to the right side of the panel in EMU (default PowerPoint units).
        """
        return Inches(self.left)

    @property
    def y(self):
        """
        The distance from the top of the slide to the top of the panel in EMU (default PowerPoint units).
        """
        return Inches(self.top)

    @property
    def cx(self):
        """
        The width of the panel in EMU (default PowerPoint units).
        """
        return Inches(self.width)

    @property
    def cy(self):
        """
        The height of the panel in EMU (default PowerPoint units).
        """
        return Inches(self.height)
