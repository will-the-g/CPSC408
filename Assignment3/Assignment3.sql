-- #1
SELECT tracks.Composer, ROUND(AVG(tracks.Milliseconds),1) as Average
from tracks
GROUP BY tracks.Composer;

-- #2
SELECT COUNT(DISTINCT invoices.CustomerId) as TotalNumberOfCustomers
FROM invoices;

-- #3
SELECT tracks.TrackId, tracks.GenreId, COUNT(tracks.TrackId), MAX(tracks.UnitPrice)
FROM tracks
GROUP BY MediaTypeId, GenreId;

-- #4
SELECT genres.Name, ROUND(AVG(tracks.Milliseconds),1) as AverageTrackLength
FROM tracks
INNER JOIN genres
    ON tracks.GenreId = genres.GenreId
GROUP BY genres.Name;

-- #5
SELECT artists.Name, COUNT(albumId) as TotalAlbums
FROM albums
INNER JOIN artists
    ON artists.ArtistId = albums.ArtistId
GROUP BY artists.Name;

-- #6
SELECT invoices.BillingCity, COUNT(invoiceId)
FROM invoices
WHERE invoices.BillingCountry = 'USA'
GROUP BY BillingCity;

-- Set 2
-- #1
SELECT Composer, ROUND(AVG(tracks.Milliseconds), 1) as AvgTrackLength
FROM tracks
WHERE tracks.Milliseconds < 375000
GROUP BY Composer;

-- #2
SELECT Composer, ROUND(AVG(tracks.Milliseconds), 1) as AvgTrackLength
FROM tracks
GROUP BY composer
HAVING AvgTrackLength < 375000;

-- #3
SELECT BillingCountry, COUNT(invoiceId) as NumRecords
FROM invoices
GROUP BY BillingCountry
HAVING numRecords < 10;

-- #4
SELECT BillingCountry, COUNT(DISTINCT BillingCity) as NumCities
FROM invoices
GROUP BY BillingCountry
HAVING NumCities = 8;

-- #5
SELECT invoices.BillingCountry, SUM(invoices.Total)
FROM invoices
WHERE invoices.InvoiceDate LIKE '%2010%'
GROUP BY BillingCountry
HAVING COUNT(*) > 5;




