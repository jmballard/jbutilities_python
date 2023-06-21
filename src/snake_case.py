from re import sub


def snake_case(string):
    '''
    Get the snake case version of a string
    
    Parameters
    ----------
    string : str
        The string we want to change

    Returns
    -------
    the corrected string

    
    Example
    -------
    sbake_case(string = "aasdkjh213987_@AKh")
    '''
    return '-'.join(
        sub(r"(\s|_|-)+"," ",
        sub(r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
        lambda mo: ' ' + mo.group(0).lower(), string)).split())
 
    # Other way:
    
    #     return'_'.join(
    #         re.sub('([A-Z][a-z]+)',r' \1',
    #         re.sub('([A-Z]+)',r' \1',
    #                re.sub('[()]','',
    #         s.replace('-',' ').\
    #             replace('.','_')))).split()).lower()