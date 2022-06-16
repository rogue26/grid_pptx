from pathlib import Path
from grid_pptx import GridPresentation, Row, Column
from grid_pptx.components import Text, LineChart, AreaChart, PieChart, Table, BarChart, ColumnChart, ScatterChart
import pandas as pd


if __name__ == '__main__':
    df = pd.DataFrame({'a': [1, 2, 9], 'b': [4, 1, 6], 'c': [7, 8, 2]})

    chart = AreaChart(df=df, stacked=True, normalized=True)
    table = Table(df)
    text = Text(text='some explanatory text here')

    design = Row(12,
                 Column(6, chart),
                 Column(6,
                        Row(6, table),
                        Row(6, text)))

    p = GridPresentation(
        # template='greenblue.pptx',
        slide_size='16_9',
        header_height=1.5,
        footer_height=1.0,
        right_margin=0.25,
        left_margin=0.25
    )

    s = p.add_slide(layout_num=5, design=design, title='my shiny analysis')

    examples_loc = Path(__file__).parent.resolve()
    filename = 'example_2.pptx'
    p.save(examples_loc / filename)
