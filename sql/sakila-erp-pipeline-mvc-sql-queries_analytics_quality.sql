 USE sakila;
 
 -- Preguntas Sobre Base de Datos Sakila
 
 -- 1-) Todas las Peliculas
 
 SELECT 
	film_id, 
    title, 
    release_year, 
    rental_rate
FROM film;

-- 2-) Peliculas por Categoria

SELECT 
	c.name AS "Categoria", 
	COUNT(f.film_id) AS "Total"
FROM sakila.film f
JOIN sakila.film_category fc ON f.film_id = fc.film_id
JOIN sakila.category c ON fc.category_id = c.category_id
GROUP BY c.name
ORDER BY Total DESC;

-- 3-) Renta por Cliente (TOP 10)

SELECT 
	CONCAT(c.first_name,' ',c.last_name) AS "Cliente",
	COUNT(r.rental_id) AS "Rentas"
FROM sakila.customer c
JOIN sakila.rental r ON c.customer_id = r.customer_id
GROUP BY c.customer_id
ORDER BY Rentas DESC
LIMIT 10;

-- 4-) Actores mas Frecuentes (TOP 10)

SELECT 
	CONCAT(a.first_name,' ',a.last_name) AS "Actor",
	COUNT(fa.film_id) AS "Peliculas"
FROM sakila.actor a
JOIN sakila.film_actor fa ON a.actor_id = fa.actor_id
GROUP BY a.actor_id
ORDER BY Peliculas DESC
LIMIT 10;

-- 5-) Ingresos por Tienda

SELECT 
	s.store_id,
	SUM(p.amount) AS "Ingresos Totales"
FROM sakila.payment p
JOIN sakila.staff st ON p.staff_id = st.staff_id
JOIN sakila.store s ON st.store_id = s.store_id
GROUP BY s.store_id;

-- 6-) Cuales es la Rotacion del Inventario 

SELECT 
    f.film_id AS 'ID Artículo',
    f.title AS 'Descripción del Producto',
    
    -- NUMERADOR: Total de despachos / salidas logísticas en el histórico
    COUNT(r.rental_id) AS 'Total Despachos (Rentas)',
    
    -- DENOMINADOR: Stock total de copias asignadas en inventario
    COUNT(DISTINCT i.inventory_id) AS 'Inventario Disponible (Unidades)',
    
    -- CÁLCULO DEL ÍNDICE DE ROTACIÓN (Flujo Total / Stock)
    -- Usamos ROUND y NULLIF para evitar divisiones entre cero si un artículo no tiene stock
    ROUND(
        COUNT(r.rental_id) / NULLIF(COUNT(DISTINCT i.inventory_id), 0), 
        2
    ) AS 'Índice Rotación Inventario (IRI)',
    
    
    -- DIAGNÓSTICO LOGÍSTICO (Análisis de Criticidad de Almacén)
    CASE 
        WHEN COUNT(r.rental_id) = 0 THEN 'MERMA / STOCK CRÍTICO INACTIVO'
        WHEN (COUNT(r.rental_id) / COUNT(DISTINCT i.inventory_id)) > 5 THEN 'ALTA ROTACIÓN (Fast Moving)'
        WHEN (COUNT(r.rental_id) / COUNT(DISTINCT i.inventory_id)) BETWEEN 2 AND 5 THEN 'ROTACIÓN ESTÁNDAR'
        ELSE 'BAJA ROTACIÓN (Slow Moving / Capital Atrapado)'
    END AS 'Estatus Operativo'
    FROM film f
-- LEFT JOIN para no dejar fuera los artículos con CERO rentas (mermas u obsolescencia)
LEFT JOIN inventory i ON f.film_id = i.film_id
LEFT JOIN rental r ON i.inventory_id = r.inventory_id

GROUP BY f.film_id, f.title
ORDER BY f.film_id ASC;

-- 7-) Cuantos Dias Promedio pasan las peliculas en inventario antes de ser rentadas

SELECT 
    f.film_id AS 'ID Artículo',
    f.title AS 'Descripción del Producto',
    
      
    -- Días promedio que pasa el activo en estante antes de rotar
    ROUND(
        365 / NULLIF((COUNT(r.rental_id) / NULLIF(COUNT(DISTINCT i.inventory_id), 0)), 0), 
        1
    ) AS 'Días de Cobertura (DSI)'
    
FROM film f
-- LEFT JOIN para no dejar fuera los artículos con CERO rentas (mermas u obsolescencia)
LEFT JOIN inventory i ON f.film_id = i.film_id
LEFT JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY f.film_id, f.title
ORDER BY f.film_id ASC;

-- 8-) Cuantos Dias Promedio y su Desviacion Estandar pasan las peliculas rentadas (Fuera de la Tienda)

SELECT 
    i.inventory_id AS 'ID Copia Artículo',
    f.title AS 'Descripción del SKU',
    COUNT(r.rental_id) AS 'Total de Despachos en el Histórico',
    -- Calculamos el TIEMPO PROMEDIO de ciclo que esa unidad pasa fuera de la tienda
    ROUND(AVG(TIMESTAMPDIFF(DAY, r.rental_date, r.return_date)), 2) AS 'Tiempo Promedio Fuera de Tienda (Dias)',
    -- Calculamos la Desviacion Estandar del tiempo de fuera de tienda
    ROUND(STDDEV_SAMP(TIMESTAMPDIFF(DAY, r.rental_date, r.return_date)),2) AS "Desviacion Estandar (Dias)",
    -- Calculamos el Coeficiente de Variacion
    ROUND(STDDEV_SAMP(TIMESTAMPDIFF(DAY, r.rental_date, r.return_date))/(AVG(TIMESTAMPDIFF(DAY, r.rental_date, r.return_date))),2)*100 AS "Coeficiente de Variacion (S/X)*100"
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
WHERE r.return_date IS NOT NULL
GROUP BY i.inventory_id, f.title
ORDER BY `Tiempo Promedio Fuera de Tienda (Dias)` DESC;

