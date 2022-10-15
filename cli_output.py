from datetime import date
from typing import Union, List, Tuple


def print_formatted_table(entries: Union[Tuple, List][int, str, str, str]) -> None:
    """
    Take a tuple or list, containing an integer followed by three strings as argument
    for the entries parameter and print neatly formatted table.
    """

    # Whitespace padding of header titles.
    header_id = " ID "
    header_name = f" Name{' ' * 20}"
    header_dd_month = " Birthday "
    header_year = " Turning "
    header = f"¦{header_id}¦{header_name}¦{header_dd_month}¦{header_year}¦"

    # Header frame.
    header_id_fill = "-" * (len(header_id))
    header_name_fill = "-" * (len(header_name))
    header_dd_month_fill = "-" * (len(header_dd_month))
    header_year_fill = "-" * (len(header_year))
    frame = [header_id_fill, header_name_fill, header_dd_month_fill, header_year_fill]
    frame = f"+{'+'.join(frame)}+"

    # Format headers and surrounding frame.
    headers = f"{frame}\n{header}\n{frame}"
    print(headers)

    # Format and print each row.
    for entry in entries:
        id_num = entry[0]
        if id_num < 10:
            # Leading blank space to make single digit same len as double digit.
            id_num = f" {id_num}"

        name = entry[1].title()
        # Fill space to make an evenly formatted table.
        fill_space = " " * (len(header_name) - len(name) - 2)
        name = f"{name}{fill_space}"

        bday_yy = entry[3]
        bday_mmdd = entry[2]
        bday_yymmdd = "".join([bday_yy, bday_mmdd])
        dd_month = _format_yymmdd_date_to_dd_month(bday_yymmdd)
        # Fill space to make an evenly formatted table.
        fill_space = " " * (len(header_dd_month) - len(dd_month) - 2)
        dd_month = f"{dd_month}{fill_space}"

        # Year returned from _get_years_coming_bday() has leading 19.
        # Meaning if someone turns 35 this year, the value returned will be 1935.
        # Convert to string and slice out to work around this.
        years_coming_bday = str(_get_years_coming_bday(bday_yymmdd))[-2:]
        fill_space = " " * (len(header_year) - len(years_coming_bday) - 2)
        years_coming_bday = f"{fill_space}{years_coming_bday}"

        # Format CLI table row.
        output = f"¦ {id_num} ¦ {name} ¦ {dd_month} ¦ {years_coming_bday} ¦"
        print(output)
        # Print bottom border of frame.
        print(frame)


def _format_yymmdd_date_to_dd_month(bday: str) -> str:
    """Format "yyyymmdd", "yymmdd" and "mmdd" dates to "dd month"."""

    # Print days left until birthday if less than 30 days.
    days_left = _get_days_to_bday(bday)
    if days_left <= 30:
        return f"-{days_left} DAYS"

    # Using negative numbers to account for "yyyymmdd" and "mmdd" format.
    dd = int(bday[-2:])
    mm = int(bday[-4:-2])

    # Leading blank space to make single digit same len as double digit date.
    if dd == 1:
        dd = f" {str(dd)}st"
    elif dd == 2:
        dd = f" {str(dd)}nd"
    elif dd == 3:
        dd = f" {str(dd)}rd"
    elif dd >= 4 and dd < 10:
        dd = f" {str(dd)}th"
    elif dd >= 10:
        dd = f"{str(dd)}th"

    # Format numerical month to month to abbreviated text.
    months = {
        1: "jan",
        2: "feb",
        3: "mar",
        4: "apr",
        5: "may",
        6: "jun",
        7: "jul",
        8: "aug",
        9: "sep",
        10: "oct",
        11: "nov",
        12: "dec",
    }

    return f"{dd} {months[mm].capitalize()}"


def _get_days_to_bday(bday: str) -> int:
    """Return days left as an integer."""
    today = date.today()

    bday_mm = int(bday[-4:-2])
    bday_dd = int(bday[-2:])
    bday = date(today.year, bday_mm, bday_dd)
    if bday < today:
        bday = bday.replace(year=today.year + 1)

    days_left = abs(bday - today)

    return days_left.days


def _get_years_coming_bday(bday: str) -> int:
    """Return Nth birthday as an integer."""
    today = date.today()

    bday_yy = int(bday[:-4])
    bday_mm = int(bday[-4:-2])
    bday_dd = int(bday[-2:])
    bday = date(today.year, bday_mm, bday_dd)

    if bday < today:
        years = today.year - bday_yy
    else:
        years = today.year - bday_yy - 1

    return years + 1
