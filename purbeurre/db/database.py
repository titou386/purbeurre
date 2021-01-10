"""database.py."""
import mysql.connector
from mysql.connector import errorcode
import logging
from purbeurre.constants import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


class Mysql:
    """Mysql interface for purbeurre application."""

    def __init__(self):
        """Constructor for MySQL connection."""
        try:
            self.cnx = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error("Something is wrong \
                    with your user name or password")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                logging.error("Database does not exist")
            else:
                logging.error("Something went wrong at the connection :")
                logging.error(e)
            exit(1)

        self.cursor = self.cnx.cursor()

    def execute(self, sql, values=None):
        """Transmit sql request to Mysql server.

        Paramaters:
        sql(str): Contains the request (with no value).
        values(tuple): Contains the values.

        Returns:
        Boolean value
            True for successful
            False for failure
        """
        try:
            self.cursor.execute(sql, values)
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                logging.error("Table already exists.")
            else:
                logging.error(e.msg)
            logging.error(sql)
            if values:
                logging.error(values)
            return False
        else:
            logging.info("Succeeded")
            logging.info(sql)
            if values:
                logging.info(values)
            return True

    def apply_structure(self):
        """Apply structure from structure.sql file."""
        with open('purbeurre/db/structure.sql', 'r') as file:
            lines = file.read()

            lst = lines.split(';')
            lst.pop(len(lst) - 1)
            for sql in lst:
                self.execute(sql)

    def insert(self, table, values):
        """Insert one line of data into the table.

        Parameters:
        table(str): Select the table in the database.
        values(dict):
            key: column name in the table.
            data: data should be inserted in that column.

        Returns:
            return the value on the first column if succeeded.
            return None if failed.
        """
        sql = "INSERT INTO {} ({}) VALUES ({})"

        data_quantity = ', '.join(['%s' for e in range(len(values))])
        data = tuple([values[key] for key in values])
        sql = sql.format(table, ', '.join([key for key in values]),
                         data_quantity)

        self.execute(sql, data)
        self.cnx.commit()
        r = self.get(table, values)
        if r:
            return r[0]
        else:
            return None

    def query(self, table, values, select='*', **options):
        """Query to database.

        Parameters:
        table(str): Same as FROM in sql
        values(list): Values ordered in the same order as the request
        select(str): Data selected in the table
        options(dict): Optionnal named parameters :
            distinc(key): (bool)

            join(key): (str) Name the table (works with on)
            on(key): (str) Name the table (works with join)

            where(key): (str) The condition
                like(key): (bool) Generate %s for each item in values
                                  Works with where key.
                inside(key): (bool) Generate %s for each item in values
                                    Works with where key.

            order_by(key): (str) column(s) name should be ordered
                            columns name must be separated with a comma.
                direction key: (str) "ASC" For ascend
                                      (default if key doesn't exist)
                                      "DESC" for descend

            limit(key): (int/str) Number of results
                offset(key): (int/str) where result should be begin

            Returns:
                return the value on the first column if succeeded.
                return None if failed.
        """
        if 'distinct' in options:
            sql = "SELECT DISTINCT {} FROM {}".format(select, table)
        else:
            sql = "SELECT {} FROM {}".format(select, table)

        if 'join' in options and 'on' in options:
            sql += " JOIN {} ON {}".format(options['join'], options['on'])

        if 'where' in options:
            sql += " WHERE {}".format(options['where'])

            if 'like' in options:
                data_quantity = ' AND '.join(['%s' for e in
                                              range(len(values))])
                sql += " LIKE {}".format(data_quantity)

            if 'inside' in options:
                data_quantity = ', '.join(['%s' for e in range(len(values))])
                sql += " IN ({})".format(data_quantity)

        if 'order_by' in options:
            if 'direction' not in options:
                options['direction'] = "ASC"
            sql += " ORDER BY {} {}".format(options['order_by'],
                                            options['direction'].upper())

        if 'limit' in options:
            sql += " LIMIT {}".format(options['limit'])
            if 'offset' in options:
                sql += " OFFSET {}".format(options['offset'])

        self.execute(sql, values)
        try:
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(sql, values)
            logging.error(e.msg)
            return None

    def get_all(self, table, values):
        """Query database and return all results.

        Parameters:
            table(str): Select the table in the database.
            values(dict):
                key: column name in the table.

        Returns:
            return a list of lists if succeeded.
                first list level is each database line matching
                second list level is each column in table
            return None if failed.
        """
        data = tuple([values[key] for key in values])
        where = " AND ".join([key + "=%s" for key in values])
        return self.query(table, data, where=where)

    def get(self, table, values):
        """Query database and return one result.

        Parameters:
            table(str): Select the table in the database.
            values(dict):
                key: column name in the table.

        Returns:
            return the value on the first column if succeeded.
            return None if failed.
        """
        data = tuple([values[key] for key in values])
        where = " AND ".join([key + "=%s" for key in values])
        results = self.query(table, data, where=where, limit=1)
        return results[0] if results else None

    def delete(self, table, values):
        """Delete all matchind data in the table.

        Parameters:
            table(str): Select the table in the database.
            values(dict):
                key: column name in the table.

        Returns:
            Nothing.
        """
        data = tuple([values[key] for key in values])
        where = " AND ".join([key + "=%s" for key in values])
        sql = "DELETE FROM {} WHERE {}".format(table, where)
        self.execute(sql, data)
        self.cnx.commit()
