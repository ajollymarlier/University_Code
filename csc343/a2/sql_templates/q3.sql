-- Q3. North and South Connections

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO air_travel, public;
DROP TABLE IF EXISTS q3 CASCADE;

CREATE TABLE q3 (
    outbound VARCHAR(30),
    inbound VARCHAR(30),
    direct INT,
    one_con INT,
    two_con INT,
    earliest timestamp
);

-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS intermediate_step CASCADE;

/* all airport info from all combos of canada-usa connections */
DROP VIEW IF EXISTS can_city_combos CASCADE;
create view can_city_combos as
select air1.code can_code, air1.city can_city, air1.country can_country,
        air2.code air2_code, air2.city air2_city, 
        air2.country air2_country,
        air3.code air3_code, air3.city air3_city, 
        air3.country air3_country,
        air4.code air4_code, air4.city air4_city, 
        air4.country air4_country
from airport air1, airport air2, airport air3, airport air4
where ((air1.country = 'Canada' and air2.country = 'USA') 
        or (air1.country = 'Canada' and air3.country = 'USA') 
        or (air1.country = 'Canada' and air4.country = 'USA'));

/* all airport info from all combos of usa-canada connections */
DROP VIEW IF EXISTS usa_city_combos CASCADE;
create view usa_city_combos as
select air1.code usa_code, air1.city usa_city, 
air1.country usa_country,
        air2.code air2_code, air2.city air2_city, 
        air2.country air2_country,
        air3.code air3_code, air3.city air3_city, 
        air3.country air3_country,
        air4.code air4_code, air4.city air4_city, 
        air4.country air4_country
from airport air1, airport air2, airport air3, 
airport air4
where ((air1.country = 'USA' and air2.country = 'Canada') 
        or (air1.country = 'USA' and air3.country = 'Canada') 
        or (air1.country = 'USA' and air4.country = 'Canada'));

/* all possible one flight routes for canada-usa */
DROP VIEW IF EXISTS view one_flight_can_usa CASCADE;
create view one_flight_can_usa as
select f.id f1_id, f.s_dep f1_s_dep, f.s_arv f1_s_arv, 
c.can_code outbound, c.air2_code inbound
from flight f
        inner join can_city_combos c on c.can_code = f.outbound
where c.air2_country = 'USA' 
        and c.air2_code = f.inbound 
        and date_part('year', f.s_dep) = '2020' 
        and date_part('month', f.s_dep) = '04'
        and date_part('day', f.s_dep) = '30'
group by f.id, f.s_dep, c.can_code, c.air2_code
order by f.s_dep;

/* all possible one flight routes for usa-canada */
DROP VIEW IF EXISTS one_flight_usa_can CASCADE;
create view one_flight_usa_can as
select f.id f1_id, f.s_dep f1_s_dep, f.s_arv f1_s_arv, 
c.usa_code outbound, c.air2_code inbound
from flight f
        inner join usa_city_combos c on c.usa_code = f.outbound
where c.air2_country = 'Canada' 
        and c.air2_code = f.inbound 
        and date_part('year', f.s_dep) = '2020' 
        and date_part('month', f.s_dep) = '04'
        and date_part('day', f.s_dep) = '30'
group by f.id, f.s_dep, f.s_arv, c.usa_code, c.air2_code
order by f.s_dep;

/* all possible two flight routes for canada-usa */
DROP VIEW IF EXISTS two_flight_can_usa CASCADE;
create view two_flight_can_usa as
select f1.id f1_id, f1.s_dep f1_s_dep, f1.s_arv f1_s_arv, 
f2.id f2_id, f2.s_dep f2_s_dep, f2.s_arv f2_s_arv, f1.outbound outbound, 
f2.inbound inbound
from flight f1
        inner join flight f2 on f1.inbound = f2.outbound
        inner join can_city_combos c on c.can_code = f1.outbound
