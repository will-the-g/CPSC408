import mysql.connector
from helper import helper

class db_operations():
    # constructor with connection path to DB
    def __init__(self, host, user, password, database):
        # connects to mysql without database
        self.connection = mysql.connector.connect(
            host = host,
            user = user,
            password = password
        )
        self.cursor = self.connection.cursor()
        # checks if the database already exists, then creates it if it doesn't
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        self.cursor.close()
        self.connection.close()
        # reconnects with the database parameter knowing it exists (also allows better reproducability)
        self.connection = mysql.connector.connect(host=host,user=user,password=password,database=database)
        self.cursor = self.connection.cursor()
        print("connection made..")

    # function to simply execute a DDL or DML query.
    # commits query, returns no results. 
    # best used for insert/update/delete queries with no parameters
    def modify_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    # function to simply execute a DDL or DML query with parameters
    # commits query, returns no results. 
    # best used for insert/update/delete queries with named placeholders
    def modify_query_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        self.connection.commit()

    # function to simply execute a DQL query
    # does not commit, returns results
    # best used for select queries with no parameters
    def select_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    # function to simply execute a DQL query with parameters
    # does not commit, returns results
    # best used for select queries with named placeholders
    def select_query_params(self, query, dictionary):
        result = self.cursor.execute(query, dictionary)
        return result.fetchall()

    def single_row(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()
    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with no parameters
    def single_record(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with named placeholders
    def single_record_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        return self.cursor.fetchone()[0]
    
    # function to return a single attribute for all records 
    # from some table.
    # best used for select statements with no parameters
    def single_attribute(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        results.remove(None)
        return results
    
    # function to return a single attribute for all records 
    # from some table.
    # best used for select statements with named placeholders
    def single_attribute_params(self, query, dictionary):
        self.cursor.execute(query,dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results
    
    
    # function that creates the tables in our rideshare database
    def create_tables(self):
        query = '''
        CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        password VARCHAR(20) NOT NULL
        );
        '''
        self.cursor.execute(query)
        #self.cursor.execute("DROP TABLE rides;") # in case table rules need to be changed
        #self.cursor.execute("DROP TABLE driverAccounts;")
        query = '''
        CREATE TABLE IF NOT EXISTS driverAccounts (
            driverID INTEGER PRIMARY KEY NOT NULL UNIQUE,
            isActive BOOLEAN DEFAULT FALSE,
            averageRating DECIMAL(3,2) DEFAULT 0 CHECK (averageRating >= 0),
            ratingCount INTEGER DEFAULT 0 CHECK (ratingCount >= 0),
            FOREIGN KEY (driverID) REFERENCES accounts(id) ON DELETE CASCADE

        );
        '''
        self.cursor.execute(query)
        query = '''
        CREATE TABLE IF NOT EXISTS rides (
            rideID INTEGER PRIMARY KEY NOT NULL UNIQUE,
            driverID INTEGER REFERENCES driverAccounts(driverID),
            riderID INTEGER REFERENCES accounts(id),
            startDateTime DATETIME,
            pickup VARCHAR(30),
            dropoff VARCHAR(30),
            rating INTEGER DEFAULT 0 CHECK (rating >= 0 AND rating <= 5)
        );
            '''
        self.cursor.execute(query)
        self.connection.commit()
        print('Tables Created')
    def populate_tables(self):
        # only populates the tables with arbitrary data for testing if they're empty already
        self.cursor.execute("SELECT COUNT(*) FROM accounts")
        if self.cursor.fetchone()[0] == 0:
            query = '''
            INSERT INTO accounts (id, password) VALUES
                (1, 'password123'),
                (2, 'something456'),
                (3, 'cpsc408'),
                (4, '34rsdf5'),
                (5, '4f6w34gd'),
                (6, test123),
                (7, test123),
                (8, test234),
                (9, test2344),
                (10, test124);

            '''
            self.cursor.execute(query)
        self.cursor.execute("SELECT COUNT(*) FROM driverAccounts")
        if self.cursor.fetchone()[0] == 0:
            query = '''
            INSERT INTO driverAccounts (driverID, isActive, averageRating, ratingCount) VALUES
            (1, TRUE, 4.50, 10),
            (2, TRUE, 3.80, 5),
            (3, FALSE, 0, 0),
            (4, TRUE, 4.90, 20),
            (5, TRUE, 4.25, 15);
            (6, FALSE)
            (7, FALSE)
            '''
            self.cursor.execute(query)
        self.cursor.execute("SELECT COUNT(*) FROM rides") 
        if self.cursor.fetchone()[0] == 0:
            
            query = '''
            INSERT INTO rides (rideID, driverID, riderID, startDateTime, pickup, dropoff, rating) VALUES
            (1, 1, 8, '2024-11-01 14:00:00', 'The District at Tustin Legacy', 'Irvine Spectrum Center', 5),
            (2, 1, 9, '2024-11-02 10:30:00', 'South Coast Plaza', 'The Block at Orange', 4),
            (3, 2, 8, '2024-11-02 12:15:00', 'Huntington Beach Pier', 'Pacific City', 3),
            (4, 3, 9, '2024-11-03 09:00:00', 'John Wayne Airport', 'Laguna Beach', 2),
            (5, 4, 10, '2024-11-03 15:45:00', 'Angel Stadium', 'Honda Center', 5),
            (6, 5, 8, '2024-11-03 17:00:00', 'Disneyland Resort', 'Downtown Disney District', 4),
            (7, 2, 10, '2024-11-04 08:30:00', 'Knott’s Berry Farm', 'Buena Park Downtown', 1),
            (8, 4, 9, '2024-11-04 11:00:00', 'Tustin Marketplace', 'Old Town Orange', 5);
            '''
            self.cursor.execute(query)
        self.connection.commit()
        print("Tables populated")



    # destructor that closes connection with DB
    def destructor(self):
        self.cursor.close()
        self.connection.close()