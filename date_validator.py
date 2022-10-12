import datetime


def is_valid_yymmdd_date(date, date_format="%y%m%d"):
    """
    Returns a boolean value based on validity of given date.
    Specifying date format is optional and defaults to YYMMDD format.
    Other formats can be specified as an argument for the date_format parameter.
    """
    try:
        datetime.datetime.strptime(date, date_format)
    except ValueError:
        return False
    else:
        return True
