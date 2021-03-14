""" Helper functions for testing """
import pandas as pd


def assert_data_equal(data, expected_data):
    """
    Test that two dataframes are the same after changing the
    types of some columns
    """
    data.loc[:, data.columns.str.contains("xG|xA|X|Y")] = data.loc[
        :, data.columns.str.contains("xG|xA|X|Y")
    ].astype(float)
    data.loc[:, ~data.columns.str.contains("xG|xA|X|Y")] = data.loc[
        :, ~data.columns.str.contains("xG|xA|X|Y")
    ].astype(str)
    expected_data.loc[
        :, ~expected_data.columns.str.contains("xG|xA|X|Y")
    ] = expected_data.loc[
        :, ~expected_data.columns.str.contains("xG|xA|X|Y")
    ].astype(
        str
    )
    data.replace({None: "None"}, inplace=True)
    pd.testing.assert_frame_equal(
        data, expected_data, check_dtype=False, atol=6
    )