-- 9-) Cuales peliculas nunca han sido rentadas (Obsolencias)

SELECT 
    i.inventory_id AS 'ID Copia Artículo',
    f.title AS 'Descripción del SKU',
    0 AS 'Total de Despachos en el Histórico'
FROM inventory i
JOIN film f ON i.film_id = f.film_id
-- Buscamos las unidades que jamás han registrado una salida en la tabla transaccional
WHERE i.inventory_id NOT IN (
    SELECT DISTINCT rental.inventory_id 
    FROM rental
)
ORDER BY i.inventory_id;

-- 10-) Disponibilidad de Peliculas por Tienda (Disponibilidad de Activos)

SELECT 
	s.store_id AS "ID Tienda",
    f.title AS 'Descripción del SKU',
    COUNT(i.inventory_id) as "Inventario de Peliculas"
FROM inventory i
JOIN film f on i.film_id = f.film_id
JOIN store s on i.store_id = s.store_id
GROUP BY s.store_id, f.film_id, f.title
ORDER BY s.store_id ASC, `Inventario de Peliculas` DESC;

-- Vamos a conocer las restriccion actuales
SELECT 
    constraint_schema AS 'Base de Datos',
    table_name AS 'Tabla',
    constraint_name AS 'Nombre de la Restricción',
    constraint_type AS 'Tipo de Restricción'
FROM information_schema.table_constraints
WHERE constraint_schema = 'sakila' -- Filtra solo tu base de datos activa
ORDER BY table_name ASC, constraint_type DESC;


-- "Al auditar el esquema original de Sakila, detectamos que carece de validaciones lógicas de negocio, 
-- permitiendo registrar costos negativos o devoluciones en el pasado".

-- Restricciones de Costes y Ratios Menores que 0
ALTER TABLE film 
ADD CONSTRAINT chk_film_rental_rate CHECK (rental_rate > 0.00),
ADD CONSTRAINT chk_film_replacement_cost CHECK (replacement_cost > 0.00);

-- Restricciones de duracion de la Pelicula y de Renta, evitando sean Menores que 0
ALTER TABLE film 
ADD CONSTRAINT chk_film_length CHECK (length > 0),
ADD CONSTRAINT chk_film_rental_duration CHECK (rental_duration > 0);

-- Restriccion de valores de transacciones facturadas, evitnado sean Menores que 0
ALTER TABLE payment 
ADD CONSTRAINT chk_payment_amount CHECK (amount >= 0.00);

-- Restriccion para consistencia temporal
ALTER TABLE rental 
ADD CONSTRAINT chk_rental_dates CHECK (return_date >= rental_date);

-- SCRIPTS para prueba del funcionamiento de las restricciones

-- Debe fallar por violación de chk_film_rental_rate
INSERT INTO film (title, language_id, rental_duration, rental_rate, replacement_cost) 
VALUES ('RESTRICCION TEST 1', 1, 3, -1.99, 20.00);

-- Debe fallar por violación de chk_film_replacement_cost
INSERT INTO film (title, language_id, rental_duration, rental_rate, replacement_cost) 
VALUES ('RESTRICCION TEST 2', 1, 3, 2.99, 0.00);

-- Debe fallar por violación de chk_film_length
INSERT INTO film (title, language_id, rental_duration, rental_rate, replacement_cost, length) 
VALUES ('RESTRICCION TEST 3', 1, 5, 2.99, 19.99, -120);

-- Debe fallar por violación de chk_film_rental_duration
INSERT INTO film (title, language_id, rental_duration, rental_rate, replacement_cost) 
VALUES ('RESTRICCION TEST 4', 1, -5, 2.99, 19.99);

-- Debe fallar por violación de chk_film_length y proteger inventario actual
UPDATE film 
SET length = 0 
WHERE film_id = 1;

-- Debe fallar por violación de chk_payment_amount
INSERT INTO payment (customer_id, staff_id, rental_id, amount, payment_date)
VALUES (1, 1, 1, -50.00, NOW());

-- Debe fallar y mantener la integridad contable intacta
UPDATE payment 
SET amount = -0.01 
WHERE payment_id = 1;

-- Debe fallar por violación de chk_rental_dates
INSERT INTO rental (rental_date, inventory_id, customer_id, return_date, staff_id)
VALUES ('2026-05-29 12:00:00', 1, 1, '2026-05-28 12:00:00', 1);

-- Debe fallar inmediatamente impidiendo la alteración de la línea de tiempo del proceso
UPDATE rental 
SET return_date = '2005-01-01 00:00:00' 
WHERE rental_id = 1;

-- Debe ejecutarse PERFECTAMENTE sin errores, demostrando que el sistema solo frena el dato defectuoso
INSERT INTO film (title, language_id, rental_duration, rental_rate, replacement_cost, length) 
VALUES ('PROCESO CONTROLADO OK', 1, 5, 4.99, 15.00, 95);








   
    
    
    



