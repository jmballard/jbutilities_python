

from datetime import datetime


#%% Function useful when running long pipelines

def step_time(step = 0,
              digits = 2):
    '''
    Function to print a step and time. Step is by default with 2 digits

    Parameters
    ----------
    step : TYPE, optional
        DESCRIPTION. The default is 0.
    digits : TYPE, optional
        DESCRIPTION. The default is 2.

    Returns
    -------
    None.

    '''
    mystr = f"({round(step,digits):.{digits}f}) - [" 
    mystr += datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    
    return(mystr)