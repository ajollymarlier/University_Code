/* 1. */
select b.pass_id as pass_id, (firstname || ' ' ||  surname) as name, count(b.flight_id) as airlines
from booking b full join passenger p 
    on b.pass_id = p.id
group by pass_id, firstname, surname;