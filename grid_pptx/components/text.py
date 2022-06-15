from __future__ import annotations
from typing import TYPE_CHECKING
from .panel import GridPanel

from pptx.util import Pt
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT

# imports for type hints that would normally cause circular imports
if TYPE_CHECKING:
    from grid_pptx.slide import GridSlide


class Text(GridPanel):
    def __init__(self, text: str, **kwargs) -> None:
        super().__init__(**kwargs)

        self.text = text

        self.fill_color = None
        self.outline_color = None
        self.fontcolor = 'black'
        self.bold = False
        self.fontsize = 16

        # set any attributes that have been supplied in kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_to_slide(self, gridslide: GridSlide) -> None:
        print('adding to slide', self.text)
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
        p.alignment = PP_PARAGRAPH_ALIGNMENT.CENTER
        run = p.add_run()
        run.text = self.text
        font = run.font
        font.size = Pt(self.fontsize)
        font.bold = self.bold
        font.color.rgb = self.color_dict[self.fontcolor]


class Bullets(Text):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class Footnotes(Text):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
