-- Q3. Site Prices

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO wet_world, public;
DROP TABLE IF EXISTS q3 CASCADE;

CREATE TABLE q3 (
    site_id INT,
    avg_fee NUMERIC,
    capacity_level TEXT
);

-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS group_dive_count CASCADE;
DROP VIEW IF EXISTS solo_dive_count CASCADE;
DROP VIEW IF EXISTS combined_dive_count CASCADE;
DROP VIEW IF EXISTS avg_price_site CASCADE;

CREATE VIEW group_dive_count AS
select b.bookingid, count(distinct diverid) + 1 as num_divers 
from booking b
    inner join bookedbylead bbl
        on b.bookingid = bbl.bookingid
    inner join site s
        on b.siteid = s.id
group by b.bookingid;

CREATE VIEW solo_dive_count AS
select b.bookingid, 1 as num_divers
from booking b
where b.bookingid not in (select bookingid from group_dive_count);

CREATE VIEW combined_dive_count AS
(select * from group_dive_count)
    union
(select * from solo_dive_count);

CREATE VIEW avg_price_site AS
select s.id as siteid, sum(cdc.num_divers) as total_divers, avg(b.price) avg_price, s.daycapacity
from combined_dive_count cdc
    inner join booking b
        on cdc.bookingid = b.bookingid
    inner join site s
        on b.siteid = s.id
group by s.id;



-- Define views for your intermediate steps here:


-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q3
(select siteid, avg_price as avg_fee, 'lower or equal' as capacity_level 
from avg_price_site aps 
where aps.total_divers <= (aps.daycapacity / 2))
    union
(select siteid, avg_price as avg_fee, 'higher' as capacity_level
from avg_price_site aps 
where aps.total_divers > (aps.daycapacity / 2));

