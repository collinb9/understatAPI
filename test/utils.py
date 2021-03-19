""" Helper functions for testing """
import pandas as pd


def assert_data_equal(data, expected_data):
    """
    Test that two dataframes are the same after changing the
    types of some columns and getting NaN/None values matched up
    """
    metric_regex = "|".join(
        [
            "xG",
            "xA",
            "X",
            "Y",
            "goals",
            "id$",
            "minute",
            "forecast_",
            "_season",
            "shots",
            "_time",
            "yellow_card",
            "red_card",
            "roster",
            "key_passes",
            "assists",
            "Order",
        ]
    )
    data.loc[:, data.columns.str.contains(metric_regex)] = data.loc[
        :, data.columns.str.contains(metric_regex)
    ].astype(float)
    data.loc[:, ~data.columns.str.contains(metric_regex)] = data.loc[
        :, ~data.columns.str.contains(metric_regex)
    ].astype(str)
    expected_data.loc[
        :, ~expected_data.columns.str.contains(metric_regex)
    ] = expected_data.loc[
        :, ~expected_data.columns.str.contains(metric_regex)
    ].astype(
        str
    )
    data.replace({None: "None"}, inplace=True)
    data.replace({"nan": "None"}, inplace=True)
    data.fillna("None", inplace=True)
    expected_data.replace({"nan": "None"}, inplace=True)
    expected_data.fillna("None", inplace=True)
    data.index = data.index.astype(str)
    expected_data.index = expected_data.index.astype(str)
    pd.testing.assert_frame_equal(
        data, expected_data, check_dtype=False, atol=6
    )
