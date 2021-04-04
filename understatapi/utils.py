""" Helper functions for formatting data """
from typing import List, Union, Dict
from numpy.typing import ArrayLike
import pandas as pd
import numpy as np


def json_to_dataframe(
    data: Union[List[Dict[str, ArrayLike]], Dict[str, ArrayLike]],
    **kwargs: str,
) -> pd.DataFrame:
    """
    Convert output of ``json.loads()`` to a dataframe

    :param data: Output of ``json.loads()``
    :param kwargs: Keyword arguments to pass to
        ``pd.DataFrame.from_dict()`` (if ``data`` is a dictionary)
    """
    try:
        data = pd.DataFrame.from_dict(data, **kwargs)
    except AttributeError:
        data = pd.DataFrame(data)
    return data


def try_json_normalize(col: pd.Series) -> pd.DataFrame:
    """
    Try to apply ``pd.json_normalize()`` to a column of a pd.DataFrame.
    Otherwise just convert the series into a dataframe

    :param col: Column to which ``pd.json_normalize()`` will be
        applied
    """
    try:
        keys = col.iloc[0].keys()
        replace_with = {key: np.nan for key in keys}
        col = col.map(lambda x: replace_with if pd.isnull(x) else x)
        col = pd.json_normalize(col).add_prefix(f"{col.name}_")
    except (TypeError, AttributeError):
        col = pd.DataFrame(col)
    return col


def unpack_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    """
    Unpack each column in a dataframe whose entries are dictionaries
    into separate columns. The new columns are named by combining the
    original collumn name with the corresponding key in the dictionary

    :param data: A dataframe with nested columns
    :rtype: ``pd.DataFrame``

    :Example:

    .. testsetup::

        from understatapi.utils import unpack_dataframe

    .. doctest::

        >>> import pandas as pd
        >>> data= pd.DataFrame(
        ...     data=[[{"ham": 1, "eggs": 2}]],
        ...     columns=["spam"]
        ... )
        >>> print(data)
                            spam
        0  {'ham': 1, 'eggs': 2}
        >>> unpacked_data = unpack_dataframe(data)
        >>> print(unpacked_data)
           spam_ham  spam_eggs
        0         1          2

    """
    data = pd.concat(
        [try_json_normalize(data[col]) for col in data.columns],
        axis=1,
    )
    return data
