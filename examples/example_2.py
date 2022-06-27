from grid_pptx import GridPresentation, Row, Column
from grid_pptx.components import Text, AreaChart, Table
import pandas as pd

if __name__ == '__main__':  # pragma: no cover
    df = pd.DataFrame({'a': [1, 2, 9], 'b': [4, 1, 6], 'c': [7, 8, 2]})

    p = GridPresentation(
        # template='greenblue.pptx',
        slide_size='16_9',
        header_height=1.5,
        footer_height=1.0,
        right_margin=0.25,
        left_margin=0.25
    )

    chart = AreaChart(df=df, stacked=True, normalized=False)
    table = Table(df)
    text = Text(text='some explanatory text here')

    design = Row(12,
                 Column(6, chart),
                 Column(6,
                        Row(6, table),
                        Row(6, text)))

    p.add_slide(layout_num=5, design=design, title='my shiny analysis')

    filename = 'example_2.pptx'

    p.save(filename)
