import sqlite3 as lite
import csv
import os
import re


validQueries = ['help', 'song', 'artist', 'quit', 'popularity', 'tempo', 'popularity' ,'followers', 'load_database']
db_file = "spotifyDatabase.db"


def load_database():
    # check if already created
    if os.path.exists("spotifyDatabase.db"):
        print("Created database.") # you can change this if u want

    else:
        print('Creating database...')
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
        print("Done!")


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


def select_song_pop(conn, song):
    # song popularity 'songName'
    cur = conn.cursor()

    cur.execute('SELECT tblArtists.Artist,tblSongs.Streams,tblSongs.Rank FROM '
                'tblSongs INNER JOIN tblArtists ON tblSongs.ArtistId = tblArtists.ArtistId WHERE TrackName = "' + song + '"')
    rows = cur.fetchall()

    if len(rows) == 0:
        print("No match was found.")
    else:
        print('"' + song + '" by',rows[0][0],"has been streamed", rows[0][1], "times and ranks number", rows[0][2], "globally.")


def select_tempo(conn, song):
    # song tempo 'songName'
    cur = conn.cursor()

    cur.execute('SELECT Tempo FROM tblSongs WHERE TrackName = "' + song + '"')
    rows = cur.fetchall()
    if len(rows) == 0:
        print("No match was found.")
    else:
        print('"{}" is played at {:.2f} BPM'.format(song, rows[0][0]))


def select_song_artist(conn, song):
    # song artist 'songName'
    cur = conn.cursor()

    cur.execute('SELECT ArtistId FROM tblSongs WHERE TrackName = "' + song + '"')

    artist_id = cur.fetchall()
    cur.execute('SELECT Artist FROM tblArtists WHERE ArtistId = "'+artist_id[0][0]+'"')
    rows = cur.fetchall()
    if len(rows) == 0:
        print("No match was found.")
    else:
        print('"{}" was made by {}'.format(song, rows[0][0]))


def select_by_artist(conn, artist):
    # artist 'name'
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


def select_artist_pop(conn, name):
    # artist popularity 'songName'
    cur = conn.cursor()

    cur.execute('SELECT ArtistPopularity FROM tblArtists WHERE Artist = "'+name+'"')
    rows = cur.fetchall()
    if len(rows) == 0:
        print("No match was found.")
    else:
        print(name + ' has a '+rows[0][0]+'% popularity score on Spotify')


def select_followers(conn, name):
    # artist followers 'songName'
    cur = conn.cursor()

    cur.execute('SELECT ArtistFollowers FROM tblArtists WHERE Artist = "' + name + '"')
    rows = cur.fetchall()
    if len(rows) == 0:
        print("No match was found.")
    else:
        print(name + ' has ' + rows[0][0] + ' followers on Spotify')


def select_top_x(conn, x):

    cur = conn.cursor()

    cur.execute('SELECT Rank, TrackName FROM tblSongs WHERE Rank <= '+ str(x))
    rows = cur.fetchall()
    print('{:<5} {}'.format("Rank", "Song"))
    for row in rows:
        print('{:<5} {}'.format(row[0],row[1]))


def main():

    print("Welcome to the spotify database searching tool, for help type 'help'")
    print("You must input 'load_database' first.")

    query = input(">> ")
    query = re.findall(r'\w+|\"\w+\s+\w+\"', query)
    query = [x.strip('"') for x in query]

    while query[0] != "quit":
        #check query is valid
        while query[0] not in validQueries:
            print("Invalid Query, please try again")
            query = input(">> ")
            query = re.findall(r'\w+|\"\w+\s+\w+\"', query)
            query = [x.strip('"') for x in query]

        #query is quit
        if query[0] == "quit":
            print("Thank you for using our program")
        elif query[0] == "load_database":
            load_database()
            conn = create_connection(db_file)
        elif query[0] == "help":
            print("Artist and song names must be in double quotes.")
            print("song popularity ...")
            print("song artist ...")
            print("song tempo ...")
            print("artist popularity ...")
            print("artist followers ...")
            print("artist  ...")
        try:
            if query[0] == "song":
                if query[1] == "popularity": 
                    select_song_pop(conn, query[2])
                elif query[1] == "artist": 
                    select_song_artist(conn, query[2])
                elif query[1] == "tempo":
                    select_tempo(conn, query[2])

            elif query[0] == "artist":
                if query[1] == "popularity":
                    select_artist_pop(conn, query[2])
                elif query[1] == "followers":
                    select_followers(conn, query[2])
                else:
                    select_by_artist(conn, query[1])
        except:
            print("Invalid Query, please try again or 'help'")

        query = input(">> ")
        query = re.findall(r'\w+|\"\w+\s+\w+\"', query)
        query = [x.strip('"') for x in query]


main()
