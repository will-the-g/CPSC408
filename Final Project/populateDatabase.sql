CREATE TABLE IF NOT EXISTS users (
            userID INTEGER AUTO_INCREMENT PRIMARY KEY NOT NULL,
            fullName VARCHAR(30) NOT NULL,
            dateOfBirth DATE NOT NULL,
            email VARCHAR(30) NOT NULL,
            phoneNumber VARCHAR(15),
            address TEXT NOT NULL,
            hashedPassword VARCHAR(20) NOT NULL,
            userRole VARCHAR(10) NOT NULL DEFAULT 'Customer' COMMENT 'Customer, Joint, Employee, Admin, Supervisor, Audit',
            employmentStatus VARCHAR(10),
            income INTEGER,
            securityQuestion text
        );


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

CREATE TABLE IF NOT EXISTS cards(
            cardID INTEGER AUTO_INCREMENT PRIMARY KEY NOT NULL,
            userID INTEGER NOT NULL,
            accountID INTEGER NOT NULL,
            cardNumber INTEGER NOT NULL,
            cardType VARCHAR(10) NOT NULL,
            cardNetwork VARCHAR(20) NOT NULL,
            nameOnCard VARCHAR(30) NOT NULL,
            expDate VARCHAR(10) NOT NULL,
            CVV INTEGER NOT NULL,
            billingAddress VARCHAR(30),
            creditLimit FLOAT,
            pin INTEGER,
            FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE,
            FOREIGN KEY (accountID) REFERENCES accounts(accountID) ON DELETE CASCADE
        );



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
            FOREIGN KEY (accountID) REFERENCES accounts(accountID) ON DELETE SET NULL,
            FOREIGN KEY (cardID) REFERENCES cards(cardID)
        );



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


INSERT INTO users (fullName, dateOfBirth, email, phoneNumber, address, hashedPassword,
    userRole, employmentStatus, income, securityQuestion
) VALUES
      ('John Doe', '1985-07-20', 'johndoe@example.com', '(312) 555-1234', '123 Main St, Springfield, IL', 'hashedpassword1',
    'Customer', 'Employed', 45000, 'What is your pet\'s name? | tango'),

      ('Jane Smith', '1990-03-15', 'janesmith@example.com', '(415) 555-5678', '456 Oak St, Springfield, IL', 'hashedpassword2',
    'Admin', 'Employed', 80000, 'What was the name of your first school? | Chapman Elementary'),

    ('Alice Johnson', '1992-12-05', 'alicej@example.com', '(646) 555-9876', '789 Pine St, Springfield, IL', 'hashedpassword3',
    'Employee', 'Unemployed', 55000, 'What is your favorite color? | purple'),

    ('Bob Brown', '1988-08-22', 'bobbrown@example.com', '(718) 555-1357', '101 Maple St, Springfield, IL', 'hashedpassword4',
    'Customer', 'Employed', 39000, 'What is your mother\'s maiden name? | john'),

    ('Eve Davis', '1980-11-30', 'evedavis@example.com', '(213) 555-2468', '202 Birch St, Springfield, IL', 'hashedpassword5',
    'Supervisor', 'Employed', 95000, 'Where were you born? | San Diego'),

    ('Charlie Clark', '2000-01-10', 'charlieclark@example.com', '(312) 555-8642', '303 Cedar St, Springfield, IL', 'hashedpassword6',
    'Customer', 'Unemployed', 20000, 'What is your favorite hobby? | doomscrolling'),

    ('David Wilson', '1995-05-17', 'davidwilson@example.com', '(617) 555-3579', '404 Elm St, Springfield, IL', 'hashedpassword7',
    'Customer', 'Employed', 46000, 'What was your first car? | Honda Accord'),

    ('Grace Lewis', '1983-09-25', 'gracelewis@example.com', '(305) 555-7531', '505 Ash St, Springfield, IL', 'hashedpassword8',
    'Employee', 'Employed', 70000, 'What is your father\'s middle name? | John'),

    ('Frank Harris', '1997-06-12', 'frankharris@example.com', '(202) 555-1592', '606 Redwood St, Springfield, IL', 'hashedpassword9',
    'Admin', 'Employed', 95000, 'What is your favorite movie? | Interstellar'),

    ('Hannah Young', '1993-04-14', 'hannahyoung@example.com', '(718) 555-4863', '707 Fir St, Springfield, IL', 'hashedpassword10',
    'Customer', 'Employed', 42000, 'What is the name of your best friend? | John');

SELECT *
FROM users;

UPDATE users
SET email = 1, users.hashedPassword = 1
WHERE userID = 1;

