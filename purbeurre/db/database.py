# -*- coding: utf-8 -*-
"""database.py."""
import mysql.connector
from mysql.connector import errorcode
import logging
from purbeurre.constants import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


class Mysql:
    """Mysql interface for purbeurre application."""

    def __init__(self):
        """Connection to Mysql.

        :param str db_host:
            Mysql server host.

        :param str db_user:
            Username for access to the database(db_name).

        :param str db_password:
            Password of the username.

        :param str db_name:
            Database name.
        """
        try:
            self.cnx = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error("Something is wrong \
                    with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.error("Database does not exist")
            else:
                logging.error("Something went wrong at the connection :")
                logging.error(err)
            exit(1)

        self.cursor = self.cnx.cursor()

    def execute(self, sql, values=None):
        """Transmit sql request to Mysql server."""
        try:
            if values:
                self.cursor.execute(sql, values)
            else:
                self.cursor.execute(sql)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                logging.error("Table already exists.")
#            elif err.errno == errorcode.ER_NO_SUCH_TABLE_ERROR:
#                logging.error("Table doesn't exist")
#            elif err.errno == errorcode.ER_WRONG_COLUMN_NAME_ERROR:
#                logging.error("Column doesn't exist")
            else:
                logging.error(err.msg)
            logging.error(sql.format(values))
            return -1
        else:
            logging.info("Succeeded")
            logging.info(sql.format(values))
            return 0

    def apply_structure(self):
        """Delete table & apply table structure from structure.sql file."""
        with open('purbeurre/db/structure.sql', 'r') as file:
            lines = file.read()
            lst = lines.split(' ')
            tables = []
            while len(lst) != 0:
                if 'TABLE' == lst.pop(0):
                    tables.append(lst.pop(0))

            tables.reverse()
            for table in tables:
                self.execute("DROP TABLE IF EXISTS " + table)

            lst = lines.split(';')
            lst.pop(len(lst) - 1)
            for sql in lst:
                self.execute(sql)

    def insert(self, table, values):
        """Insert one line of data into the table.

        :param dict values
            key: data
            key = colonne name
            data = data should be inserted

        return the value of id
        """
        sql = "INSERT INTO {} ({}) VALUES ({})"

        data_quantity = ', '.join(['%s' for e in range(len(values))])
        data = tuple([values[key] for key in values])
        sql = sql.format(table, ', '.join([key for key in values]),
                         data_quantity)

        r = self.exists(table, values)
        if r:
            return r
        else:
            self.execute(sql, data)
            self.cnx.commit()
            return self.exists(table, values)

    def query(self, table, values, select='*', **options):
        """Query to database.

        :param str table:
            Same as FROM in sql
            Table name for query

        :param list values

        :param dict options
        """
        if 'distinct' in options:
            sql = "SELECT DISTINCT {} FROM {}".format(select, table)
        else:
            sql = "SELECT {} FROM {}".format(select, table)

        if 'where' in options:
            sql += " WHERE {}".format(options['where'])

        if 'in' in options:
            data_quantity = ', '.join(['%s' for e in range(len(values))])
            sql += " IN {}".format(data_quantity)

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
        self.results = self.cursor.fetchall()

    def exists(self, table, values):
        """Test if these values are recorded in the table.

        if values were found the id is returned,
        if not None is returned
        """
        data = tuple([values[key] for key in values])
        where = " AND ".join([key + "=%s" for key in values])
        self.query(table, data, where=where)
        if len(self.results) == 0:
            return None
        else:
            return self.results[0][0]

    def update(self, table, set, where):
        """Not yet implemented."""
        pass

    def delete(self, table, where):
        """Not yet implemented."""
        pass
