-- #1
CREATE TABLE Patient(patientID INT NOT NULL PRIMARY KEY, name VARCHAR(20), dob VARCHAR(20), phone INT );

-- #2
ALTER TABLE Patient
ADD COLUMN address VARCHAR(30);

-- #3
DROP TABLE Patient;

-- #4
SELECT FirstName, LastName, Email
FROM employees;

-- #5
SELECT EmployeeId
FROM employees
WHERE HireDate > 2004;

-- #6
SELECT *
FROM employees
WHERE Title LIKE '%Manager%';

-- #7
SELECT DISTINCT BillingCity
FROM invoices;

-- #8
SELECT DISTINCT BillingCountry
FROM invoices
WHERE (invoices.Total > 10) AND (invoices.InvoiceDate LIKE '%2013%');

-- #9
SELECT DISTINCT State
FROM customers
WHERE State NOT NULL
EXCEPT
SELECT DISTINCT State
FROM employees;

-- #10
SELECT Phone
FROM customers
UNION
SELECT Phone
FROM employees;

-- #11
SELECT FirstName
FROM customers
INTERSECT
SELECT FirstName
from employees;

