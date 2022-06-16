from __future__ import annotations
from typing import TYPE_CHECKING

from pptx.util import Pt
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT

from .panel import GridPanel

# imports for type hints that would normally cause circular imports
if TYPE_CHECKING:
    from grid_pptx.slide import GridSlide


class Text(GridPanel):
    text_alignments = {
        'center': PP_PARAGRAPH_ALIGNMENT.CENTER,
        'distribute': PP_PARAGRAPH_ALIGNMENT.DISTRIBUTE,
        'justify': PP_PARAGRAPH_ALIGNMENT.JUSTIFY,
        'justify_low': PP_PARAGRAPH_ALIGNMENT.JUSTIFY_LOW,
        'left': PP_PARAGRAPH_ALIGNMENT.LEFT,
        'right': PP_PARAGRAPH_ALIGNMENT.RIGHT,
        'thai_distribute': PP_PARAGRAPH_ALIGNMENT.THAI_DISTRIBUTE,
    }

    def __init__(self, text: str, alignment: str = 'left', **kwargs) -> None:
        """

        :param text:
        :param alignment:
        :param kwargs:
        """
        super().__init__(**kwargs)

        self.text = text

        self.fill_color = 'white'
        self.outline_color = None
        self.fontcolor = 'black'
        self.bold = False
        self.fontsize = 16
        self.alignment = alignment

        # set any attributes that have been supplied in kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_to_slide(self, gridslide: GridSlide) -> None:
        """

        :param gridslide:
        :return:
        """
        slide = gridslide.slide

        shape = slide.shapes.add_shape(
            MSO_AUTO_SHAPE_TYPE.RECTANGLE, self.x, self.y, self.cx, self.cy
        )

        # configure fill color
        if self.fill_color is None:
            shape.fill.background()
        else:
            shape.fill.solid()
            shape.fill.fore_color.rgb = self.color_dict[self.fill_color]

        # configure outline color
        if self.outline_color is None:
            shape.line.fill.background()
        else:
            shape.line.fill.solid()
            shape.line.color.rgb = self.color_dict[self.outline_color]

        # configure text
        p = shape.text_frame.paragraphs[0]
        p.alignment = self.text_alignments[self.alignment]
        run = p.add_run()
        run.text = self.text
        font = run.font
        font.size = Pt(self.fontsize)
        font.bold = self.bold
        font.color.rgb = self.color_dict[self.fontcolor]


class Bullets(Text):
    def __init__(self, **kwargs) -> None:
        """

        :param kwargs:
        """
        super().__init__(**kwargs)


class Footnotes(Text):
    def __init__(self, **kwargs) -> None:
        """

        :param kwargs:
        """
        super().__init__(**kwargs)
