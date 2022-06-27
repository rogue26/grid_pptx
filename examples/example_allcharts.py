from grid_pptx import GridPresentation, Row, Column
from grid_pptx.components import (
    AreaChart, BarChart, BubbleChart, ColumnChart, LineChart,
    PieChart, RadarChart, ScatterChart, StockChart, SurfaceChart,
    Text
)
import pandas as pd

if __name__ == '__main__':  # pragma: no cover
    p = GridPresentation(
        slide_size='16_9',
        header_height=1.5,
        footer_height=1.0,
        right_margin=0.25,
        left_margin=0.25
    )

    # AreaChart example
    df = pd.DataFrame({'a': [1, 2, 9], 'b': [4, 1, 6], 'c': [7, 8, 2]})
    chart = AreaChart(df=df, stacked=True, normalized=False)
    design = Row(12, chart)
    p.add_slide(layout_num=5, design=design, title='my shiny analysis')

    # BarChart example
    #  NotImplementedError: XML writer for chart type BAR_STACKED (58) not yet implemented
    #  NotImplementedError: XML writer for chart type THREE_D_BAR_STACKED (61) not yet implemented
    # NotImplementedError: XML writer for chart type THREE_D_BAR_STACKED_100 (62) not yet implemented
    df = pd.DataFrame({'a': [1, 2, 9], 'b': [4, 1, 6], 'c': [7, 8, 2]})
    not_implemented = Text(text="N/I")

    chart1a = BarChart(df=df, three_d=True, shape='rectangle', stacked=False, normalized=False)
    chart2a = BarChart(df=df, three_d=True, shape='cone', stacked=False, normalized=False)
    chart3a = BarChart(df=df, three_d=True, shape='cylinder', stacked=False, normalized=False)
    chart4a = BarChart(df=df, three_d=True, shape='pyramid', stacked=False, normalized=False)
    chart1b = BarChart(df=df, three_d=True, shape='rectangle', stacked=True, normalized=False)
    chart2b = BarChart(df=df, three_d=True, shape='cone', stacked=True, normalized=False)
    chart3b = BarChart(df=df, three_d=True, shape='cylinder', stacked=True, normalized=False)
    chart4b = BarChart(df=df, three_d=True, shape='pyramid', stacked=True, normalized=False)
    chart1c = BarChart(df=df, three_d=True, shape='rectangle', stacked=True, normalized=True)
    chart2c = BarChart(df=df, three_d=True, shape='cone', stacked=True, normalized=True)
    chart3c = BarChart(df=df, three_d=True, shape='cylinder', stacked=True, normalized=True)
    chart4c = BarChart(df=df, three_d=True, shape='pyramid', stacked=True, normalized=True)

    design = Row(12,
                 Column(3,
                        Row(4, chart1a),
                        Row(4, chart1b),
                        Row(4, chart1c)),
                 Column(3,
                        Row(4, chart2a),
                        Row(4, chart2b),
                        Row(4, chart2c)),
                 Column(3,
                        Row(4, chart3a),
                        Row(4, chart3b),
                        Row(4, chart3c)),
                 Column(3,
                        Row(4, chart4a),
                        Row(4, chart4b),
                        Row(4, chart4c)))

    p.add_slide(layout_num=5, design=design, title='3D Bar charts')

    chart5a = BarChart(df=df, three_d=False, shape='rectangle', stacked=False, normalized=False)
    chart5b = BarChart(df=df, three_d=False, shape='rectangle', stacked=True, normalized=False)
    chart5c = BarChart(df=df, three_d=False, shape='rectangle', stacked=True, normalized=True)

    design = Row(12,
                 Column(4, chart5a),
                 Column(4, chart5b),
                 Column(4, chart5c))

    p.add_slide(layout_num=5, design=design, title='Regular Bar charts')

    # BubbleChart example
    df = pd.DataFrame({'x': [1, 2, 9], 'y': [4, 1, 6], 'size': [7, 8, 2]})
    chart1 = BubbleChart(df=df, x_col='x', y_col='y', size_col='size', three_d=False)
    design = Row(12, chart1)
    p.add_slide(layout_num=5, design=design, title='Bubble charts')

    # ColumnChart example
    df = pd.DataFrame({'a': [1, 2, 9], 'b': [4, 1, 6], 'c': [7, 8, 2]})
    chart = ColumnChart(df=df, stacked=True, normalized=False)
    design = Row(12, chart)
    p.add_slide(layout_num=5, design=design, title='my shiny analysis')

    # LineChart example
    df = pd.DataFrame({'a': [1, 2, 9], 'b': [4, 1, 6], 'c': [7, 8, 2]})
    chart = LineChart(df=df, stacked=True, normalized=False)
    design = Row(12, chart)
    p.add_slide(layout_num=5, design=design, title='my shiny analysis')

    # PieChart example
    # df = pd.DataFrame({'a': [1, 2, 9], 'b': [4, 1, 6], 'c': [7, 8, 2]})
    # chart = PieChart(df=df, stacked=True, normalized=False)
    # design = Row(12, chart)
    # p.add_slide(layout_num=5, design=design, title='my shiny analysis')

    # RadarChart example
    df = pd.DataFrame({'a': [1, 2, 9], 'b': [4, 1, 6], 'c': [7, 8, 2]})
    chart = RadarChart(df=df, stacked=True, normalized=False)
    design = Row(12, chart)
    p.add_slide(layout_num=5, design=design, title='my shiny analysis')

    # ScatterChart example
    df = pd.DataFrame({'x': [1, 2, 9], 'y': [4, 1, 6], 'size': [7, 8, 2]})
    chart1 = ScatterChart(df=df, x_col='x', y_col='y', three_d=False)
    design = Row(12, chart1)
    p.add_slide(layout_num=5, design=design, title='Scatter charts')

    # StockChart example
    df = pd.DataFrame({'a': [1, 2, 9], 'b': [4, 1, 6], 'c': [7, 8, 2]})
    chart = StockChart(df=df, stacked=True, normalized=False)
    design = Row(12, chart)
    p.add_slide(layout_num=5, design=design, title='my shiny analysis')
    #
    # SurfaceChart example
    # df = pd.DataFrame({'a': [1, 2, 9], 'b': [4, 1, 6], 'c': [7, 8, 2]})
    # chart = SurfaceChart(df=df, stacked=True, normalized=False)
    # design = Row(12, chart)
    # p.add_slide(layout_num=5, design=design, title='my shiny analysis')

    filename = 'example_allcharts.pptx'

    p.save(filename)
