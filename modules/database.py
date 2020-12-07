# -*- coding: utf-8 -*-
"""database.py."""
import mysql.connector
from mysql.connector import errorcode
import logging


class Mysql:
    """Mysql interface for purbeurre application."""

    def __init__(self, db_host, db_user, db_password, db_name):
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
            cnx = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
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

        self.cursor = cnx.cursor()

    def execute(self, sql, values):
        """Transmit sql request to Mysql server."""
        try:
            if not values or len(values) == 1:
                self.cursor.execute(sql, values)
            else:
                self.cursor.executemany(sql, values)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                logging.error("Table already exists.")
            elif err.errno == errorcode.ER_NO_SUCH_TABLE_ERROR:
                logging.error("Table doesn't exist")
            elif err.errno == errorcode.ER_WRONG_COLUMN_NAME_ERROR:
                logging.error("Column doesn't exist")
            else:
                logging.error(err.msg)
            logging.error(sql.format(values))
            return 1
        else:
            logging.info("Succeeded")
            logging.info(sql.format(values))
            return 0

    def create_table(self, name, *col, **options):
        """Create one table in the database.

        :param str col:
            Descritpion sql of the colonnes
            ex: "id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT "

        :param dict options
            Option of the table
            ex engine=innodb
        """
        col_sql_format = (', '.join(col))
        sql = "CREATE TABLE {} ({})".format(name, col_sql_format)

        for arg in options:
            sql += (' {}={}'.format(arg.upper(), options[arg].upper()))

        return self.execute(sql)


    def insert(self, table, values_names, values):
        """Insert one or few lines of data into the table.

        :param list values_names
            List of colonnes names
            (Must be the same keys values)

        :param dict values
            key: data
            key = colonne name
            data = data should be inserted
        """
        sql = "INSERT INTO {} ({}) VALUES ({})"

        data_quantity = ', '.join(['%s' for e in range(len(values_names))])
        data = [(tuple([val[name]
                for name in values_names])) for val in values]

        sql = sql.format(table, ', '.join(values_names), data_quantity)

        return self.execute(sql, data)

    def query(self, table, *values, select='*', **options):
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

        return self.execute(sql, values)

    def update(self, table, set, where):
        """Not yet implemented."""
        pass

    def delete(self, table, where):
        """Not yet implemented."""
        pass
