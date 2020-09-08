-- Q2. Simps

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO wet_world, public;
DROP TABLE IF EXISTS q2 CASCADE;

CREATE TABLE q2 (
    monitor_id INT,
    avg_fee NUMERIC,
    email TEXT
);

-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS avg_site_rating CASCADE;
DROP VIEW IF EXISTS avg_monitor_rating CASCADE;
DROP VIEW IF EXISTS simp CASCADE;
DROP VIEW IF EXISTS combined_price CASCADE;
DROP VIEW IF EXISTS avg_monitor_price CASCADE;

-- Define views for your intermediate steps here:

-- All avg site ratings
CREATE VIEW avg_site_rating as 
select b.siteid, avg(r.rating) from
((select * from leaddiversiterating)
union
(select * from nonleaddiversiterating)) r
inner join booking b
on r.bookingid = b.bookingid
group by siteid;

-- All avg monitor ratings
CREATE VIEW avg_monitor_rating as
select avg(rating), monitorid 
from monitorrating mr
inner join
booking b
on mr.bookingid = b.bookingid
group by monitorid;

-- Gets all monitors with a lower rating than site for all sites
CREATE VIEW simp as
select distinct(res1.monitorid), res1.siteid, res1.avg avg_site_rating, amr.avg avg_monitor_rating from
(select monitorid, asr.siteid, avg from
    monitoropendiveprice modp 
    inner join avg_site_rating asr 
    on modp.siteid = asr.siteid) res1
inner join avg_monitor_rating amr
on res1.monitorid = amr.monitorid
where res1.avg > amr.avg;

-- Gets combined pricing for all monitors
CREATE VIEW combined_price as
(select monitorid, morningprice, afternoonprice, nightprice from monitorcavediveprice
    union 
select monitorid, morningprice, afternoonprice, nightprice from monitoropendiveprice
    union 
select monitorid, morningprice, afternoonprice, nightprice from monitordeepdiveprice);

-- Gets avg prices for every monitor
CREATE VIEW avg_monitor_price as
select monitorid, avg(price_sum) avg_booking_fee
from (select monitorid, (morningprice + afternoonprice + nightprice) as price_sum
        from combined_price) summed
group by monitorid;


-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q2
select monitorid, avg_booking_fee, email 
from    (select * from avg_monitor_price where monitorid not in (select monitorid from simp) 
                                    and monitorid in (select monitorid from avg_monitor_rating)) non_simp
            inner join diver d
                on d.id = non_simp.monitorid;



