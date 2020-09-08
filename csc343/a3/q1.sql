-- Q1. Site Prices

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO wet_world, public;
DROP TABLE IF EXISTS q1 CASCADE;

CREATE TABLE q1 (
    dive_type TEXT,
    num_sites INT
);

-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS open_dives CASCADE;
DROP VIEW IF EXISTS cave_dives CASCADE;
DROP VIEW IF EXISTS deep_dives CASCADE;

-- Define views for your intermediate steps here:
CREATE VIEW open_dives AS 
select 'open' as dive_type, count(distinct siteid) site_count
from monitoropendiveprice;

CREATE VIEW cave_dives AS 
select 'cave' as dive_type, count(distinct siteid) site_count
from monitorcavediveprice;

CREATE VIEW deep_dives AS 
select 'deep' as dive_type, count(distinct siteid) site_count
from monitordeepdiveprice;


-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q1
((select * from open_dives)
    union 
(select * from cave_dives) 
    union
(select * from deep_dives))
order by site_count, dive_type;


