import sqlite3 as lite
import os


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


def select_by_song_name(conn, song):
    cur = conn.cursor()

    cur.execute('SELECT tblArtists.Artist,tblSongs.Streams,tblSongs.Rank FROM '
                'tblSongs INNER JOIN tblArtists ON tblSongs.ArtistId = tblArtists.ArtistId WHERE TrackName = "' + song + '"')
    rows= cur.fetchall()

    if len(rows) == 0:
        print("No match was found.")
    else:
        print('"' + song + '" by',rows[0][0],"has been streamed", rows[0][1], "times and ranks number", rows[0][2], "globally.")


def select_by_artist(conn, artist):
    cur = conn.cursor()

    cur.execute('SELECT ArtistId FROM tblArtists WHERE Artist ="' + artist + '"')
    artist_id = cur.fetchall()
    cur.execute('SELECT Rank, TrackName, Streams FROM tblSongs WHERE ArtistId ="' + artist_id[0][0] + '"')
    rows = cur.fetchall()
    if len(rows) == 0:
        print('no match.')
    else:
        print(artist, "has the following songs in our database:\n")
        print('{:<5} {:60} {:5}'.format("Rank", "Song", "Views"))
        for row in rows:
            print('{:<5} {:60} {:5}'.format(row[0], row[1], row[2]))


def select_top_x(conn, x):
    cur = conn.cursor()

    cur.execute('SELECT Rank, TrackName FROM tblSongs WHERE Rank <= '+ str(x))
    rows = cur.fetchall()
    print('{:<5} {}'.format("Rank", "Song"))
    for row in rows:
        print('{:<5} {}'.format(row[0],row[1]))


def load_database():
    # create database.
    print("Creating database...")
    # to prevent errors when running more than once, delete previously created db.
    if os.path.exists("spotifyDatabase.db"):
        os.remove("spotifyDatabase.db")

    # connect to database
    conn=lite.connect('spotifyDatabase.db')
    conn.text_factory = str

    #create cursor to execute SQL commands
    c=conn.cursor()

    inputFile = csv.DictReader(open("songsDB.csv"))
    inputFile2= csv.DictReader(open("artistsDB.csv"))
    #create table
    c.execute('''CREATE TABLE IF NOT EXISTS tblSongs (
        Rank INT,
        TrackName TEXT,
        Tempo REAL,
        Streams INT,
        ArtistId TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS tblArtists (
        pmkArtist INTEGER PRIMARY KEY AUTOINCREMENT,
        Artist TEXT,
        ArtistPopularity TEXT,
        ArtistFollowers TEXT,
        ArtistId INT)''')


    #populate DB table1
    for row in inputFile:
        #parse values from table
        rank=float(row['Rank'])
        tempo=float(row['Tempo'])
        streams=int(row['Streams'])
        trackName=row['Track Name']
        artistId=row['Artist_id']

        c.execute("INSERT INTO tblSongs (Rank,TrackName,Tempo, Streams,ArtistId) VALUES(?,?,?,?,?)",
                  (rank, trackName, tempo, streams, artistId))
        conn.commit()



    #populate DB table2
    for row in inputFile2:
        artist = row['Artist']
        popularity = int(row['Artist_popularity'])
        followers = int(row['Artist_follower'])
        artistId2 = row['Artist_id']

        c.execute("INSERT INTO tblArtists (Artist,ArtistPopularity,ArtistFollowers,ArtistId) VALUES(?,?,?,?)",
                  (artist, popularity, followers, artistId2))
        conn.commit()

    conn.close()
    createDatabase.main()
    print("Done!")


def main():
    if os.path.exists("spotifyDatabase.db"):
        print("Database loaded.")
    #else:
   #     load_database()
    # connect to database.
    conn = create_connection(db_file)

    #example: always pass 'conn' to the methods.
    select_top_x(conn, 10)
    '''
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

    '''

main()
