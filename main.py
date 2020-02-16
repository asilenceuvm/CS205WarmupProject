validQueries = ['help', 'song', 'artist', 'quit']

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
    print(song)

# get top x songs
def getTopX(x):
    print("top " + x)


main()
