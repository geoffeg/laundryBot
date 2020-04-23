CREATE TABLE devices (
  id   smallserial PRIMARY KEY,
  name text
);

CREATE TABLE sensors (
  id   serial PRIMARY KEY,
  name text
);

CREATE TABLE reading (
  id        bigserial PRIMARY KEY,
  device_id integer,
  sensor_id integer,
  time      timestamp,
  reading   real
);
  
