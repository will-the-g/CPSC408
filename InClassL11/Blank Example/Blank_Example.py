#import library
import sqlite3
print('import')

#add path to chinook.db to connect to it
connection = sqlite3.connect("chinook.db")
print('connection: ', connection)

#cursor object that executes SQL commands
cur_obj = connection.cursor()
print('init cursor: ', cur_obj)

#function definitions

#create table
def createQuery():
    create_query = '''
        CREATE TABLE tweet(
            tweetID INTEGER NOT NULL PRIMARY KEY,
            Text VARCHAR(280),
            creationDate DATETIME,
            User VARCHAR(20),
            Likes INTEGER,
            Retweets INTEGER,
            Comments INTEGER
        );
    '''
    # execute the query using the cursor
    cur_obj.execute(create_query)
    
    # comit connection
    connection.commit()
    print('Tweet table successfully created')
def insertQueryHardCode():
    #query to insert a record (hard coded values)
    insert_query = '''
    INSERT INTO tweet 
    VALUES(1, 'This is a tweet', '2022-01-01', "@Clibourne", 1,2,3);
    '''
    #execute, commit, print confirmation
    cur_obj.execute(insert_query)
    connection.commit()
    print ('Inserted hard coded values successfully')

def insertQueryQmark():
    #A tuple with 4 values to be inserted
    record = (2, 'This is not a tweet', '2021-01-02', '@Alice')

    #insert query with q-mark placeholders
    insert_query = '''
    INSERT INTO tweet(tweetID, Text, creationDate, User)
    VALUES (?,?,?,?)
    '''
    #in execute function, pass query and tuple to fill in
    cur_obj.execute(insert_query, record)
    connection.commit()

def insertManyQuery():
    records = [(3, 'hello world', '2021-01-03', '@Eve'),
        (4, 'hello universe', '2021-01-04', '@Bob'),
        (5, 'this is patrick', '2021-01-05', '@pStar')]
    #insert query with q-mark placeholders
    insert_query = '''
    INSERT INTO tweet(tweetID, Text, creationDate, User)
    VALUES (?,?,?,?)
    '''

    #use executemany function for multiple records
    cur_obj.executemany(insert_query, records)
    connection.commit()

#main method
createQuery()
#always close connections when exiting
cur_obj.close()
connection.close()
print('connection closed')