def is_string_or_list_of_strings(obj):
    """Helper function to verify that objects supplied to source_currency and target_currency parameters of __init__ method are either string or list of strings.

    Parameters
    ----------
    obj : any object
        object supplied to source_currency and target_currency parameters of __init__ method

    Returns
    -------
    bool
        boolean representing whether or not the object satisfies the is a string or list of strings
    """
    
    # Check if object is string
    if isinstance(obj, str):
        return True
    # Check if object is list
    elif isinstance(obj, list):
        # Check if list consists solely of strings
        if all(isinstance(item, str) for item in obj):
            return True
        else:
            return False
    else:
        return False