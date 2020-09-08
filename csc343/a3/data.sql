-- Starting Values for Testing
insert into Diver values (1,'Dom', 'dom.casillano@mail.utoronto.ca', 'NAUI', '2000-07-10'); 
insert into Diver values (2,'Chris', 'chris.hansen@mail.utoronto.ca', 'NAUI', '2000-08-10');
insert into Diver values (3,'Maria', 'maria.maria@mail.utoronto.ca', 'NAUI', '2000-09-10');
insert into Diver values (4,'Alex', 'alex.pulchico@mail.utoronto.ca', 'NAUI', '2000-07-31');
insert into Diver values (5, 'Bill', 'bill.bill@gmail.com', 'CMAS', '2002-01-12');

insert into Monitor values (1, 10, 8, 6);
insert into Monitor values (2, 20, 20, 10);

insert into Site values (1, 'Marine Land', 'Toronto', 20.00, 20, 0, 10, 10);
insert into Site values (2, 'Lake Ontario', 'Toronto', 15.00, 18, 18, 0, 8);
insert into Site values (3, 'Lake Eerie', 'Eerie', 16.00, 15, 13, 10, 10);

insert into Booking values (1, 3, 1, 1, '2019-05-16 04:05:06', 40.00, '1234567898765432');
insert into Booking values (2, 3, 1, 1, '2019-07-16 04:05:06', 20.00, '9876543212345678');
insert into Booking values (3, 3, 2, 2, '2020-07-16 04:05:06', 20.00, '9876543212345678');

insert into BookedByLead values (4, 1);

insert into LeadDiverSiteRating values (3, 1, 4);
insert into NonLeadDiverSiteRating values (4, 1, 5);

insert into MonitorRating values (3, 1, 5);

insert into MonitorOpenDivePrice values (1, 1, 20.00, 20.00, 15.00);
insert into MonitorCaveDivePrice values (1, 1, 26.00, 26.00, 30.00);
insert into MonitorDeepDivePrice values (1, 1, 30.00, 36.00, 40.00);

insert into MonitorOpenDivePrice values (2, 1, 40.00, 40.00, 25.00);
insert into MonitorCaveDivePrice values (2, 1, 46.00, 46.00, 60.00);
insert into MonitorDeepDivePrice values (2, 1, 60.00, 66.00, 80.00);

insert into MonitorCaveDivePrice values (1, 2, 16.00, 16.00, 10.00);
insert into MonitorDeepDivePrice values (1, 2, 20.00, 26.00, 20.00);

insert into DiveSiteServices values (1, 'dive video', 15.00);