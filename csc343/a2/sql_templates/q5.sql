-- Q5. Flight Hopping

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO air_travel, public;
DROP TABLE IF EXISTS q5 CASCADE;

CREATE TABLE q5 (
	destination CHAR(3),
	num_flights INT
);

-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS intermediate_step CASCADE;

DROP VIEW IF EXISTS start_day CASCADE;
CREATE VIEW start_day AS
SELECT day::date as day FROM q5_parameters;
-- can get the given date using: (SELECT day from day)

DROP VIEW IF EXISTS num_flights_table CASCADE;
CREATE VIEW num_flights_table AS
SELECT n FROM q5_parameters;
-- can get the given number of flights using: (SELECT n from n)

-- HINT: You can answer the question by writing one recursive query below, without any more views.
-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q5

with recursive flights_hopping as (
(select inbound, 1 as num_flights, s_arv from flight 
where outbound = 'YYZ'
and (s_dep - (select day from q5_parameters)) < '24:00:00' 
and (s_dep - (select day from q5_parameters)) >= '00:00:00')
union all
(select flight.inbound as inbound, num_flights + 1 
as num_flights, flight.s_arv 
from flights_hopping
	inner join flight 
	on flight.outbound = flights_hopping.inbound and
				(flight.s_dep - flights_hopping.s_arv) >= '00:00:00' 
				and
				(flight.s_dep - flights_hopping.s_arv) < '24:00:00' 
				and 
				num_flights < (select n from q5_parameters))
)

select inbound as destination, num_flights from flights_hopping;