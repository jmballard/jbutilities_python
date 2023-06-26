import os


# %% Functions


def find_series(name_file, type_file):
    """
    Function to find the latest file in a series. If a file doesn't exist, the function returns None.

    Parameters
    ----------
    name_file : str
        Name of the file.
        If file not at the working directory, add the path to it.
    type_file : str
        Extension of the file.

    Returns
    -------
    either None or the latest file in the serie.

    Example
    -------
    find_series(name_file = "test",
                type_file = "csv")


    """

    # check of inputs
    if not isinstance(name_file, str):
        raise TypeError(
            "The input 'name_file' is not of the correct format. Needs a string."
        )

    if not isinstance(type_file, str):
        raise TypeError(
            "The input 'type_file' is not of the correct format. Needs a string."
        )

    if name_file == "":
        raise ValueError("The input 'name_file' is empty")

    if type_file == "":
        raise ValueError("The input 'name_file' is empty")

    # main body
    f = name_file + "." + type_file
    if not os.path.exists(f):
        print(f"The file {f} doesn't exist")
        return None
    i = 1
    while os.path.exists(f):
        f1 = name_file + "_" + str(i) + "." + type_file
        if not os.path.exists(f1):
            return f
        i += 1
        f = f1


def name_series(name_file, type_file):
    """
    Function to create files without over writing them.
    It will add an underscore and the next number of the series.

    Parameters
    ----------
    name_file : str
        Name of the file.
        If file not at the working directory, add the path to it.
    type_file : str
        Extension of the file.

    Returns
    -------
    The next installation of the series.

    Example
    -------
    find_series(name_file = "test",
                type_file = "csv")

    """
    # check of inputs
    if not isinstance(name_file, str):
        raise TypeError(
            "The input 'name_file' is not of the correct format. Needs a string."
        )

    if not isinstance(type_file, str):
        raise TypeError(
            "The input 'type_file' is not of the correct format. Needs a string."
        )

    if name_file == "":
        raise ValueError("The input 'name_file' is empty")

    if type_file == "":
        raise ValueError("The input 'name_file' is empty")

    # main body
    f = name_file + "." + type_file
    if not os.path.exists(f):
        return f
    i = 1
    while os.path.exists(f):
        f = name_file + "_" + str(i) + "." + type_file
        i += 1
    return f
