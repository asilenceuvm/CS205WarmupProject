import sqlite3
import csv
import os

def main():
    #connect to database
    connection=sqlite3.connect('spotifyDatabase.db')
    connection.text_factory = str

    #create cursor to execute SQL commands
    c=connection.cursor()

    inputFile = csv.DictReader(open("songsDB.csv"))
    inputFile2= csv.DictReader(open("artistsDB.csv"))

    #create table
    c.execute('''CREATE TABLE IF NOT EXISTS spotifySongData (
        Rank int,
        TrackName text,
        Tempo real,
        Streams int,
        ArtistId text)''')

    c.execute('''CREATE TABLE IF NOT EXISTS spotifyArtistData (
        pmkArtist int AUTO_INCREMENT,
        Artist text,
        ArtistPopularity text,
        ArtistFollowers text,
        ArtistId int)''')

    table1="spotifySongData"
    table2="spotifyArtistData"

    #populate DB table1
    for row in inputFile:
        #parse values from table
        rank=float(row['Rank'])
        tempo=float(row['Tempo'])
        streams=int(row['Streams'])
        trackName=row['Track Name']
        artistId=row['Artist_id']

        c.execute("INSERT INTO spotifySongData (Rank,TrackName,Streams,ArtistId) VALUES(?,?,?,?)",
                  (rank, trackName, streams, artistId))
        connection.commit()

    printDbTable(c, table1)
    print("")

    #populate DB table2
    for row in inputFile2:
        artist = row['Artist']
        popularity = int(row['Artist_popularity'])
        followers = int(row['Artist_follower'])
        artistId2 = row['Artist_id']

        c.execute("INSERT INTO spotifyArtistData (Artist,ArtistPopularity,ArtistFollowers,ArtistId) VALUES(?,?,?,?)",
                  (artist, popularity, followers, artistId2))
        connection.commit()


    print("")
    printDbTable(c, table2)

    #close connection to DB
    connection.close()


def printDbTable(c, db):
    #literally selects data with your cursor
    if(db=="spotifySongData"):
        c.execute("SELECT * FROM spotifySongData")

    if(db=="spotifyArtistData"):
        c.execute("SELECT * FROM spotifyArtistData")

    #rows is equal to everything selected by your cursor
    rows=c.fetchall()

    for row in rows:
        print(row)

main()

