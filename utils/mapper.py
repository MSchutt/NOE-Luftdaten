MONTH_NAMES_GERMAN = ["Jänner", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]



def map_month_to_monthname_german(month_num: int):
    """
    Maps a month number to the corresponding German month name.
    
    Args:
        month_num (int): The month number (1-12).
        
    Returns:
        str: The German month name corresponding to the given month number.
    """
    
    assert month_num >= 1 and month_num <= 12, "Invalid month number!"
    return MONTH_NAMES_GERMAN[month_num - 1]