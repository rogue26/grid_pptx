from grid_pptx import GridPresentation, Row, Column
from grid_pptx.components import Text

if __name__ == '__main__':  # pragma: no cover
    a = Text(text='a', outline_color='black', shadow=False)
    b = Text(text='b', outline_color='black', shadow=False)
    c = Text(text='c', outline_color='black', shadow=False)
    d = Text(text='d', outline_color='black', shadow=False)
    e = Text(text='e', outline_color='black', shadow=False)
    f = Text(text='f', outline_color='black', shadow=False)
    g = Text(text='g', outline_color='black', shadow=False)
    h = Text(text='h', outline_color='black', shadow=False)
    i = Text(text='i', outline_color='black', shadow=False)
    j = Text(text='j', outline_color='black', shadow=False)
    k = Text(text='k', outline_color='black', shadow=False)

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

    p.save('example_1.pptx')
