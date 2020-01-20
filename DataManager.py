import sqlite3
import os

# Low-level DB functions:

def create_connection(db_file):
    """ create db connection to SQLite db
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    finally:
        return conn

def create_table(conn, table_create):
    """ Create a table using the connection
    :param conn: Connection object to use
    :param table_create: CREATE-query-string to execute
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(table_create)
    except sqlite3.Error as e:
        print(e)

def dbExists():
    """ Checks if the database exists
    :return:
    """
    return os.path.exists("data/metadata.db")

def setupDB(conn):
    """ Sets up the database
    :return:
    """
    createquery = """ CREATE TABLE IF NOT EXISTS pastes (
        id integer PRIMARY KEY,
        pasteId text NOT NULL,
        name text,
        language text,
        user text,
        timestamp text,
        deletiontime text
    )
    """
    create_table(conn, createquery)

def isPasteInDB(conn, pasteID):
    """ Checks if a pasteID is in the database
    :param conn: Connection object to use
    :param pasteID: PasteID String to check
    :return: True if paste exists, False otherwise
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM pastes WHERE pasteId=" + pasteID)
    rows = cur.fetchall()
    return rows.__len__() != 0

# Highlevel Paste Functions:

def isPasteDownloaded(conn, pasteID):
    return os.path.exists("data/content/" + pasteID + ".paste") and isPasteInDB(conn, pasteID)

def savePasteContent(pasteID, content):
    f = open("data/content/" + pasteID + ".paste", "wb")
    f.write(content.encode('utf-8'))
    f.close()

def savePasteMetadata(conn, pasteID, title, language, timestamp, user, deletiontime):
    cur = conn.cursor()
    sql = ''' INSERT INTO pastes(pasteId, name, language, user, timestamp, deletiontime) VALUES(?,?,?,?,?,?) '''
    paste = (pasteID, title, language, user, timestamp, deletiontime)
    cur.execute(sql, paste)
    conn.commit()
    return cur.lastrowid