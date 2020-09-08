-- Q4. Site Prices

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO wet_world, public;
DROP TABLE IF EXISTS q4 CASCADE;

CREATE TABLE q4 (
    site_id INT,
    max_price INT,
    min_price INT,
    avg_price INT
);

-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS intermediate_step CASCADE;


-- Define views for your intermediate steps here:


-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q4
select s.id, max(b.price), min(b.price), avg(b.price) 
from site s inner join booking b
on s.id = b.siteid
group by s.id;
