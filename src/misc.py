
import pandas as pd
import itertools
from datetime import datetime


#%% Functions that would'nt be put into a specific category

def expand_grid(data_dict: dict) -> pd.DataFrame:
    '''
    Mimics R's "expand.grid" function for python dicts.

    Parameters
    ----------
    data_dict : dict
        Dictionary of all the unique values per column 

    Returns
    -------
    A Dataframe where we took into account all mixes from the dictionary

    '''
    rows = itertools.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())


#%% Function useful when running long pipelines

def step_time(step = 0,
              digits = 2):
    '''
    Function to print a step and time. Step is by default with 2 digits

    Parameters
    ----------
    step : numerical, optional
        step number. The default is 0.
    digits : int, optional
        digits to use to round the step number. The default is 2.

    Returns
    -------
    None.

    '''
    mystr = f"({round(step,digits):.{digits}f}) - [" 
    mystr += datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    
    return(mystr)