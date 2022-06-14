from typing import Union
import itertools

from .presentation import GridPresentation
from .panel import Panel


class GridDesign:
    def __init__(self):
        pass


class GridSlide:

    def __init__(self, presentation: GridPresentation, slide):

        self.presentation = presentation
        self.slide = slide

        self._design = None
        self.panels = []

        self.implement_design()

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
        if issubclass(type(obj), Panel):
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
                new_panel = self.panel(self, l, t, w, h, row_col='col')
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
                new_panel = self.panel(self, l, t, w, h, row_col='row')

                parent_panel.add_subpanel(new_panel)
                if isinstance(subelement, list):
                    self.loop_over_design(subelement, new_panel)

    def implement_design(self):
        base_panel = Panel(self, 0, 1.2, 14.7, 6.5, row_col='row')
        self.add_panel(base_panel)
        self.loop_over_design(self.design, base_panel)