INSERT INTO accounts (userID, accountNumber, accountType, dateOpened, balance, interestRate, minimumBalance, overDraftLimit, monthlyFees)
VALUES
(1, 1000001, 'Checkings', '2022-01-15', 1500.00, 0.00250, 500.00, 100.00, 10.00),
(2, 1000002, 'Savings', '2021-06-10', 3000.00, 0.01000, 1000.00, NULL, 5.00),
(3, 1000003, 'MMA', '2023-03-01', 7500.00, 0.01200, 2500.00, NULL, 15.00),
(4, 1000004, 'CD', '2020-11-20', 10000.00, 0.03000, NULL, NULL, 0.00),
(5, 1000005, 'IRA', '2019-08-30', 20000.00, 0.02000, NULL, NULL, 0.00),
(6, 1000006, 'Joint', '2022-09-05', 5000.00, 0.00300, 1000.00, 500.00, 12.00),
(7, 1000007, 'Student', '2023-07-14', 1200.00, 0.00050, 100.00, 50.00, 1.00),
(8, 1000008, 'Business', '2021-12-12', 15000.00, 0.00800, 5000.00, 1000.00, 25.00),
(9, 1000009, 'Savings', '2023-02-01', 2500.00, 0.01000, 500.00, NULL, 3.00),
(10, 1000010, 'Checkings', '2020-10-10', 800.00, 0.00150, 200.00, 200.00, 8.00);

SELECT *
FROM accounts;

INSERT INTO accounts (userID, accountNumber, accountType, dateOpened, balance, interestRate, minimumBalance, overDraftLimit, monthlyFees)
VALUES
(1, 1234567890, 'Checking', '2023-01-01', 0.00, 0.0035, 100.00, 500.00, 12.99),
(1, 1234567891, 'Savings', '2023-02-15', 100000.00, 0.0050, 500.00, 0.00, 5.99),
(1, 1234567892, 'MMA', '2023-03-20', 0.00, 0.0075, 1000.00, 1000.00, 19.99),
(1, 1234567893, 'CD', '2023-04-10', 0.00, 0.0250, 500.00, 0.00, 0.00),
(1, 1234567894, 'IRA', '2023-05-05', 0.00, 0.0040, 2000.00, 0.00, 15.00),
(1, 1234567895, 'Joint', '2023-06-15', 0.00, 0.0025, 100.00, 500.00, 10.99);


INSERT INTO accounts (userID, accountNumber, accountType, dateOpened, balance, interestRate, minimumBalance, overDraftLimit, monthlyFees)
VALUES
(1, 1234567893, 'CD', '2023-04-10', 0.00, 0.0250, 500.00, 0.00, 0.00),
(1, 1234567894, 'IRA', '2023-05-05', 0.00, 0.0040, 2000.00, 0.00, 15.00);

SELECT *
FROM accounts
WHERE userID = 1;




ALTER TABLE cards
MODIFY cardNumber VARCHAR(16) NOT NULL;

INSERT INTO cards (userID, accountID, cardNumber, cardType, cardNetwork, nameOnCard, expDate, CVV, billingAddress, creditLimit, pin)
VALUES
(1, 1, '4000123412341234', 'Credit', 'Visa', 'John Doe', '12/26', 123, '123 Elm St', NULL, 1234),
(2, 2, '4000567812345678', 'Credit', 'Mastercard', 'Jane Smith', '11/25', 456, '456 Oak St', 5000.00, 2345),
(3, 3, '4000987612349876', 'Credit', 'Amex', 'Alice Johnson', '01/28', 789, '789 Pine St', 10000.00, 3456),
(4, 4, '4000112211221122', 'Debit', 'Discover', 'Bob Brown', '03/27', 321, '321 Maple St', NULL, 4567),
(5, 5, '4000778877887788', 'Credit', 'Visa', 'Charlie Davis', '07/29', 654, '654 Cedar St', 15000.00, 5678),
(6, 6, '4000334433443344', 'Debit', 'Mastercard', 'Diana White', '09/26', 987, '987 Birch St', NULL, 6789),
(7, 7, '4000445544554455', 'Credit', 'Amex', 'Emily Black', '02/30', 213, '213 Aspen St', 20000.00, 7890),
(8, 8, '4000223322332233', 'Credit', 'Visa', 'Frank Green', '06/25', 876, '876 Spruce St', 7500.00, 8901),
(9, 9, '4000889988998899', 'Debit', 'Discover', 'Grace Kelly', '10/27', 432, '432 Willow St', NULL, 9012),
(10, 10, '4000667766776677', 'Credit', 'Mastercard', 'Henry Adams', '04/28', 543, '543 Palm St', 25000.00, 1230);

