#imports
from helper import helper
from db_operations import db_operations

#global variables
db_ops = db_operations("playlist.db")

#functions
def startScreen():
    print("Welcome to your playlist!")
    #db_ops.create_songs_table()
    db_ops.populate_songs_table("songs.csv")

#show user menu options
def options():
    print('''Select from the following menu options: 
    1. Find songs by artist
    2. Find songs by genre
    3. Find songs by feature
    4. Edit song by name
    5. Delete song by name
    6. Exit''')
    return helper.get_choice([1,2,3,4,5,6])

#search for songs by artist
def search_by_artist():
    #get list of all artists in table
    query = '''
    SELECT DISTINCT Artist
    FROM songs;
    '''
    print("Artists in playlist: ")
    artists = db_ops.single_attribute(query)

    #show all artists, create dictionary of options, and let user choose
    choices = {}
    for i in range(len(artists)):
        print(i, artists[i])
        choices[i] = artists[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Artist =:artist ORDER BY RANDOM()
    '''
    dictionary = {"artist":choices[index]}
    if num != 0:
        query +="LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

#search songs by genre
def search_by_genre():
    #get list of genres
    query = '''
    SELECT DISTINCT Genre
    FROM songs;
    '''
    print("Genres in playlist:")
    genres = db_ops.single_attribute(query)

    #show genres in table and create dictionary
    choices = {}
    for i in range(len(genres)):
        print(i, genres[i])
        choices[i] = genres[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Genre =:genre ORDER BY RANDOM()
    '''
    dictionary = {"genre":choices[index]}
    if num != 0:
        query +="LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

#search songs table by features
def search_by_feature():
    #features we want to search by
    features = ['Danceability', 'Liveness', 'Loudness']
    choices = {}

    #show features in table and create dictionary
    choices = {}
    for i in range(len(features)):
        print(i, features[i])
        choices[i] = features[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #what order does the user want this returned in?
    print("Do you want results sorted in asc or desc order?")
    order = input("ASC or DESC: ")

    #print results
    query = "SELECT DISTINCT name FROM songs ORDER BY "+choices[index]+" "+order
    dictionary = {}
    if num != 0:
        query +=" LIMIT:lim"
        dictionary["lim"] == num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

def search_by_name():
    songName = input("Enter the name of the song you would like to edit: ")
    songIDquery = f'SELECT * FROM songs WHERE name = "{songName}" LIMIT 1'
    songID = db_ops.single_record(songIDquery)
    songQuery = f'SELECT * FROM songs WHERE songID = "{songID}" LIMIT 1'
    songAttributes = db_ops.select_query(songQuery)[0]
    song_keys = ["Song ID", "Name", "Artist", "Album", "Release Date", "Genre", "Explicit", "Duration", "Energy", "Danceability", "Acousticness", "Liveness", "Loudness"]
    song_dict = dict(zip(song_keys, songAttributes))
    for key, value in song_dict.items():
        print(f"{key}: {value}")
    print('''Enter the number of the Attribute you would like to change:
          1. Song Name
          2. Artist Name
          3. Album Name
          4. Release Date
          5. Explicit Tag
          6. Exit''')
    while (True):
        try:
            editAttribute = input()
            editAttribute = int(editAttribute)
            if 1 <= editAttribute <= 6:
                break
            else:
                print("Number not in range of list given")
        except ValueError:
            print("Please enter a number from the list given")
    match editAttribute:
        case 1:
            editName = input("Enter the new name of the song: ")
            updateQuery = f'UPDATE songs SET Name = "{editName}" WHERE songID = "{songID}"'
            db_ops.modify_query(updateQuery)
        case 2:
            editAlbum = input("Enter the new album for the song: ")
            updateQuery = f'UPDATE songs SET Album = "{editAlbum}" WHERE songID = "{songID}"'
            db_ops.modify_query(updateQuery)
        case 3:
            editArtist = input("Enter the new artist for the song: ")
            updateQuery = f'UPDATE songs SET Artist = "{editArtist}" WHERE songID = "{songID}"'
            db_ops.modify_query(updateQuery)
        case 4:
            editReleaseDate = input("Enter the new release date for the song: ")
            updateQuery = f'UPDATE songs SET releaseDate = "{editReleaseDate}" WHERE songID = "{songID}"'
            db_ops.modify_query(updateQuery)
        case 5:
            editExplicit = input("Enter the new explicit tag for the song: ")
            updateQuery = f'UPDATE songs SET Explicit = "{editExplicit}" WHERE songID = "{songID}"'
            db_ops.modify_query(updateQuery)
        case 6:
            pass



def delete_by_name():
    # select the song by inputted name
    songName = input("Enter the name of the song you would like to edit: ")
    songIDquery = f'SELECT * FROM songs WHERE name = "{songName}" LIMIT 1'
    songID = db_ops.single_record(songIDquery)
    # delete the song from table by songID
    deleteQuery = f'DELETE FROM songs WHERE songID = "{songID}" '
    db_ops.modify_query(deleteQuery)


def insert_songs(file):
    data = helper.data_cleaner(file)
    insertQuery = '''INSERT INTO songs(
        songID, Name, Artist, Album, releaseDate, Genre, Explicit, Duration, Energy, Danceability, Acousticness, Liveness, Loudness)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    db_ops.bulk_insert(insertQuery, data)
#main method
startScreen()

newSongsAnswer = input("Would you like to load some songs? Yes/No")
if newSongsAnswer == "Yes":
    file = input("Enter the file name: ")
    insert_songs(file)
    print("Songs Loaded")

#program loop
while True:
    user_choice = options()
    if user_choice == 1:
        search_by_artist()
    if user_choice == 2:
        search_by_genre()
    if user_choice == 3:
        search_by_feature()
    if user_choice == 4:
        search_by_name()
    if user_choice == 5:
        delete_by_name()
    if user_choice == 6:
        print("Goodbye!")
        break

db_ops.destructor()