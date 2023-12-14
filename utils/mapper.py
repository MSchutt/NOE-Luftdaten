from datetime import datetime

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



def format_timestamp(timestamp: datetime, include_time: bool = False) -> str:
    """
    Format a timestamp to a human readable format.
    
    Args:
        timestamp (datetime): The timestamp to format.
        include_time (bool, optional): Whether to include the time in the formatted timestamp. Defaults to False.
        
    Returns:
        str: The formatted timestamp.
    """
    
    return timestamp.strftime(f"%d.%m.%Y{' %H:%M:%S' if include_time else ''}")