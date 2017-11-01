import pymysql.cursors

def get_connection(db_dictionary):
    return pymysql.connect(
        host=db_dictionary['JAWSDB_HOST'],
        user=db_dictionary['JAWSDB_USER'],
        password=db_dictionary['JAWSDB_PASS'],
        db=db_dictionary['JAWSDB_NAME'])

def get_text_commands_dict(db_conn):
    try:
        with db_conn as cursor:
            sql = "SELECT * FROM tblTextCommands"
            cursor.execute(sql)
            result = cursor.fetchall()
            text_commands = dict((y,z) for x, y, z in result)
    finally:
        db_conn.close()
    return text_commands

def add_new_text_command(db_conn, text_command, text_output):
    try:
        with db_conn as cursor:
            sql = "INSERT INTO tblTextCommands (TextCommand, TextOutput) "+\
                  "VALUES ({}, {})".format(text_command, text_output)
            print(sql)
            cursor.execute(sql)
    finally:
        db_conn.close()
