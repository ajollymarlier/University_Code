-- Q4. Plane Capacity Histogram

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO air_travel, public;
DROP TABLE IF EXISTS q4 CASCADE;

CREATE TABLE q4 (
	airline CHAR(2),
	tail_number CHAR(5),
	very_low INT,
	low INT,
	fair INT,
	normal INT,
	high INT
);

-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS intermediate_step CASCADE;


-- Define views for your intermediate steps here:
/* combines all plane info with total attendances and total capacity */
DROP VIEW IF EXISTS plane_capacity CASCADE;
create view plane_capacity as
select total_caps.flight_id, total_caps.plane, total_caps.total_capacity,
 total_caps.airline, total_atts.attendance 
from    (select f.id flight_id, f.plane, 
capacity_economy + capacity_business + capacity_first total_capacity, 
f.airline
        from flight f inner join plane p
        on f.plane = p.tail_number) total_caps
   left join /* left ? */
        (select flight_id, count(id) attendance
        from booking
        group by flight_id) total_atts
on total_caps.flight_id = total_atts.flight_id;

/* get flights that had high capacity */
DROP VIEW IF EXISTS high_capacity CASCADE;
create view high_capacity as
select plane, count(flight_id) num_high_flights
from plane_capacity
where attendance >= (total_capacity * 0.8)
group by plane;

/* get flights that had normal capacity */
DROP VIEW IF EXISTS normal_capacity CASCADE;
create view normal_capacity as
select plane, count(flight_id) num_normal_flights
from plane_capacity
where attendance >= (total_capacity * 0.6) 
and attendance < (total_capacity * 0.8)
group by plane;

/* get flights that had fair capacity */
DROP VIEW IF EXISTS fair_capacity CASCADE;
create view fair_capacity as
select plane, count(flight_id) num_fair_flights
from plane_capacity
where attendance >= (total_capacity * 0.4) 
and attendance < (total_capacity * 0.6)
group by plane;

/* get flights that had low capacity */
DROP VIEW IF EXISTS low_capacity CASCADE;
create view low_capacity as
select plane, count(flight_id) num_low_flights
from plane_capacity
where attendance >= (total_capacity * 0.2) 
and attendance < (total_capacity * 0.4)
group by plane;

/* get flights that had very low capacity */
DROP VIEW IF EXISTS very_low_capacity CASCADE;
create view very_low_capacity as
select plane, count(flight_id) num_very_low_flights
from plane_capacity
where attendance < (total_capacity * 0.2)
group by plane;

/* combine all capacity tables */
DROP table IF EXISTS final_table_w_null CASCADE;
create table final_table_w_null as
select airline, plane_capacity.plane tail_number, 
num_very_low_flights very_low, num_low_flights low, 
        num_fair_flights fair, num_normal_flights normal, 
        num_high_flights high 
from            plane_capacity
            left join
                high_capacity 
                on high_capacity.plane = plane_capacity.plane
            left join 
                normal_capacity 
                on normal_capacity.plane = plane_capacity.plane
            left join
                fair_capacity 
                on fair_capacity.plane = plane_capacity.plane
            left join
                low_capacity 
                on low_capacity.plane = plane_capacity.plane
            left join
                very_low_capacity 
                on very_low_capacity.plane = plane_capacity.plane;

/* updates null very_low values to 0s */
update final_table_w_null set very_low = 0
where very_low is NULL;

/* updates null low values to 0s */
update final_table_w_null set low = 0
where low is NULL;

/* updates null fair values to 0s */
update final_table_w_null set fair = 0
where fair is NULL;

/* updates null normal values to 0s */
update final_table_w_null set normal = 0
where normal is NULL;

/* updates null high values to 0s */
update final_table_w_null set high = 0
where high is NULL;

-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q4
/*final query */
select airline, tail_number, sum(very_low) very_low, 
sum(low) low, sum(fair) fair, sum(normal) normal, 
sum(high) high
from final_table_w_null
group by tail_number, airline;

