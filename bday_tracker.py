import argparse
import pathlib

from db_sqlite3 import SQLite3Database
from date_validator import is_valid_yymmdd_date
from cli_output import print_formatted_table

# Settings.
PATH_TO_DB = f"{pathlib.Path(__file__).parent.resolve()}/db_bdays.sqlite3"
TABLE = "birthdays"
COLUMNS = "id INTEGER PRIMARY KEY, name TEXT, birthday TEXT, year_of_birth TEXT"
COLUMN_NAMES = "name, birthday, year_of_birth"

# Database.
db = SQLite3Database(PATH_TO_DB)
db.create_table(TABLE, COLUMNS)

# Parse CLI arguments.
parser = argparse.ArgumentParser()
# New entry.
parser.add_argument(
    "-n",
    "--new_entry",
    nargs=2,
    help=(
        """
        Add new Bday Tracker entry. Accepts two arguments:
        One for the name of a person, and another for that persons birthday.
        Date of birthday are to be given in YYMMDD format.
        """
    ),
)
# Remove entry.
parser.add_argument(
    "-rm",
    "--remove",
    nargs="+",
    help=(
        """
        Remove entry by ID.
        Multiple IDs can be given, separated by space, to remove multiple entries.
        """
    ),
)
args = parser.parse_args()

# Remove a single or multiple entries.
if args.remove:
    primary_keys = args.remove
    for pk in primary_keys:
        db.delete_row(TABLE, pk)

# Add new entry.
elif args.new_entry:
    # Determine what element of the list of args is a numerical date.
    # Can be given in any order in the CLI argument.
    try:
        birthday = int(args.new_entry[1])
    except ValueError:
        # First element consists of numerical characters.
        name = args.new_entry[1]
        birthday = args.new_entry[0]
    else:
        # Last element consists of numerical characters.
        name = args.new_entry[0]
        birthday = args.new_entry[1]

    # Ensure YYMMDD format.
    # Separate year, month, and day.
    birthday_yy = birthday[:-4]
    birthday_mm = birthday[-4:-2]
    birthday_dd = birthday[-2:]
    # Ensure year is in YY format and not YYYY.
    birthday_yy = birthday_yy[-2:]

    # Parse and validate YYMMDD date.
    birthday = "".join([birthday_yy, birthday_mm, birthday_dd])
    if is_valid_yymmdd_date(birthday):
        # Concatenate month and day.
        birthday_mmdd = "".join([birthday_mm, birthday_dd])
        # Write to database.
        values = f"'{name}', '{birthday_mmdd}', '{birthday_yy}'"
        db.insert_row(TABLE, COLUMN_NAMES, values)
    else:
        print("Given date of birth is not a valid date.\nNo entry was made.")
else:
    # Show all entries if no CLI arguments are given.
    sql_clause_order_by_mmdd_date = "ORDER BY birthday"
    entries = db.get_all_rows(TABLE, sql_clause_order_by_mmdd_date)

    if len(entries) > 0:
        # for entry in entries:
        #     print(entry)
        print_formatted_table(entries)
    else:
        print("No birthdays tracked.\nPlease add birthdays.")

db.close_connection()
