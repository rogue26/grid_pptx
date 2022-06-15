from __future__ import annotations
from typing import TYPE_CHECKING, Union
from pathlib import Path

from pptx import Presentation
from .slide import GridSlide
from .components import Placeholder

# imports for type hints that would normally cause circular imports
if TYPE_CHECKING:
    from .design import GridDesign



class GridPresentation:
    """
    Stores and manipulates a pptx.Presentation instance
    """

    def __init__(self, template: Union[str, Path] = None):
        self.prs = Presentation(template)
        self.slides = []

    def save(self, loc: Union[str, Path] = Path.home()):
        self.prs.save(loc)

    def add_slide(self, design: list, content: list, layout_num: int = 1, ) -> GridSlide:
        """Add a Slide to the pptx Presentation and a GridSlide to GridPresentation to manage it

        :param design:
        :param content:
        :param layout_num:
        :return:
        """

        layout = self.prs.slide_layouts[layout_num]

        new_slide = self.prs.slides.add_slide(layout)
        new_gridslide = GridSlide(self, new_slide)
        self.slides.append(new_gridslide)
        return new_gridslide
