import sqlite3


class SQLite3Database:
    """Handles CRUD operations of a SQLite3 database."""

    def __init__(self, path_to_db):
        """
        Init connection to a SQLite3 database specified as an argument, and a cursor.
        """
        self.connection = sqlite3.connect(path_to_db)
        self.cursor = self.connection.cursor()

    def create_table(self, table, columns):
        """
        Method to create a table.
        The table parameter takes a string argument and is used to name the table.
        The column parameter takes a string argument and is used to create the columns
        of the table. Only the name of the columns and the expected datatype needs to
        be given separated by commas. E.g. "name TEXT, age INTEGER".
        """
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS '{table}'" f"({columns});")

        self.connection.commit()

    def insert_row(self, table, columns, values):
        """
        Inserts values given as a string for the second positional argument into table
        specified in the first positional argument as a string.
        The primary key assignment is handled automatically by SQLite3.
        Only the actual values to be inserted are expected in the second positional
        argument. E.g. "'name' , 1".
        """
        self.cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")

        self.connection.commit()

    def update_row(self, table, primary_key, updated_column_values):
        """
        Update given values for row specified by given primary_key in given table.
        Function call example:
            Database.update_row("demo_table", 1, demo_column="New Value")
        This would update the value of the demo_column column to "New Value" for the
        row that has 1 as primary key.
        """
        self.cursor.execute(
            f"UPDATE {table} SET {updated_column_values} WHERE id = {primary_key}"
        )

        self.connection.commit()

    def delete_row(self, table, primary_key):
        """Delete row specified by given primary_key in given table."""
        self.cursor.execute(f"DELETE FROM {table} WHERE id = {primary_key}")

        self.connection.commit()

    def get_row_by_pk(self, table, primary_key):
        """Get row from given table name specified by primary key."""
        self.cursor.execute(f"SELECT * FROM {table} WHERE id = {primary_key}")

        return self.cursor.fetchone()

    def get_row_by_column_value(self, table, column_value):
        """
        Get row from given table name specified by column and its value.
        Comparison agnostic argument given for the column_value parameter is expected
        to be a string containing the column name, comparison operator, and value.
        E.g. "demo_column = 'demo_value'" or "demo_column LIKE '%_value%'".
        """
        self.cursor.execute(f"SELECT * FROM {table} WHERE {column_value}")

        return self.cursor.fetchone()

    def get_all_rows(self, table):
        """Get all rows from specified table."""
        self.cursor.execute(f"SELECT * FROM {table}")

        return self.cursor.fetchall()

    def close_connection(self):
        self.connection.close()
