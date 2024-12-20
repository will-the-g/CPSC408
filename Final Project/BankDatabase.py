from db_ops import db_ops
from helper import helper
from datetime import datetime



class BankDatabase():
    def __init__(self):
        self.db_ops = db_ops(host = "localhost", user="root", password="CPSC408!", database="BankApp")
        self.db_ops.create_tables()
        self.userID = 0
        #db_ops.populate_tables()

    # checks to see if the given password matches the stored password
    def check_login(self, username, password):
        # checks if email exists
        query = 'SELECT * FROM users WHERE email = %s'
        if self.db_ops.single_record_params(query,(username,)) is None:
            return False
        
        query = 'SELECT hashedPassword FROM users WHERE email = %s'
        real_password = self.db_ops.single_record_params(query,(username,))
        if password == real_password:
            query = 'SELECT userID FROM users WHERE email = %s'
            self.userID = self.db_ops.single_record_params(query,(username,))
            return True
        else:
            return False
    
    def set_userID(self, userID):
        self.userID = userID
    
    def get_userID(self):
        return self.userID
    
    def get_name(self):
        query = f"SELECT fullName FROM users WHERE userID = {self.userID}"
        return self.db_ops.single_record(query)
        
    # gets the account type given userID 
    def get_account_type(self):
        query = f'SELECT userRole FROM users WHERE userID = {self.userID}'
        return self.db_ops.single_record(query)
    
    def get_amount(self, accountType):
        result = self.db_ops.single_row(f'SELECT * FROM accounts WHERE userID = {self.userID} AND accountType="{accountType}"')
        if result:
            return '$' + str(result[5])
        else:
            return "No account"

    # 1. Print/Display records from your database/tables: Displays all accounts
    
    def get_accounts(self):
        query = f'SELECT * FROM accounts WHERE userID = {self.userID}'
        result = self.db_ops.select_query(query)
        return result if result is not None else None
        
    def get_accounts_checkings_savings(self):
        query = f'SELECT accountNumber FROM accounts WHERE userID = {self.userID} AND (accountType = "Checkings" OR accountType = "Savings");'
        result = self.db_ops.select_query(query)
        return result if result is not None else None
    # gets all transactions from the account   
    def get_transactions(self, accountID):
        query = f'SELECT * FROM transactions WHERE accountID = {accountID} ORDER BY dateTime DESC;'
        result = self.db_ops.select_query(query)
        return result if result is not None else None

    # gets all statements from the user in descending order
    # 9. One query must contain a subquery
    # 2. QUery for data/results with various parameters/filters
    def get_statements(self, limit):
        query = f'''SELECT s.* , 
        (SELECT c.cardNumber
        FROM cards c
        WHERE c.cardID = s.cardID)
        FROM statements s 
        WHERE userID = {self.userID} 
        ORDER BY dueDate DESC 
        LIMIT {limit};'''
        result = self.db_ops.select_query(query)
        return result if result is not None else None
        
    # gets all Not Paid or Late statements from the user    
    def get_notPaid_statements(self):
        query = f'''SELECT *, 
        (SELECT c.cardNumber
        FROM cards c
        WHERE c.cardID = s.cardID) 
        FROM statements s
        WHERE userID = {self.userID} 
        AND (STATUS = "Not Paid" OR STATUS = "Late") 
        ORDER BY dueDate ASC;'''
        result = self.db_ops.select_query(query)
        return result if result is not None else None
    
    # 3, 5, and 6. Update and insert query wrapped in a transacton (commit + rollback defined in db_ops)
    def update_statement(self, statement, current, amount, accountNumber):
        queries = []
        if amount == 0:
            queries.append(f'''UPDATE statements
                    SET totalDue = {current-amount}, minimum = 0, STATUS = "Paid"
                    WHERE statementID = {statement[0]};''')
        else:
            queries.append(f'''UPDATE statements
                    SET totalDue = {current-amount}, minimum = 0
                    WHERE statementID = {statement[0]};''')
            
        queries.append(f'''INSERT INTO transactions (accountID, cardID, type, amount, dateTime, status, recipientName, description, location)
                VALUES ({statement[2]},{statement[3]}, "Card Payment", {amount}, NOW(), "Completed", "Bank", "Card Payment", "Online");
                    ''')

        queries.append(f''' UPDATE accounts
                SET balance = balance - {amount}
                WHERE accountID = {statement[2]};
                ''')
        self.db_ops.run_transaction(queries)

    # 4. Delete query
    def delete_curr_account(self, accountID):
        query = f'SELECT balance FROM accounts WHERE accountID = {accountID}'
        balance = self.db_ops.single_record(query)
        print(balance)
        if balance == 0.0:
            query = f'DELETE FROM accounts WHERE accountID = {accountID}'
            self.db_ops.modify_query(query)
            print('Account Deleted')
            return True
        else:
            return False
        
    # 8. One query must perform an aggregation/group by clause    
    def total_money_owed(self):
        query = f'SELECT SUM(totalDue) FROM statements WHERE userID = {self.userID} AND (STATUS = "Not Paid" OR STATUS = "Late");'
        result = self.db_ops.single_record(query)
        return result if result is not None else None
    
    # 10. 1st query with joins Across 3 Tables 
    def get_transaction_history(self):
        query = f'''SELECT 
            users.userID,
            users.fullName,
            users.email,
            accounts.accountNumber,
            accounts.accountType,
            cards.cardNumber,
            cards.cardType,
            transactions.transactionID,
            transactions.type AS transactionType,
            transactions.amount,
            transactions.dateTime AS transactionDate,
            transactions.status AS transactionStatus
        FROM 
            users
        JOIN 
            accounts ON users.userID = accounts.userID
        JOIN 
            cards ON users.userID = cards.userID
        JOIN 
            transactions ON cards.cardID = transactions.cardID AND accounts.accountID = transactions.accountID
        WHERE 
            users.userID = {self.userID};
        '''
        result = self.db_ops.select_query(query)
        return result if result is not None else None
    
    # 10. 2nd query with joins Across 3 Tables 
    def get_statement_history(self):
        query = f'''SELECT 
            users.userID,
            users.fullName,
            accounts.accountNumber,
            accounts.accountType,
            cards.cardNumber,
            cards.cardType,
            SUM(transactions.amount) AS totalSpent,
            statements.totalDue,
            statements.dueDATE,
            statements.STATUS AS statementStatus
        FROM 
            users
        JOIN 
            accounts ON users.userID = accounts.userID
        JOIN 
            cards ON users.userID = cards.userID
        JOIN 
            transactions ON cards.cardID = transactions.cardID AND accounts.accountID = transactions.accountID
        JOIN 
            statements ON accounts.accountID = statements.accountID
        WHERE 
            users.userID = {self.userID} 
            AND transactions.dateTime BETWEEN statements.periodStart AND statements.periodEnd
        GROUP BY 
            users.userID, accounts.accountID, cards.cardID, statements.statementID;
            '''
        result = self.db_ops.select_query(query)
        return result if result is not None else None
    
    # 12. Database view
    def create_account_view(self):
        query = '''
            CREATE VIEW user_account_overview AS
            SELECT 
                users.userID,
                users.fullName,
                users.email,
                accounts.accountNumber,
                accounts.accountType,
                accounts.balance,
                accounts.dateOpened,
                accounts.interestRate,
                accounts.minimumBalance,
                accounts.overDraftLimit
            FROM 
                users
            JOIN 
                accounts ON users.userID = accounts.userID;
        '''
        self.db_ops.modify_query(query)
        return

    def view_account(self):
        query = f'SELECT * FROM user_account_overview WHERE userID = {self.userID}'
        result = self.db_ops.select_query(query)
        print(result)
        return