import numpy as np
import pandas as pd
import emoji
import re
import math

from snake_case import snake_case

# %% check data quality functions


def check_format_df(df, digits=2):
    """
    What is checked:
    - The format of the table: data.table, data.frame or tibble?
    - The names of the columns needed: only letters, integers or "_"
    - The format of the columns: contains only factors and numeric columns
    - Missing data per column
    - Other strange values: "NaN", "NA", or +/- Inf

    And a summary is created on all variables

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    digits : TYPE, optional
        DESCRIPTION. The default is 2.

    Raises
    ------
    TypeError
        DESCRIPTION.

    Returns
    -------
    None.

    Example
    -------
    from sklearn import datasets
    iris = datasets.load_iris(as_frame = True)
    data = iris.frame
    data['target'] = data['target'].map({0:'setosa',1:'versicolor',2:'virginica'})
    data['target'] = data['target'].astype('category')
    check_format_df(df = data, digits = 2)


    """
    if not isinstance(digits, (int)):
        raise TypeError(
            "The input 'digits' is not of the correct format. Needs an integer."
        )

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "The input 'data' is not of the correct format. Needs a dataset."
        )

    def happy(string):
        print(
            emoji.emojize(
                "\033[1; 32m :smiley: : " + string + "\033[0 m", language="alias"
            )
        )

    def unhappy(string):
        print(
            emoji.emojize("\033[1; 31m :x: : " + string + "\033[0 m", language="alias")
        )

    df_summary = np.transpose(df.describe(include="all", datetime_is_numeric=True))
    for col in ["mean", "std", "min", "25%", "50%", "75%", "max"]:
        df_summary[col] = np.round(pd.to_numeric(df_summary[col]), digits)

    # corrected names
    df_summary["columns_snake_case"] = df_summary.index.map(lambda x: snake_case(x))

    if any(df_summary.index != df_summary["columns_snake_case"]):
        unhappy("There are columns with names that are not in accepted format:")
        for col in df_summary.index[
            df_summary.index != df_summary["columns_snake_case"]
        ]:
            unhappy(
                f"\t- The column {col} should have been {df_summary.loc[col,'columns_snake_case']}"
            )
    else:
        happy("All column names have correct format.")

    # type of the column
    df_summary["data_type"] = pd.DataFrame(df.dtypes)

    if any(df_summary["data_type"] == "object"):
        unhappy("There are columns with type 'object':")
        for col in df_summary.index[df_summary["data_type"] == "object"]:
            unhappy(f"\t- The column {col}")
    else:
        happy("ALl columns have correct type")

    # type of column between numerical and categorical
    df_summary["type_cat_or_num"] = ""
    for col in df.columns:
        try:
            pd.to_numeric(df[col])
            df_summary.loc[col, "type_cat_or_num"] = "Numerical"
        except:
            df_summary.loc[col, "type_cat_or_num"] = "Categorical"

    # percentage of missing values
    df_summary["missing_rows_pct"] = np.round(
        pd.DataFrame(df.isna().sum() / df.shape[0]) * 100, digits
    )

    if any(df_summary["missing_rows_pct"] > 0):
        unhappy("There are some missing values:")
        for col in df_summary.index[df_summary["missing_rows_pct"] > 0]:
            unhappy(
                f"\t- The column {col} has {df_summary.loc[col,'missing_rows_pct']}% missing value"
            )
    else:
        happy("All the columns are full")

    # percentage of infinite values
    df_summary["infinite_rows_pct"] = np.round(
        pd.DataFrame(((df == math.inf) | (df == -math.inf)).sum() / df.shape[0]) * 100,
        digits,
    )

    if any(df_summary["infinite_rows_pct"] > 0):
        unhappy("There are some infinite values:")
        for col in df_summary.index[df_summary["infinite_rows_pct"] > 0]:
            unhappy(
                f"\t- The column {col} has {df_summary.loc[col,'infinite_rows_pct']}% infinite value"
            )
    else:
        happy("All the columns are finite")

    # number of levels/categories
    df_summary["num_levels"] = pd.DataFrame(df.nunique())

    df_summary = df_summary[
        [
            "columns_snake_case",
            "data_type",
            "type_cat_or_num",
            "count",
            "missing_rows_pct",
            "infinite_rows_pct",
            "mean",
            "std",
            "min",
            "25%",
            "50%",
            "75%",
            "max",
            "num_levels",
            "top",
            "freq",
        ]
    ]
    return df_summary


# %% Cleaning data functions
