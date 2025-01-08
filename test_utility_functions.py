import pandas as pd
import numpy as np
import math


def compFloat(exp, act, atol = 0.00001):
    """
    Compares two floating point values, and returns True if they are equal, False otherwise. Unlike a standard
    numeric comparison math.nan == math.nan = True and math.inf == math.inf = True (these would normally return
    False)
    :param exp: The expected value
    :type exp: float
    :param act: the actual value being tested
    :type act: float
    :param atol: Absolute tolerance used in Numpy.isclose(...) to compare finite floats
    :type atol:
    :return:
    :rtype:
    """

    if not isinstance(exp, float) and not isinstance(act, float):
        # one or the other is not a float, cannot proceed
        return None

    if math.isnan(exp) and math.isnan(act):
        return True
    elif math.isinf(exp) and math.isinf(act):
        return True
    else:
        return np.isclose(exp, act, atol)


def compSeries(exp: pd.Series, act: pd.Series, atol=0.000001):
    """
    Performs a comparison of two Series objects that accounts for nan, inf, and floating point inaccuracies
    :param exp: Object representing expected results
    :type exp: Pandas.Series
    :param act: Object representing actual results
    :type act: Pandas.Series
    :param atol: Absolute tolerance to use with np.isclose function for doing the comparison
    :param atol: float
    :return: True if the Series are equal, False otherwise; None if either of exp or act is not Series object
    :rtype: bool or None
    """

    if isinstance(act, pd.Series) == False or isinstance(exp, pd.Series) == False:
        # one of the arguments is not a series, so this is not a valid call
        return None

    if len(exp) != len(act):
        return False

    if exp.name != act.name:
        return False

    if not exp.index.equals(act.index):
        return False

    if exp.dtype == 'float':
        # the series is a float, so we'll need to do special handling
        # first, create a Series of the index so that we can "apply" over the two Series objects
        idx = pd.Series(exp.index)

        # compare, pairwise, all elements in the two Series
        result = idx.apply(lambda i: compFloat(exp.loc[i], act.loc[i]))

        # return the aggregate result True if all are equal, False otherwise
        return np.all(result)
    else:
        # we should be able to simply compare them with standard operators
        return (exp.equals(act))


def compDataFrame(exp, act, atol=0.000001):
    """
     Performs a comparison of two DataFrame objects that accounts for nan, inf, and floating point inaccuracies
     :param exp: Object representing expected results
     :type exp: Pandas.DataFrame
     :param act: Object representing actual results
     :type act: Pandas.DataFrame
     :param atol: Absolute tolerance to use with np.isclose function for doing the comparison
     :param atol: float
     :return: True if the Series are equal, False otherwise; None if either of exp or act is not Series object
     :rtype: bool or None
     """

    if isinstance(act, pd.DataFrame) == False or isinstance(exp, pd.DataFrame) == False:
        # one of the arguments is not a series, so this is not a valid call
        return None

    if exp.shape != act.shape:
        # exp and act must have the same shape
        return False

    if any(exp.keys() != act.keys()):
        # DataFrames must have the same column names
        return False

    if any(exp.index != act.index):
        # DataFrames must have the same indexes
        return False

    # DataFrames have same shape, indexes, and column names, so we can compare the columns one at a time
    for col in exp.keys():
        if not compSeries(exp[col], act[col]):
            # columns are not equal
            return False

    return True