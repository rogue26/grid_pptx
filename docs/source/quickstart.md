# Quickstart

## Installing grid_pptx
    pip install grid-pptx

## Importing grid_pptx components
The primary objects you will typically work with are `GridPresentation`, `Row`, `Column`, and the various 
components that you can add to a slide, such as `Table`, `LineChart` (and other chart types), and `Text`. You'll also 
need to import `pandas` for any tables or charts. You can import them as follows:

```python
from grid_pptx import GridPresentation, Row, Column
from grid_pptx.components import Text, AreaChart, Table
import pandas as pd
```

## Creating a presentation
`GridSlide` objects can be added once we have created a `GridPresentation` object, so let's create one first.
`GridPresentation` objects have no required arguments, however you'll likely want to set either a `template` (if using 
a pre-existing slide template), or a `slide_size`. Additional optional keyword arguments give you control over 
`header_height`, `footer_height`, `right_margin`, `left_margin`, etc., however the default values will usually be a 
reasonable starting point.

Creating a `GridPresentation` object might look like this:
```python
gp = GridPresentation(
    slide_size='16_9',  # name of slide dimensions -- additional details can be found in the documentation
    header_height=1.5,  # space at the top of the slide reserved for the title, measured in inches
    footer_height=1.0,  # space at the bottom of the slide reserved for the footer, measured in inches
    right_margin=0.25,  # margin on the right side of the slide, measured in inches
    left_margin=0.25  # margin on the left side of the slide, measured in inches
)
```

## Creating a chart component
Before we can create a slide, we have to create the charts and other components that will be shown on the slide.
To create a chart, instantiate the appropriate class from `grid_pptx.components`. The various types of components are 
listed [here](https://google.com), along with examples. All components except for `Text` require a pandas dataframe at a 
minimum. Other available options depend on the chart type and are described in the [documentation]().

Creating an `AreaChart` might look like this:
```python
df = pd.DataFrame({'a': [1, 2, 9], 'b': [4, 1, 6], 'c': [7, 8, 2]})
chart = AreaChart(df=df, stacked=True, normalized=False)
```

## Creating a table component
If using `python-pptx` alone, creating and formatting tables can involve tedious [looping over cells](<link needed>) 
to add values and adjust fonts. Controlling table styles can also involve a bit of [research](<link needed>). 
grid-pptx takes care of this for you, enabling you to dump your pandas dataframe directly to a slide component.

Creating a `Table` using the dataframe defined above is as simple as:
```python
table = Table(df)
```

Optional keyword arguments allow you to control various aspects of the table formatting, including ### add list ###. 
You can read more about table configuration [here](<link needed>).

## Creating a text block component
`Text` components require, at a minimum, some text. Additional optional arguments allow you to control things 
like `font`, `font_size`, `background_color`, etc., as documented [here](<link needed>)

```python
text = Text(text='some highly informative text here')
```

## Designing a slide
When displaying data or the results of data analysis, a simple and effective slide could consist of a simple layout with
1-2 charts or tables and a text box highlighting the takeaways. The popular Bootstrap CSS framework allows developers 
to quickly create a [flexible grid layout](https://getbootstrap.com/docs/4.0/layout/grid/) by dividing any element 
into 12 segments. 12 is a useful number because it can be divided in half (6 - 6), thirds (4 - 4 - 4), 
quarters (3 - 3 - 3 - 3), etc. or combinations of these (3 - 3 - 6) using only integers.


`GridSlide` objects are created usint the `add_slide` method of the `GridPresentation` object.
The method requires a design at a minimum. Designs, which implement a Bootstrap-inspired grid layout, are created using `Row` and `Column` instances. 


The first argument
for both `Row` and `Column` instances is an integer between 1 and 12.


The design must be an instance of the `Row` class.


```python
design = Row(12,
             Column(6, chart),
             Column(6,
                    Row(6, table),
                    Row(6, text)))

gp.add_slide(layout_num=5, design=design, title='my shiny analysis')
```
## Detailed tweaking using `python-pptx`

## Completed script and resulting slide
