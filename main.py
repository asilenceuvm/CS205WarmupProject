import createDatabase
import sqlite3 as lite

validQueries = ['help', 'song', 'artist', 'quit']
db_file = "spotifyDatabase.db"


def create_connection(db_file):
    """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """

    conn = lite.connect(db_file)
    return conn


def print_table(conn, tableName):
    """
       Query all rows in the given table
       :param conn: the Connection object
       :return:
       """
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + tableName)

    rows = cur.fetchall()

    for row in rows:
        print(row)


def main():
    print("Welcome to the spotify database searching tool, for help type 'help'")

    query = input(">> ")
    query = query.split()
    queryType = query[0]

    while queryType != "quit":
        while queryType not in validQueries:
            print("Ivalid Query, please try again")
            query = input(">> ")
            query = query.split()
            queryType = query[0]

        if queryType == "quit":
            print("Thank you for using our program")
        else:
            if queryType == "help":
                print("TODO: create help output")
            elif queryType == "song":
                getSong(query[1])
            elif queryType == "artist":
                getArtist(query[1])

            query = input(">> ")
            query = query.split()
            queryType = query[0]


# get all songs by artist
def getArtist(artist):
    print(artist)


# rank, times streamed, track id
def getSong(song):
    createDatabase.getSong(song)


# get top x songs
def getTopX(x):
    print("top " + x)


main()
