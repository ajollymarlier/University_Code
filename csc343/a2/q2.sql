/* get scheduled and real times with locations and flight_id */
create view flightinfo as
select f.id flight_id, s_dep, s_arv, d.datetime r_dep, a.datetime r_arv, air1.country out_country, air2.country in_country, b.price, b.seat_class, f.airline, airl.name
from flight f inner join departure d on f.id = d.flight_id 
                inner join arrival a on f.id = a.flight_id 
                inner join airport air1 on f.outbound = air1.code 
                inner join airport air2 on f.inbound = air2.code
                inner join airline airl on airl.code = f.airline
                inner join booking b on f.id = b.flight_id;

/* domestic low refunds */\
create view dom_low_refunds as
select sum(price * 0.35) refund_sum, seat_class, flight_id, airline, name
from flightinfo 
where (out_country = in_country) and ((r_dep - s_dep) >= '4:00:00') and ((r_dep - s_dep) < '10:00:00') and ((r_arv - s_arv) > (r_dep - s_dep) * 0.5)
group by seat_class, flight_id, airline, name;

/* domestic high refunds */
create view dom_high_refunds as
select sum(price * 0.50) refund_sum, seat_class, flight_id, airline, name
from flightinfo 
where (out_country = in_country) and ((r_dep - s_dep) >= '10:00:00') and ((r_arv - s_arv) > (r_dep - s_dep) * 0.5)
group by seat_class, flight_id, airline, name;

/* domestic low refunds */
create view int_low_refunds as
select sum(price * 0.35) refund_sum, seat_class, flight_id, airline, name
from flightinfo 
where (out_country != in_country) and ((r_dep - s_dep) >= '7:00:00') and ((r_dep - s_dep) < '12:00:00') and ((r_arv - s_arv) > (r_dep - s_dep) * 0.5)
group by seat_class, flight_id, airline, name;

/* domestic high refunds */
create view int_high_refunds as
select sum(price * 0.35) refund_sum, seat_class, flight_id, airline, name
from flightinfo 
where (out_country != in_country) and ((r_dep - s_dep) >= '12:00:00') and ((r_arv - s_arv) > (r_dep - s_dep) * 0.5)
group by seat_class, flight_id, airline, name;

/*Get table of split refunds*/
create table split_refund_table as
select fi.airline, fi.name, date_part('year', fi.s_dep) as year, fi.seat_class, dlf.refund_sum dlf_refund, dhf.refund_sum dhf_refund, ilf.refund_sum ilf_refund, ihf.refund_sum ihf_refund
from    flightinfo fi
        left join dom_low_refunds dlf on (fi.seat_class = dlf.seat_class and fi.flight_id = dlf.flight_id)
        left join dom_high_refunds dhf on (fi.seat_class = dhf.seat_class and fi.flight_id = dhf.flight_id)
        left join int_low_refunds ilf on (fi.seat_class = ilf.seat_class and fi.flight_id = ilf.flight_id)
        left join int_high_refunds ihf on (fi.seat_class = ihf.seat_class and fi.flight_id = ihf.flight_id)
group by fi.airline, fi.name, date_part('year', fi.s_dep), fi.seat_class, dlf.refund_sum, dhf.refund_sum, ilf.refund_sum, ihf.refund_sum;

/* updates null dlf_refund values to 0s */
update split_refund_table set dlf_refund = 0
where dlf_refund is NULL;

/* updates null dhf_refund values to 0s */
update split_refund_table set dhf_refund = 0
where dhf_refund is NULL;

/* updates null ilf_refund values to 0s */
update split_refund_table set ilf_refund = 0
where ilf_refund is NULL;

/* updates null ihf_refund values to 0s */
update split_refund_table set ihf_refund = 0
where ihf_refund is NULL;

/*Final table*/
create view final_table as
select airline, name, year, seat_class, (dlf_refund + dhf_refund + ilf_refund + ihf_refund) refund
from split_refund_table;

/*Final Query taht combines same airline flights in same year refunds*/
select airline, name, year, seat_class, sum(refund) refund
from final_table
group by airline, name, year, seat_class;