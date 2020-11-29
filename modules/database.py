import mysql.connector
from mysql.connector import errorcode


class Mysql:
    def __init__(self, host_db, user_db, password_db, database_db):
        self.db_type = db_type
        self.error_encountered = False
        self.error_msgs = []

        try:
            cnx = mysql.connector.connect(
                host=host_db,
                user=user_db,
                password=password_db,
                database=database_db
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            exit(1)

        self.cursor = cnx.cursor()

    def error(self, msg):
        if msg == 'clear':
            self.error_msgs = []
            self.error_encountered = False
        else:
            self.error_encountered = True
            self.error_msgs.append(msg)

    def execute(self, sql, values):
        try:
            self.cursor.execute(sql, values)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                self.error("Table already exists.")
            elif err.errno == errorcode.ER_NO_SUCH_TABLE_ERROR:
                self.error("Table doesn't exist")
            elif err.errno == errorcode.ER_WRONG_COLUMN_NAME_ERROR:
                self.error("Column doesn't exist")
            self.error(err.msg)
            self.error(sql.format(values))
        else:
            print("OK")

    def create_table(self, name, *col, **options):
        values = ()

        sql = "CREATE TABLE IF NOT EXIST {} ("
        values.append(name)
        for i, x in enumerate(col):
            if i != 0:
                sql += ', '
            sql += '{}'
            values.append(x)
        sql += ')'

        for arg in options:
            sql += ' {}={}'
            values.append(arg.upper())
            values.append(options[arg].upper())

        self.execute(sql, values)

    def insert(self, table, values_order, *values):  # values_order --> list, values --> scale
        values = ()

        sql = "INSERT INTO {} ("
        values.append(table)
        for i, val_name in enumerate(values_order):
            if i != 0:
                sql += ', '
            sql += '{}'
            values.append(val_name)
        sql += ") VALUES "

        for j, line_vals in enumerate(values):
            if j != 0:
                sql += ', '
            for i, val in enumerate(line_vals):
                if i == 0:
                    sql += '('
                if i != 0:
                    sql += ', '
                sql += '\'{}\''
                values.append(val)
            sql += ')'

        self.execute(sql, values)

    def query(self, table, select='*', *where, **options):
        values = ()

        sql = "SELECT {} FROM {}"
        values.append(select)
        values.append(table)
        for i, arg in enumerate(where):
            if i == 0:
                sql += " WHERE"
            sql += ' {}'
            values.append(arg)

        for key in options:
            sql += ' {} {}'
            values.append(key.upper())
            values.append(options[key])

        self.execute(sql, values)

    def update(self, table_name, set, where):
        pass
