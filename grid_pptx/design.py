from __future__ import annotations
from typing import TYPE_CHECKING, Union

from .components.panel import GridPanel

if TYPE_CHECKING:  # pragma: no cover
    from grid_pptx import GridSlide


class Row(GridPanel):
    def __init__(self, value: int, *args: Union[GridPanel, Column], **kwargs) -> None:
        """

        :param value:
        :param args:
        :param kwargs:
        """
        super().__init__(**kwargs)

        self.value = value
        self.containers = [_ for _ in args]
        self.terminal = len(args) == 1 and not isinstance(args[0], Column)

    def build(self, slide: GridSlide) -> None:
        """

        :param slide:
        :return:
        """

        if self.terminal:  # configure panel and add to slide
            panel = self.containers[0]

            panel.top = self.top
            panel.height = self.height
            panel.left = self.left
            panel.width = self.width

            panel.add_to_slide(slide)

        else:
            left_tracker = self.left
            for container in self.containers:
                # Top and height will be the same for all columns in row
                container.top = self.top
                container.height = self.height

                # width will be determined by width of current row and value (out of 12) given to panel
                container.left = left_tracker
                container.width = container.value / 12.0 * self.width

                container.build(slide)

                left_tracker += container.width


class Column(GridPanel):
    def __init__(self, value: int, *args: Union[GridPanel, Row], **kwargs) -> None:
        """

        :param value:
        :param args:
        :param kwargs:
        """
        super().__init__(**kwargs)

        self.value = value
        self.containers = [_ for _ in args]
        self.terminal = len(args) == 1 and not isinstance(args[0], Row)

    def build(self, slide: GridSlide) -> None:
        """

        :param slide:
        :return:
        """

        if self.terminal:  # configure panel and add to slide
            panel = self.containers[0]

            panel.top = self.top
            panel.height = self.height
            panel.left = self.left
            panel.width = self.width

            panel.add_to_slide(slide)

        else:
            top_tracker = self.top
            for container in self.containers:
                # Left and width will be the same for all columns in row
                container.left = self.left
                container.width = self.width

                # width will be determined by width of current row and value (out of 12) given to panel

                container.top = top_tracker
                container.height = container.value / 12.0 * self.height

                container.build(slide)

                top_tracker += container.height
