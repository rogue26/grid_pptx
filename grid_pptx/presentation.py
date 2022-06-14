from typing import Union
from pathlib import Path

from pptx import Presentation
from pptx.slide import Slide
from .slide import GridSlide


class GridPresentation:
    def __init__(self, template: Union[str, Path] = None):
        self.prs = Presentation(template)
        self.slides = []


    def save(self, loc: Union[str, Path] = Path.home()):
        self.prs.save(loc)

    def add_slide(self, layout):
        """Add a Slide to the pptx Presentation and a GridSlide to GridPresentation to manage it

        :param new_slide:
        :return:
        """
        new_slide = self.prs.add_slide(layout)
        self.slides.append(GridSlide(self, new_slide))