where c.air3_country = 'USA' 
        and c.air3_code = f2.inbound 
        and date_part('year', f1.s_dep) = '2020' 
        and date_part('month', f1.s_dep) = '04'
        and date_part('day', f1.s_dep) = '30'
        and (f2.s_dep - f1.s_arv) > '0:30:00'
group by f1.id, f1.s_dep, f1.s_arv, f2.id, f2.s_dep, f2_s_arv, 
f1.inbound, f2.outbound 
order by f1.s_dep;

/* all possible two flight routes for usa-canada */
DROP VIEW IF EXISTS two_flight_usa_can CASCADE;
create view two_flight_usa_can as
select f1.id f1_id, f1.s_dep f1_s_dep, f1.s_arv f1_s_arv, f2.id f2_id, 
f2.s_dep f2_s_dep, f2.s_arv f2_s_arv , f1.outbound outbound, 
f2.inbound inbound
from flight f1
        inner join flight f2 on f1.inbound = f2.outbound
        inner join usa_city_combos c on c.usa_code = f1.outbound
where c.air3_country = 'Canada' 
        and c.air3_code = f2.inbound 
        and date_part('year', f1.s_dep) = '2020' 
        and date_part('month', f1.s_dep) = '04'
        and date_part('day', f1.s_dep) = '30'
        and (f2.s_dep - f1.s_arv) > '0:30:00'
group by f1.id, f1.s_dep, f1.s_arv, f2.id, f2.s_dep, f2_s_arv, 
f1.inbound, f2.outbound
order by f1.s_dep;

/* all possible three flight routes for canada-usa */
DROP VIEW IF EXISTS three_flight_can_usa CASCADE;
create view three_flight_can_usa as
select f1.id f1_id, f1.s_dep f1_s_dep, f1.s_arv f1_s_arv, f2.id f2_id, 
f2.s_dep f2_s_dep, f2.s_arv f2_s_arv, f3.id f3_id, f3.s_dep f3_s_dep, 
f3.s_arv f3_s_arv, f1.outbound outbound, f3.inbound inbound
from flight f1
        inner join flight f2 on f1.inbound = f2.outbound
        inner join flight f3 on f2.inbound = f3.outbound
        inner join can_city_combos c on c.can_code = f1.outbound
where c.air4_country = 'USA' 
        and c.air4_code = f3.inbound 
        and c.air3_code = f2.inbound
        and date_part('year', f1.s_dep) = '2020' 
        and date_part('month', f1.s_dep) = '04'
        and date_part('day', f1.s_dep) = '30'
        and (f2.s_dep - f1.s_arv) > '0:30:00'
        and (f3.s_dep - f2.s_arv) > '0:30:00'
group by f1.id, f1.s_dep, f1.s_arv, f2.id, f2.s_dep, f1.id, f1.s_dep, 
f1.s_arv, f2.id, f2.s_dep, f2.s_arv, f3.id, f3.s_dep, f3_s_arv, f1.inbound, 
f3.outbound
order by f1.s_dep;

/* all possible three flight routes for usa-canada */
DROP VIEW IF EXISTS three_flight_usa_can CASCADE;
create view three_flight_usa_can as
select f1.id f1_id, f1.s_dep f1_s_dep, f1.s_arv f1_s_arv, f2.id f2_id, 
f2.s_dep f2_s_dep, f2.s_arv f2_s_arv, f3.id f3_id, f3.s_dep f3_s_dep, 
f3.s_arv f3_s_arv, f1.outbound outbound, f3.inbound inbound
from flight f1
        inner join flight f2 on f1.inbound = f2.outbound
        inner join flight f3 on f2.inbound = f3.outbound
        inner join usa_city_combos c on c.usa_code = f1.outbound
where c.air4_country = 'Canada' 
        and c.air4_code = f3.inbound 
        and c.air3_code = f2.inbound
        and date_part('year', f1.s_dep) = '2020' 
        and date_part('month', f1.s_dep) = '04'
        and date_part('day', f1.s_dep) = '30'
        and (f2.s_dep - f1.s_arv) > '0:30:00'
        and (f3.s_dep - f2.s_arv) > '0:30:00'
