import sqlite3 as lite
import csv
import os


def main():
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


main()
