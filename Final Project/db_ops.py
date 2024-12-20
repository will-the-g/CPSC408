import mysql.connector

class db_ops():
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


    def modify_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    # starts a transaction. Takes in a list of queries
    def run_transaction(self, queries):
        try:
            self.cursor.execute('START TRANSACTION')

            for query in queries:
                self.cursor.execute(query)

            self.cursor.execute("COMMIT")
        except Exception as e:
            self.cursor.execute('ROLLBACK')
            raise
            

    def modify_query_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        self.connection.commit()

    def select_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def select_query_params(self, query, dictionary):
        result = self.cursor.execute(query, dictionary)
        return result.fetchall()
    
    def single_row(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def single_record(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    def single_record_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        return self.cursor.fetchone()[0]
    
    # 13. Use at least 5 entities
    def create_tables(self):
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            userID INTEGER AUTO_INCREMENT PRIMARY KEY NOT NULL,
            fullName VARCHAR(30) NOT NULL,
            dateOfBirth DATE NOT NULL,
            email VARCHAR(30) NOT NULL,
            phoneNumber VARCHAR(15),
            address TEXT NOT NULL,
            hashedPassword VARCHAR(20) NOT NULL,
            userRole VARCHAR(10) NOT NULL DEFAULT 'Customer' COMMENT 'Customer, Joint, Employee, Admin, Supervisor, Audit',
            employmentStatus VARCHAR(15) COMMENT 'Employed, Unemployed, Self Employed, Contract, Intern, Volunteer, Temporary',
            income INTEGER,
            securityQuestion text
        );
        '''
        self.cursor.execute(query)
        query = '''
        CREATE TABLE IF NOT EXISTS accounts(
            accountID INTEGER AUTO_INCREMENT PRIMARY KEY NOT NULL,
            userID INTEGER NOT NULL,
            accountNumber INTEGER NOT NULL UNIQUE,
            accountType VARCHAR(10) NOT NULL COMMENT 'Checkings, Savings, MMA, CD, IRA, Joint, Student, Business',
            dateOpened DATE,
            balance DECIMAL(10,2),
            interestRate DECIMAL(7,5),
            minimumBalance DECIMAL(7,2),
            overDraftLimit FLOAT,
            monthlyFees FLOAT,
            FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE
        );
        '''
        self.cursor.execute(query)
        query = '''
        CREATE TABLE IF NOT EXISTS cards(
            cardID INTEGER AUTO_INCREMENT PRIMARY KEY NOT NULL,
            userID INTEGER NOT NULL,
            accountID INTEGER NOT NULL,
            cardNumber INTEGER NOT NULL,
            cardType VARCHAR(10) NOT NULL,
            cardNetwrok VARCHAR(20) NOT NULL,
            nameOnCard VARCHAR(30) NOT NULL,
            expDate VARCHAR(10) NOT NULL,
            CVV INTEGER NOT NULL,
            billingAddress VARCHAR(30),
            creditLimit FLOAT,
            pin INTEGER,
            FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE,
            FOREIGN KEY (accountID) REFERENCES accounts(accountID) ON DELETE CASCADE
        );
        '''
        self.cursor.execute(query)
        query = '''
        CREATE TABLE IF NOT EXISTS transactions(
            transactionID INTEGER AUTO_INCREMENT PRIMARY KEY NOT NULL,
            accountID INTEGER NOT NULL,
            cardID INTEGER NOT NULL,
            type VARCHAR(15) NOT NULL,
            amount FLOAT NOT NULL,
            dateTime DATETIME,
            status VARCHAR(10) NOT NULL DEFAULT 'Pending' COMMENT 'Pending, Complete, Failed, On Hold',
            recipientName VARCHAR(30) NOT NULL,
            description TEXT,
            location text,
            FOREIGN KEY (accountID) REFERENCES accounts(accountID),
            FOREIGN KEY (cardID) REFERENCES cards(cardID)
        );
        '''
        self.cursor.execute(query)
        query = '''
        CREATE TABLE IF NOT EXISTS statements(
        statementID INTEGER AUTO_INCREMENT PRIMARY KEY NOT NULL,
        userID INTEGER NOT NULL,
        accountID INTEGER NOT NULL,
        cardID INTEGER NOT NULL,
        periodStart DATETIME,
        periodEnd DATETIME,
        issueDate DATETIME,
        dueDATE DATETIME,
        totalDue FLOAT NOT NULL DEFAULT 0.0,
        interestCharged FLOAT DEFAULT 0.0,
        minimum FLOAT DEFAULT 0.0,
        STATUS VARCHAR(10) DEFAULT 'Not Paid' COMMENT 'Not Paid, Late, Paid'
        );
        '''