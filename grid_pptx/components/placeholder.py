from .panel import GridPanel


class Placeholder(GridPanel):
    def __init__(self, layout, content, **kwargs):
        super().__init__(**kwargs)
        self.subpanels = []

        # create a panel for each element in the layout
        for cell, item in zip(layout, content):
            if type(cell) == int:
                self.subpanels.append(content)

            elif type(cell) in [list, tuple]:
                pass
                # append to panels

    # def add_subpanels(self, layout: Union[list, tuple], content: Union[list, tuple]) -> None:

    # if issubclass(type(obj), GridPanel):
    #     # make sure subpanel fits within dimensions of self
    #     if obj.left < self.left - 0.0001:
    #         raise ValueError(
    #             'Subpanel left side ({}) extends to the left of the parent panel left side ({})'.format(obj.left,
    #                                                                                                     self.left)
    #         )
    #     elif obj.right > self.right + 0.0001:
    #         raise ValueError(
    #             'Subpanel right side ({}) extends to the right of the parent panel right side ({})'.format(
    #                 obj.right, self.right)
    #         )
    #     elif obj.top < self.top - 0.0001:
    #         raise ValueError('Subpanel top ({}) extends above the parent panel top ({})'.format(obj.top, self.top))
    #     elif obj.bottom > self.bottom + 0.0001:
    #         raise ValueError(
    #             'Subpanel bottom ({}) extends below the bottom of the parent panel ({}).'.format(obj.bottom,
    #                                                                                              self.bottom)
    #         )
    #     else:
    #         # add the subpanel
    #         self.subpanels.append(obj)

    # create a placeholder panel

    # allocated_space = sum([_ for _ in sublayout if isinstance(_, int)])
    # unallocated_space = 12 - allocated_space
    # number_unallocated = len([_ for _ in sublayout if isinstance(_, list)])
    # spaces = [_ if isinstance(_, int) else unallocated_space / number_unallocated for _ in sublayout]
    #
    # if self.row_col == 'row':
    #     lefts = [0] + list(itertools.accumulate([_ / 12 * self.width for _ in spaces[:-1]]))
    #     lefts = [self.left + _ for _ in lefts]
    #
    #     widths = [_ / 12 * self.width for _ in spaces]
    #     tops = [self.top for _ in spaces]
    #     heights = [self.height for _ in spaces]
    #
    #     for i, (subelement, l, t, w, h) in enumerate(zip(element, lefts, tops, widths, heights)):
    #         new_panel = GridPanel(self, l, t, w, h, row_col='col')
    #         self.add_subpanel(new_panel)
    #         if isinstance(subelement, list):
    #             self.loop_over_design(subelement, new_panel)
