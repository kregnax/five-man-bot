import pymysql.cursors
import blizzard

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
        cursor.close()
        db_conn.close()
    return text_commands

def add_new_text_command(db_conn, text_command, text_output):
    try:
        with db_conn as cursor:
            sql = "INSERT INTO tblTextCommands (TextCommand, TextOutput) VALUES ('{}', '{}')".format(text_command, text_output)
            cursor.execute(sql)
    except pymysql.Error as err:
        print("SQL Error: "+str(err))
    finally:
        cursor.close()
        db_conn.close()

def get_battletag_for_discordID(db_conn, discordID):
    battletag = 'Not found'
    try:
        with db_conn as cursor:
            sql = "SELECT Battletag FROM tblDiscord2Battletag WHERE DiscordID = {}".format(discordID)
            cursor.execute(sql)
            battletag = cursor.fetchall()
    except pymysql.Error as err:
        print("SQL Error: "+ str(err))
    finally:
        cursor.close()
        db_conn.close()
    return battletag

def register_discordID_for_battletag(db_conn, discordID, battletag):
    try:
        with db_conn as cursor:
            sql = "INSERT INTO tblDiscord2Battletag (DiscordID, Battletag) VALUES ('{}', '{}')".format(discordID, battletag)
            cursor.execute(sql)
    except pymysql.Error as err:
        print("SQL Error: "+ str(err))
    finally:
        cursor.close()
        db_conn.close()    