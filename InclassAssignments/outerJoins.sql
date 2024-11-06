-- 1
SELECT address.address_id
FROM address
LEFT JOIN store
    ON address.address_id = store.address_id
WHERE address.district = 'California' AND store.address_id IS NULL;

-- 2
SELECT film.title, COUNT(store_id)
FROM film
LEFT JOIN inventory
    ON film.film_id = inventory.film_id
GROUP BY film.film_id;

-- 3
SELECT first_name, film.title
FROM actor
LEFT JOIN film_actor
    ON actor.actor_id = film_actor.actor_id
LEFT JOIN film
    ON film_actor.film_id = film.film_id;

-- 4
SELECT actor.actor_id, film_actor.film_id
FROM actor
LEFT JOIN film_actor
    ON actor.actor_id = film_actor.actor_id
RIGHT JOIN film
    ON film_actor.film_id = film.film_id;
