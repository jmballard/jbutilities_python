from datetime import datetime

import numpy as np
import pandas as pd

from toolkit.get_variable_name import get_local_variable_name
from toolkit.snake_case import snake_case

# %% Create random data frame


def create_df_rd(size=10, seed=None, numerics=None, booleans=None, categories=None):
    """
    A function to create a dataset containing :
    - a ID column containing ID from 0 to the size-1
    - normally distributed variables (if None, no column)
    - factors variables with the levels given by list input (if None, no column)
    - Booleans with binomial distributions with list input (if None, no column)


    Parameters
    ----------
    size : int
        number of profiles to create.
    seed : int or None, optional
        Seed for reproducibility. If None, a seed is randomly created.
        The default is None.
    numerics : dict
        Normally distributed numeric columns. Keys are the names.
        Values are either None or a list of length 2 with mean and std.
    booleans : dict
        Binomial distributed columns. Keys are the names.
        Values are either None or a float which is the probability of True values.
    categories : dict
        Multinomial distributed columns. Keys are the names.
        Values are either None or a list of categorical values.
        The probabilities will be 1/N if a column has N unique values

    Returns
    -------
    random DataFrame.


    Example
    -------
    create_df_rd(size = 10,
                 seed = None,
                 numerics = {"" : None,
                             "num2" : [0,1]},
                 booleans = {"bool1" : 0.5},
                 categories = {'a' : [1,2,3],
                               'b' : ["F","M"]})


    """

    # check inputs
    print("We check the inputs...")
    if not isinstance(size, int):
        raise TypeError(
            "The input 'size' is not of the correct format. Needs an integer."
        )

    if seed is None:
        seed = (
            datetime.now().hour * 3600
            + datetime.now().minute * 60
            + datetime.now().second
        )
        print(f"\tSeed is None, we set it to {seed}")
    elif not isinstance(seed, int):
        raise TypeError(
            "The input 'seed' is not of the correct format. Needs an integer."
        )

    # check format of the 3 other columns
    def check_feature_instance(feature, instance):
        """
        Check if none and if is a dictionary of instance without null values
        """
        if feature is None:
            print(f"\t'{get_local_variable_name(feature)!r}' is None.")
        elif (isinstance(feature, dict)) & all(
            (val is None) | isinstance(val, instance) for val in feature.values()
        ):
            print(
                f"\tWe have {len(feature)} {get_local_variable_name(feature)} columns"
            )
        else:
            raise TypeError(
                f"'{get_local_variable_name(feature)!r}' is not of the correct format."
            )

    check_feature_instance(feature=numerics, instance=list)
    check_feature_instance(feature=booleans, instance=float)
    check_feature_instance(feature=categories, instance=list)

    # Check format of the new names
    print("We check the format of the new columns' name")

    def correct_input_names(dico, default):
        if dico is not None:
            i = 1
            dict_replace = {}
            for key in dico.keys():
                if key == "":
                    print(f"\tWe replace column '' by {default}" + str(i))
                    dict_replace[default + str(i)] = key
                else:
                    dict_replace[snake_case(key)] = key
                    if snake_case(key) != key:
                        print("\tWe replace column " + key + " by " + snake_case(key))
                i += 1
            for newkey, oldkey in dict_replace.items():
                dico[newkey] = dico.pop(oldkey)
        return dico

    numerics = correct_input_names(numerics, default="num_")
    booleans = correct_input_names(booleans, default="bool_")
    categories = correct_input_names(categories, default="cat_")

    # Creation of the DataFrame
    print("We create the DataFrame")
    df = pd.DataFrame({"id": np.arange(size)})
    i = 0
    if numerics is not None:
        for key, val in numerics.items():
            np.random.seed(seed + i)
            if val is None:
                print(f"\tThe column '{key!r}' is normaly distributed (0,1)")
                df[key] = np.random.normal(loc=0, scale=1, size=size)
            else:
                print(f"\tThe column '{key!r}' is normal, ({val[0]!r} , {val[1]!r})")
                df[key] = np.random.normal(loc=val[0], scale=val[1], size=size)
            i += 1

    if booleans is not None:
        for key, val in booleans.items():
            np.random.seed(seed + i)
            if val is None:
                print(
                    f"\tThe column '{key!r}' is binomialy distributed with proba 0.5 of having 1"
                )
                df[key] = np.random.binomial(n=1, p=0.5, size=size).astype("bool")
            else:
                print(
                    f"\tThe column '{key!r}' is binomialy distributed with proba {val} of having 1"
                )
                df[key] = np.random.binomial(n=1, p=val, size=size).astype("bool")
            i += 1

    if categories is not None:
        for key, val in categories.items():
            np.random.seed(seed + i)
            if val is None:
                print(f"\tThe column '{key!r}' needs at least one value")
            elif len(val) == 1:
                print(f"\tThe column '{key!r}' needs is set to {val[0]!r}")
                df[key] = val[0]
            else:
                print(
                    f"\tThe column '{key!r}' is binomialy distributed with proba {round(1 / len(val), 2)!r} for each value"
                )
                answers = pd.DataFrame(
                    np.random.multinomial(
                        n=1, pvals=[1 / len(val) for i in range(len(val))], size=size
                    )
                )
                df[key] = val[0]
                for j in range(1, len(val)):
                    df[key] = np.where(answers[j] == 1, val[j], df[key])
                df[key] = df[key].astype("category")

            i += 1

    return df
