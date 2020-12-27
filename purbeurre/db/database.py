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
        """Transmit sql request to Mysql server."""
        try:
            if values:
                self.cursor.execute(sql, values)
            else:
                self.cursor.execute(sql)

        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                logging.error("Table already exists.")
#            elif err.errno == errorcode.ER_NO_SUCH_TABLE_ERROR:
#                logging.error("Table doesn't exist")
#            elif err.errno == errorcode.ER_WRONG_COLUMN_NAME_ERROR:
#                logging.error("Column doesn't exist")
            else:
                logging.error(e.msg)
            logging.error(sql.format(values))
            return False
        else:
            logging.info("Succeeded")
            logging.info(sql.format(values))
            return True

    def apply_structure(self):
        """Delete table & apply table structure from structure.sql file."""
        with open('purbeurre/db/structure.sql', 'r') as file:
            lines = file.read()

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

        r = self.get(table, values)
        if r:
            return r[0]
        else:
            self.execute(sql, data)
            self.cnx.commit()
            r = self.get(table, values)
            if r:
                return r[0]
            else:
                return None

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

        if 'join' in options and 'on' in options:
            sql += " JOIN {} ON {}".format(options['join'], options['on'])

        if 'where' in options:
            sql += " WHERE {}".format(options['where'])

            if 'like' in options:
                data_quantity = ' AND '.join(['%s' for e in range(len(values))])
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
        """Simple function query the data.

        if values were found the id is returned,
        if not None is returned
        """
        data = tuple([values[key] for key in values])
        where = " AND ".join([key + "=%s" for key in values])
        results = self.query(table, data, where=where)
        return results

    def get(self, table, values):
        data = tuple([values[key] for key in values])
        where = " AND ".join([key + "=%s" for key in values])
        results = self.query(table, data, where=where, limit=1)
        return results[0] if results else None

    def delete(self, table, values):
        data = tuple([values[key] for key in values])
        where = " AND ".join([key + "=%s" for key in values])
        sql = "DELETE FROM {} WHERE {}".format(table, where)
        self.execute(sql, data)
        self.cnx.commit()

    def get_description(self):
        return [col[0] for col in self.cursor.description]
