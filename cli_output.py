from datetime import date


def print_formatted_table(entries):
    """
    Take a tuple or list as argument for the entries parameter and print neatly
    formatted table.
    """

    # Whitespace padding of header titles.
    header_id = f" ID "
    header_name = f" Name{' ' * 20}"
    header_bday = f" Birthday "
    header = f"¦{header_id}¦{header_name}¦{header_bday}¦"

    # Header frame.
    id_fill = "-" * (len(header_id))
    name_fill = "-" * (len(header_name))
    bday_fill = "-" * (len(header_bday))
    frame = f"+{id_fill}+{name_fill}+{bday_fill}+"

    # Format headers and surrounding frame.
    headers = f"{frame}\n{header}\n{frame}"
    print(headers)

    for entry in entries:
        id_num = entry[0]
        if id_num < 10:
            # Leading blank space to make single digit same len as double digit.
            id_num = f" {id_num}"

        name = entry[1].title()
        # Fill space to make an evenly formatted table.
        fill_space = " " * (len(header_name) - len(name) - 2)
        name = f"{name}{fill_space}"

        bday = _format_date(entry[2])
        # Fill space to make an evenly formatted table.
        fill_space = " " * (len(header_bday) - len(bday) - 2)
        bday = f"{bday}{fill_space}"

        # Format CLI table row.
        output = f"¦ {id_num} ¦ {name} ¦ {bday} ¦"
        print(output)
        # Print bottom border of frame.
        print(frame)


def _format_date(bday):
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


def _get_days_to_bday(bday):
    """Return days left as an integer."""
    today = date.today()

    bday_mm = int(bday[-4:-2])
    bday_dd = int(bday[-2:])
    bday = date(today.year, bday_mm, bday_dd)
    if bday < today:
        bday = bday.replace(year=today.year + 1)

    days_left = abs(bday - today)

    return days_left.days
