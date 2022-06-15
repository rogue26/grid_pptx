from __future__ import annotations
from typing import TYPE_CHECKING, Union
import itertools
from pptx.slide import Slide

from grid_pptx.components.panel import GridPanel
from .components import Placeholder

# imports for type hints that would normally cause circular imports
if TYPE_CHECKING:
    from .design import GridDesign


class GridSlide:
    """
    Manages a pptx.slides.Slide instance
    """

    def __init__(self, slide: Slide, layout: list, content: list) -> None:

        self.slide = slide
        self.content = content
        self.panel = Placeholder(left=0, top=0, width=1, height=1, row_col='row', sublayout=layout, gridslide=self)

    @property
    def title(self):
        return self.slide.shapes.title.text

    @title.setter
    def title(self, value: str):
        # set title for slide object
        self.slide.shapes.title.text = value

    @property
    def design(self):
        return self._design

    @design.setter
    def design(self, value: Union[GridDesign, list]):
        if type(value) == list:
            # create GridDesign object
            pass

        if type(value) == GridDesign:
            # continue
            pass

    def add_panel(self, obj):
        if issubclass(type(obj), GridPanel):
            self.panels.append(obj)

    def add_wireframe(self):
        def recursive(panel):
            for p in panel.subpanels:
                p.add_text("", outline_color='black')
                recursive(p)

        recursive(self.panels[0])

    def loop_over_design(self, element, parent_panel):
        allocated_space = sum([_ for _ in element if isinstance(_, int)])
        unallocated_space = 12 - allocated_space
        number_unallocated = len([_ for _ in element if isinstance(_, list)])
        spaces = [_ if isinstance(_, int) else unallocated_space / number_unallocated for _ in element]

        if parent_panel.row_col == 'row':
            lefts = [0] + list(itertools.accumulate([_ / 12 * parent_panel.width for _ in spaces[:-1]]))
            lefts = [parent_panel.left + _ for _ in lefts]

            widths = [_ / 12 * parent_panel.width for _ in spaces]
            tops = [parent_panel.top for _ in spaces]
            heights = [parent_panel.height for _ in spaces]

            for i, (subelement, l, t, w, h) in enumerate(zip(element, lefts, tops, widths, heights)):
                new_panel = GridPanel(self, l, t, w, h, row_col='col')
                parent_panel.add_subpanel(new_panel)
                if isinstance(subelement, list):
                    self.loop_over_design(subelement, new_panel)

        elif parent_panel.row_col == 'col':
            lefts = [parent_panel.left for _ in spaces]
            widths = [parent_panel.width for _ in spaces]

            tops = [0] + list(itertools.accumulate([_ / 12 * parent_panel.height for _ in spaces[:-1]]))
            tops = [parent_panel.top + _ for _ in tops]

            heights = [_ / 12 * parent_panel.height for _ in spaces]

            for (subelement, l, t, w, h) in zip(element, lefts, tops, widths, heights):
                new_panel = GridPanel(self, l, t, w, h, row_col='row')

                parent_panel.add_subpanel(new_panel)
                if isinstance(subelement, list):
                    self.loop_over_design(subelement, new_panel)

    def implement_design(self):
        base_panel = GridPanel(self, 0, 1.2, 14.7, 6.5, row_col='row')
        self.add_panel(base_panel)
        self.loop_over_design(self.design, base_panel)
