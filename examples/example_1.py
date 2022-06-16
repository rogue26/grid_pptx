from pathlib import Path
from grid_pptx import GridPresentation, Row, Column
from grid_pptx.components import Text

# options needed
# header space
# footer space / dealing with footnotes
# rescale if not adding to 12?
# padding around cells, slide

if __name__ == '__main__':
    a = Text(text='a', outline_color='black')
    b = Text(text='b', outline_color='black')
    c = Text(text='c', outline_color='black')
    d = Text(text='d', outline_color='black')
    e = Text(text='e', outline_color='black')
    f = Text(text='f', outline_color='black')
    g = Text(text='g', outline_color='black')
    h = Text(text='h', outline_color='black')
    i = Text(text='i', outline_color='black')
    j = Text(text='j', outline_color='black')
    k = Text(text='k', outline_color='black')

    design = Row(12,
                 Column(6,
                        Row(4,
                            Column(4, a),
                            Column(4, b),
                            Column(4, c)),
                        Row(4, d),
                        Row(4,
                            Column(4, e),
                            Column(4, f),
                            Column(4, g))),
                 Column(3, h),
                 Column(3,
                        Row(6, i),
                        Row(6,
                            Column(6, j),
                            Column(6, k))))

    p = GridPresentation(
        header_height=1.5,
        footer_height=1.0,
        right_margin=0.25,
        left_margin=0.25
    )

    s1 = p.add_slide(layout_num=5, design=design)

    examples_loc = Path(__file__).parent.resolve()
    filename = 'example_1.pptx'
    p.save(examples_loc / filename)
