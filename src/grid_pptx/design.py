from __future__ import annotations
from typing import TYPE_CHECKING, Union
from .components.panel import GridPanel

if TYPE_CHECKING:
    from src.grid_pptx import GridSlide


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

        left_tracker = self.left
        for container in self.containers:
            # Top and height will be the same for all columns in row
            container.top = self.top
            container.height = self.height

            # width will be determined by width of current row and value (out of 12) given to panel
            container.left = left_tracker

            container.width = container.value / 12.0 * self.width

            left_tracker += container.width

            if container.terminal:
                # reach in and grab the panel to add to the slide
                panel = container.containers[0]

                panel.top = container.top
                panel.height = container.height
                panel.left = container.left
                panel.width = container.width

                panel.add_to_slide(slide)

            else:
                container.build(slide)


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

        top_tracker = self.top
        for container in self.containers:
            # left and width will be the same for all rows in column
            container.width = self.width
            container.left = self.left

            # Top and height will be the same for all columns in row
            container.top = top_tracker
            container.height = container.value / 12.0 * self.height

            top_tracker += container.height

            if container.terminal:
                # reach in and grab the panel to add to the slide
                panel = container.containers[0]

                panel.top = container.top
                panel.height = container.height
                panel.left = container.left
                panel.width = container.width

                panel.add_to_slide(slide)
            else:
                container.build(slide)
