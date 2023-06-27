from math import nan

import numpy as np
import pandas as pd
from sklearn import datasets

# functions to test
import data_creation
import data_quality


def test_data_creation():
    expected = pd.DataFrame(
        {
            "id": range(10),
            "num_1": [
                0.471435,
                -1.190976,
                1.432707,
                -0.312652,
                -0.720589,
                0.887163,
                0.859588,
                -0.636524,
                0.015696,
                -2.242685,
            ],
            "num2": [
                0.689382,
                -0.031712,
                0.668054,
                0.488838,
                -0.679788,
                -1.307479,
                1.470304,
                -1.231027,
                0.958775,
                0.74049,
            ],
            "bool1": [
                False,
                False,
                True,
                True,
                False,
                True,
                False,
                False,
                False,
                False,
            ],
            "a": [1, 1, 1, 3, 3, 3, 2, 1, 1, 2],
            "b": ["F", "M", "M", "M", "M", "F", "M", "M", "F", "F"],
        }
    )

    actual = data_creation.create_df_rd(
        size=10,
        seed=1234,
        numerics={"": None, "num2": [0, 1]},
        booleans={"bool1": 0.5},
        categories={"a": [1, 2, 3], "b": ["F", "M"]},
    )

    assert all(actual == expected)


def test_data_summary():
    iris = datasets.load_iris(as_frame=True)
    data = iris.frame
    data["target"] = data["target"].map({0: "setosa", 1: "versicolor", 2: "virginica"})
    data["target"] = data["target"].astype("category")

    expected = pd.DataFrame(
        {
            "columns_snake_case": [
                "sepal-length-(-cm)",
                "sepal-width-(-cm)",
                "petal-length-(-cm)",
                "petal-width-(-cm)",
                "target",
            ],
            "data_type": ["float64", "float64", "float64", "float64", "category"],
            "type_cat_or_num": [
                "Numerical",
                "Numerical",
                "Numerical",
                "Numerical",
                "Categorical",
            ],
            "count": [150.0, 150.0, 150.0, 150.0, 150],
            "missing_rows_pct": [0.0, 0.0, 0.0, 0.0, 0.0],
            "infinite_rows_pct": [0.0, 0.0, 0.0, 0.0, 0.0],
            "mean": [5.84, 3.06, 3.76, 1.2, np.nan],
            "std": [0.83, 0.44, 1.77, 0.76, np.nan],
            "min": [4.3, 2.0, 1.0, 0.1, np.nan],
            "25%": [5.1, 2.8, 1.6, 0.3, np.nan],
            "50%": [5.8, 3.0, 4.35, 1.3, np.nan],
            "75%": [6.4, 3.3, 5.1, 1.8, np.nan],
            "max": [7.9, 4.4, 6.9, 2.5, np.nan],
            "num_levels": [35, 23, 43, 22, 3],
            "top": [np.nan, np.nan, np.nan, np.nan, "setosa"],
            "freq": [np.nan, np.nan, np.nan, np.nan, 50],
        },
        index=[
            "sepal length (cm)",
            "sepal width (cm)",
            "petal length (cm)",
            "petal width (cm)",
            "target",
        ],
    )

    actual = data_quality.check_format_df(df=data, digits=2)

    assert all(actual == expected)
