import inspect


def get_local_variable_name(var):
    """
    Get the real variable name. Will work only if called inside another function

    Parameters
    ----------
    var : str
        The variable we are interested in

    Returns
    -------
    Either the name of it or None


    Example
    -------
    a = 3
    def foo(x):
        print(get_variable_name(x))
    foo(a) # will return "a"
    print(get_variable_name(var = a)) # will return None
    """
    lcls = inspect.stack()[2][0].f_locals
    for name in lcls:
        if id(var) == id(lcls[name]):
            return name
    return None
