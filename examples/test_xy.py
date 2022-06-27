import pandas as pd

if __name__ == '__main__':  # pragma: no cover

    # multi_index = pd.MultiIndex.from_tuples([("r0", "rA"),
    #                                          ("r1", "rB")],
    #                                         names=['Courses', 'Fee'])

    cols = pd.MultiIndex.from_tuples([
        ("Gasoline", "Toyota"),
        ("Gasoline", "Ford"),
        ("Electric", "Toyota"),
        ("Electric", "Tesla"),
        ("Something", "Blah"),
        ("Something", "Fubar"),
    ])

    data = [
        [100, 300, 900, 400, 200, 500],
        [200, 500, 300, 600, 600, 900]
    ]

    df = pd.DataFrame(data, columns=cols)

    # 1. Check if multiindex
    print(isinstance(df.columns, pd.MultiIndex))

    # 2. If multi-index, how many levels, xy or bubble plot must have either 1 or 2 levels to columns
    print(df.columns.nlevels)

    # 3. If only one level, then x, y, and bubble size columns must be given to the chart.

    # 4. If two levels, then x, y, and bubble size columns still must be given to the chart, but we can see how many
    # higher level indices have those 2-3 (depending on chart type) values. Each of those will be a separate series
    print(df)
    print(df.columns.isin(['Toyota', 'Ford'], level=1))

    axis_vals_list = ['Toyota', 'Ford']

    series_list = []
    for series_candidate in df.columns.get_level_values(0).unique():
        axis_vals_in_series = df.loc[:, (series_candidate, slice(None))].columns.get_level_values(1).tolist()

        print('series_candidate = ', series_candidate)
        print('axis_vals_in_series = ', axis_vals_in_series)

        if all(_ in axis_vals_in_series for _ in axis_vals_list):
            print('this is a series')
        else:
            print('this is not a series')
        print()

    # series_list = [_ for _ in df.columns.get_level_values(0).unique() if all(_ in List1 for _ in List2)]
    # print(series_list)
    # print(
    #     df.loc[:,df.columns.isin(['Toyota', 'Ford'], level=1)]
    # )
    # df[df.index.get_level_values('PBL_AWI').isin(['Lake', 'River', 'Upland'])]