group by f1.id, f1.s_dep, f1.s_arv, f2.id, f2.s_dep, f1.id, f1.s_dep, 
f1.s_arv, f2.id, f2.s_dep, f2.s_arv, f3.id, f3.s_dep, f3_s_arv, 
f1.inbound, f3.outbound
order by f1.s_dep;

/* can_usa single code combos */
DROP VIEW IF EXISTS can_usa_city_pairs CASCADE;
create view can_usa_city_pairs as
select air1.code air1_code, air1.city air1_city,
        air2.code air2_code, air2.city air2_city
from airport air1, airport air2
where ((air1.country = 'Canada' and air2.country = 'USA') 
or (air1.country = 'USA' and air2.country = 'Canada'));

/*Get count for number of flights with all city combos for one_flight */
DROP VIEW IF EXISTS one_flight_combos CASCADE;
create view one_flight_combos as
select air1_city outbound, air2_city inbound, 
count(ofcu.f1_id) + count(ofuc.f1_id) num_one_flights, 
min(ofcu.f1_s_arv) earliest_one_can_usa, 
min(ofuc.f1_s_arv) earliest_one_usa_can
from can_usa_city_pairs cucp
        left join one_flight_can_usa ofcu 
        on (cucp.air1_code = ofcu.outbound and cucp.air2_code = ofcu.inbound)
        left join one_flight_usa_can ofuc 
        on (ofcu.inbound = ofuc.outbound and ofcu.outbound = ofuc.inbound)
group by air1_city, air2_city;

/*Get count for number of flights with all city combos for two_flight */
DROP VIEW IF EXISTS two_flight_combos CASCADE;
create view two_flight_combos as
select air1_city outbound, air2_city inbound, 
count(tfcu.f1_id) + count(tfuc.f1_id) num_two_flights, 
min(tfcu.f2_s_arv) earliest_two_can_usa, 
min(tfuc.f2_s_arv) earliest_two_usa_can
from can_usa_city_pairs cucp
        left join two_flight_can_usa tfcu 
        on (cucp.air1_code = tfcu.outbound and cucp.air2_code = tfcu.inbound)
        left join two_flight_usa_can tfuc 
        on (tfcu.inbound = tfuc.outbound and tfcu.outbound = tfuc.inbound)
group by air1_city, air2_city;

/*Get count for number of flights with all city combos for three_flight */
DROP VIEW IF EXISTS three_flight_combos CASCADE;
create view three_flight_combos as
select air1_city outbound, air2_city inbound, 
count(thfcu.f1_id) + count(thfuc.f1_id) num_three_flights, 
min(thfcu.f3_s_arv) earliest_three_can_usa, 
min(thfuc.f3_s_arv) earliest_three_usa_can
from can_usa_city_pairs cucp
        left join three_flight_can_usa thfcu 
        on (cucp.air1_code = thfcu.outbound and cucp.air2_code = thfcu.inbound)
        left join three_flight_usa_can thfuc 
        on (thfcu.inbound = thfuc.outbound and thfcu.outbound = thfuc.inbound)
group by air1_city, air2_city;


-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q3
select ofc.outbound, ofc.inbound, num_one_flights direct, 
num_two_flights one_con, num_three_flights two_con, 
        (SELECT MIN(C)
        FROM (VALUES 
                (earliest_one_can_usa), 
                (earliest_one_usa_can), 
                (earliest_two_can_usa), 
                (earliest_two_usa_can), 
                (earliest_three_can_usa), 
                (earliest_three_usa_can))
                AS v (C)) AS earliest
from one_flight_combos ofc
        inner join two_flight_combos tfc 
        on (ofc.outbound = tfc.outbound and ofc.inbound = tfc.inbound)
        inner join three_flight_combos thfc
        on (ofc.outbound = thfc.outbound and ofc.inbound = thfc.inbound);