SELECT *
FROM cards;

UPDATE cards
SET cardType = 'Credit'
WHERE userID = 1;

INSERT INTO transactions (accountID, cardID, type, amount, dateTime, status, recipientName, description, location)
VALUES
(1, 1, 'Purchase', 150.75, '2024-11-01 14:30:00', 'Complete', 'Amazon', 'Online shopping for electronics', 'Seattle, WA'),
(2, 2, 'Withdrawal', 500.00, '2024-11-03 10:15:00', 'Complete', 'ATM Withdrawal', 'Cash withdrawal from ATM', 'Los Angeles, CA'),
(3, 3, 'Payment', 300.50, '2024-11-05 16:45:00', 'Pending', 'John Doe', 'Transfer to friend for dinner', 'New York, NY'),
(4, 4, 'Deposit', 1000.00, '2024-11-06 09:20:00', 'Complete', 'Company ABC', 'Salary deposit', 'San Francisco, CA'),
(5, 5, 'Purchase', 75.25, '2024-11-07 13:00:00', 'Failed', 'Walmart', 'Groceries purchase', 'Austin, TX'),
(6, 6, 'Payment', 200.00, '2024-11-08 18:10:00', 'Complete', 'Jane Smith', 'Payment for freelance work', 'Chicago, IL'),
(7, 7, 'Transfer', 600.00, '2024-11-09 15:00:00', 'On Hold', 'Savings Account', 'Transfer to savings', 'Houston, TX'),
(8, 8, 'Purchase', 250.00, '2024-11-10 17:25:00', 'Complete', 'Target', 'Shopping for household items', 'Miami, FL'),
(9, 9, 'Withdrawal', 100.00, '2024-11-11 20:00:00', 'Complete', 'ATM Withdrawal', 'Cash withdrawal', 'Phoenix, AZ'),
(10, 10, 'Payment', 1200.00, '2024-11-12 11:30:00', 'Pending', 'Henry Adams', 'Payment for rent', 'Dallas, TX');

SELECT *
FROM transactions;


INSERT INTO statements (userID, accountID, cardID, periodStart, periodEnd, issueDate, dueDATE, totalDue, interestCharged, minimum, STATUS)
VALUES
(1, 1, 1, '2024-08-01 00:00:00', '2024-08-31 23:59:59', '2024-09-01 10:00:00', '2024-09-15 23:59:59', 250.50, 5.00, 25.00, 'Not Paid'),
(2, 2, 2, '2024-07-01 00:00:00', '2024-07-31 23:59:59', '2024-08-01 12:00:00', '2024-08-15 23:59:59', 300.00, 8.00, 30.00, 'Paid'),
(3, 3, 3, '2024-06-01 00:00:00', '2024-06-30 23:59:59', '2024-07-01 09:00:00', '2024-07-15 23:59:59', 150.75, 3.00, 15.00, 'Late'),
(4, 4, 4, '2024-05-01 00:00:00', '2024-05-31 23:59:59', '2024-06-01 08:00:00', '2024-06-10 23:59:59', 120.00, 2.50, 12.00, 'Paid'),
(5, 5, 5, '2024-04-01 00:00:00', '2024-04-30 23:59:59', '2024-05-01 11:00:00', '2024-05-10 23:59:59', 500.00, 10.00, 50.00, 'Not Paid'),
(6, 6, 6, '2024-03-01 00:00:00', '2024-03-31 23:59:59', '2024-04-01 15:00:00', '2024-04-15 23:59:59', 350.25, 7.50, 35.00, 'Paid'),
(7, 7, 7, '2024-02-01 00:00:00', '2024-02-29 23:59:59', '2024-03-01 10:30:00', '2024-03-10 23:59:59', 220.80, 4.00, 22.00, 'Not Paid'),
(8, 8, 8, '2024-01-01 00:00:00', '2024-01-31 23:59:59', '2024-02-01 13:00:00', '2024-02-15 23:59:59', 100.50, 1.50, 10.00, 'Paid'),
(9, 9, 9, '2024-12-01 00:00:00', '2024-12-31 23:59:59', '2025-01-01 14:00:00', '2025-01-15 23:59:59', 400.00, 6.50, 40.00, 'Late'),
(10, 10, 10, '2024-11-01 00:00:00', '2024-11-30 23:59:59', '2024-12-01 12:00:00', '2024-12-15 23:59:59', 600.00, 9.00, 60.00, 'Not Paid');

SELECT *
from statements;