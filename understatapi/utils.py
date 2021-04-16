""" Helper functions for formatting data """
import sys
from typing import List, Union, Dict
import inspect
import re
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


def get_all_methods(cls: type) -> List[str]:
    """
    Get the names of all methods in a class, excluding
    methods decorated with ``@property``, ``@classmethod``, etc

    :param cls: The class to get the methods for
    :return: A list of the names of the methods
    """
    return [meth[0] for meth in inspect.getmembers(cls, inspect.isfunction)]


def get_public_methods(cls: type) -> List[str]:
    """
    Get the names of all public methods in a class

    :param cls: The class to get all public methods for
    :return: A list of the names of the public methods
    """
    methods = get_all_methods(cls)
    methods = [meth for meth in methods if not meth.startswith("_")]
    return methods


def find_endpoints(line: str) -> Union[List[str], None]:
    """
    Find the name of a subclass of
    ``~understatapi.endpoints.base.BaseEndpoint` in a string

    :param line: The string in which to search for the name of a
        ``~understatapi.endpoints.base.BaseEndpoint`` object
    """
    match = re.findall(r"\w+Endpoint", line)
    if match:
        return match
    return None


def str_to_class(modulename: str, classname: str) -> type:
    """
    Get a class by using its name
    """
    return getattr(sys.modules[modulename], classname)
