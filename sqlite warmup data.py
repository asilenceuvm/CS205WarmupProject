import sqlite3
import csv

def main():
    #connect to database
    connection=sqlite3.connect('spotifyDatabase.db')
    connection.text_factory = str

    #create cursor to execute SQL commands
    c=connection.cursor()

    inputFile = csv.DictReader(open("/Users/derrickleger/CS205WarmupProject/CS205 warmup songsDB.csv"))
    inputFile2= csv.DictReader(open("/Users/derrickleger/CS205WarmupProject/CS205 warmup artistsDB.csv"))

    #create table
    c.execute('''CREATE TABLE IF NOT EXISTS spotifySongData 
        (Rank,TrackName,Streams,TrackId,ArtistId)''')

    c.execute('''CREATE TABLE IF NOT EXISTS spotifyArtistData 
            (I,Artist,ArtistPopularity,ArtistFollowers,ArtistId)''')

    table1="spotifySongData"
    table2="spotifyArtistData"

    #populate DB table1
    for row in inputFile:
        #parse values from table
        rank=float(row['Rank'])
        trackId=row['Track_id']
        streams=int(row['Streams'])
        trackName=row['Track Name']
        artistId=row['Artist_id']

        c.execute("INSERT INTO spotifySongData (Rank,TrackName,Streams,TrackId,ArtistId) VALUES(?,?,?,?,?)",
                  (rank, trackName, streams, trackId, artistId))
        connection.commit()

    printDbTable(c, table1)
    print("")

    i=1
    #populate DB table2
    for row in inputFile2:
        artist = row['Artist']
        popularity = int(row['Artist_popularity'])
        followers = int(row['Artist_follower'])
        artistId2 = row['Artist_id']

        c.execute("INSERT INTO spotifyArtistData (I, Artist,ArtistPopularity,ArtistFollowers,ArtistId) VALUES(?,?,?,?,?)",
                  (i,artist, popularity, followers, artistId2))
        connection.commit()
        i+=1

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
        print row

main()

