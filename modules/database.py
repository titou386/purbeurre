import mysql.connector
from mysql.connector import errorcode


class Database:
    def __init__(self, host_db, user_db, password_db, database_db, db_type):
        self.db_type = db_type
        self.error_encountered = False
        self.error_message = []

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

    def log(self, message):
        if message == 'clear':
            self.error_message = []
            self.error_encountered = False
        else:
            self.error_encountered = True
            self.error_message.append(message)

    def execute(self, sql_command):
        try:
            self.cursor.execute(sql_command)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                self.log("Table already exists.")
            elif err.errno == errorcode.ER_NO_SUCH_TABLE_ERROR:
                self.log("Table doesn't exist")
            elif err.errno == errorcode.ER_WRONG_COLUMN_NAME_ERROR:
                self.log("Column doesn't exist")
            self.log(err.msg)
            self.log(sql_command)
        else:
            print("OK")

    def create_table(self, name, *col, **options):

        sql = "CREATE TABLE IF NOT EXIST {} (".format(name)
        for i, x in enumerate(col):
            if i != 0:
                sql += ', '
            sql += x
        sql += ')'

        for arg in options:
            sql += ' {}={}'.format(arg.upper(), options[arg].upper())

        sql += ';'
        self.execute(sql)

    def insert(self, table, values_order, *values):  # values_order --> list, values --> scale
        sql = "INSERT INTO {} (".format(table)
        for i, val_name in enumerate(values_order):
            if i != 0:
                sql += ', '
            sql += val_name
        sql += ") VALUES "

        for j, line_vals in enumerate(values):
            if j != 0:
                sql += ', '
            for i, val in enumerate(line_vals):
                if i == 0:
                    sql += '('
                if i != 0:
                    sql += ', '
                sql += '\'{}\''.format(val)
            sql += ')'

        sql += ';'
        self.execute(sql)

    def query(self, table, select='*', *where, **options):
        sql = "SELECT {} FROM {}".format(select, table)
        for i, arg in enumerate(where):
            if i == 0:
                sql += " WHERE"
            sql += ' {}'.format(arg)

        for key in options:
            sql += ' {} {}'.format(key.upper(), options[key])
        sql += ';'
        self.execute(sql)

    def update(self, table_name, set, where):
        pass
