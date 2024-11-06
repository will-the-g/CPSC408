#1.
SELECT rental_duration, (SELECT AVG(rental_duration)
			FROM film) AS avgFilmDuration
FROM film;
#2.
SELECT COUNT(*)
FROM (
SELECT category_id
FROM film_category
GROUP BY category_id
HAVING COUNT(film_id) > 60
) AS categories_with_over_60_films;

#3.
SELECT AVG(amount) AS average_payment_amount
FROM payment
WHERE customer_id IN (
	SELECT customer_id
	FROM customer
	WHERE address_id IN (
		SELECT address_id
		FROM address
		WHERE city_id IN (
			SELECT city_id
			FROM city
			WHERE country_id = (
				SELECT country_id
				FROM country
				WHERE country = 'Mexico'
			)
		)
	)
);

#4.
SELECT AVG(p.amount) AS average_payment
FROM payment AS p
JOIN customer AS c ON p.customer_id = c.customer_id
JOIN address AS a ON c.address_id = a.address_id
JOIN city AS ci ON a.city_id = ci.city_id
JOIN country AS co on ci.country_id = co.country_id
WHERE co.country = 'Mexico';

