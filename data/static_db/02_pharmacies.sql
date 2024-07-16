create table pharmacies
(
    name     TEXT collate NOCASE    not null,
    postcode TEXT(8) collate NOCASE not null,
    address  TEXT collate NOCASE    not null,
    latitude  REAL,
    longitude REAL
);

create index pharmacies_address_index
    on pharmacies (address);

create index pharmacies_name_index
    on pharmacies (name);

create index pharmacies_postcode_index
    on pharmacies (postcode);

create index pharmacies_latitude_index
    on pharmacies (latitude);

create index pharmacies_longitude_index
    on pharmacies (longitude);

-- create view pharmacies_geolocated as
-- SELECT
--     name, pharmacies.postcode, address, latitude, longitude
-- FROM pharmacies
-- LEFT OUTER JOIN
--     main.postcodes p on pharmacies.postcode = p.postcode;
