-- Wet World Schema

drop schema if exists wet_world cascade;
create schema wet_world;
set search_path to wet_world, public;

create table Diver (
  id int primary key,
  name text not null,
  email text unique not null,
  certification char(4) not null check
  (certification in ('NAUI', 'CMAS', 'PADI')),
  birthdate date not null check
  (date_part('year', age(current_date, birthdate)) >= 16)
  );

create table Monitor (
  id int references Diver(id) primary key,
  openWaterCapacity int not null,
  caveCapacity int not null,
  deepDiveCapacity int not null
  );

-- Assumption: if a dive type is not offered
-- at a site, its capacity for that type is 0

create table Site (
  id int primary key,
  name text not null,
  location text not null,
  price numeric(2) not null check 
  (price >= 0),
  dayCapacity int not null check
  (dayCapacity >= 0),
  nightCapacity int not null check
  (nightCapacity >= 0),
  caveCapacity int not null check
  (caveCapacity >= 0),
  deepDiveCapacity int not null check
  (deepDiveCapacity >= 0)
  check (nightCapacity <= dayCapacity and caveCapacity <= dayCapacity
          and deepDiveCapacity <= dayCapacity)
  );

-- Could not enforce constraint where monitors can only dive 
-- at most twice in 24 hours

create table Booking (
  bookingId int primary key,
  leadDiverId int not null references Diver(id),
  siteId int not null references Site(id),
  monitorId int not null references Monitor(id),
  diveDate timestamp not null,
  price numeric(2) not null check
  (price >= 0), 
  charge_card char(16) not null,
  unique (leadDiverId, diveDate),
  unique (bookingId, leadDiverId) 
  );

-- Cannot enforce constraint that divers cannot have two bookings at
-- the same time because it would lead to redundant information

create table BookedByLead (
  diverId int references Diver(id),
  BookingId int references Booking(bookingId),
  primary key (diverId, bookingId)
  );

  
create table NonLeadDiverSiteRating (
  diverId int,
  bookingId int,
  rating int not null check
  (rating >= 0 and rating <= 5),
  primary key (diverId, bookingId),
  foreign key (diverId, bookingId) references BookedByLead(diverId, bookingId)
  );

create table LeadDiverSiteRating (
  leadDiverId int,
  bookingId int,
  rating int not null check
  (rating >= 0 and rating <= 5),
  primary key (leadDiverId, bookingId),
  foreign key (leadDiverId, bookingId) references Booking(leadDiverId, bookingId)
  );

create table MonitorRating (
  leadDiverId int,
  bookingId int,
  rating int not null check 
  (rating >= 0 and rating <= 5),
  primary key (leadDiverId, bookingId),
  foreign key (leadDiverId, bookingId) references Booking(leadDiverId, bookingId) 
  );

-- Separated prices to avoid null values when a
-- diver does not supervise a certain dive type

create table MonitorOpenDivePrice (
  monitorId int references Monitor(id),
  siteId int references Site(id),
  morningPrice numeric(2) not null check
  (morningPrice >= 0),
  afternoonPrice numeric(2) not null check 
  (afternoonPrice >= 0),
  nightPrice numeric(2) not null check
  (nightPrice >= 0),
  primary key (monitorId, siteId)
  );

create table MonitorCaveDivePrice (
  monitorId int references Monitor(id),
  siteId int references Site(id),
  morningPrice numeric(2) not null check
  (morningPrice >= 0),
  afternoonPrice numeric(2) not null check
  (afternoonPrice >= 0),
  nightPrice numeric(2) not null check
  (nightPrice >= 0),
  primary key (monitorId, siteId)
  );

create table MonitorDeepDivePrice (
  monitorId int references Monitor(id),
  siteId int references Site(id),
  morningPrice numeric(2) not null check 
  (morningPrice >= 0),
  afternoonPrice numeric(2) not null check
  (afternoonPrice >= 0),
  nightPrice numeric(2) not null check
  (nightPrice >= 0),
  primary key (monitorId, siteId)
  );

create table DiveSiteServices (
  siteId int primary key references Site(id),
  service text check 
  (service in ('dive video', 'snacks', 'hot showers',
  'towel service', 'mask', 'regulator fins', 
  'wrist-mounted dive computer')),
  price numeric(2) not null check 
  (price >= 0)
  );


   
