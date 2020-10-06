CREATE TABLE rpmc (
    recorded_at TIMESTAMP NOT NULL,
    device_id VARCHAR,
    temperature DECIMAL(2),
    oxygen_saturation INTEGER,
    heart_rate INTEGER,
    respiratory_rate INTEGER,
    FOREIGN KEY (device_id) REFERENCES devices (id)
    );

CREATE TABLE rpmnc (
    recorded_at TIMESTAMP NOT NULL,
    device_id VARCHAR,
    bp_systolic INTEGER,
    bp_diastolic INTEGER,
    FOREIGN KEY (device_id) REFERENCES devices (id)
    );

INSERT INTO rpmc(recorded_at, device_id, temperature, oxygen_saturation, heart_rate ) VALUES ('2020-09-28 18:46:28', 'rpm-pbi-dev-1', 36.50, 99, 72);

CREATE TABLE devices (id VARCHAR PRIMARY KEY, type VARCHAR(50), rented_to VARCHAR(50),rented_at TIMESTAMP, returned_at TIMESTAMP );
INSERT INTO devices(id, type, rented_to, rented_at ) VALUES ('rpm-pbi-dev-1','PM6100','Hussnain','2020-09-28 18:46:28');
INSERT INTO devices(id, type, rented_to, rented_at ) VALUES ('rpm-pbi-dev-2','PM6100','Ahmed','2020-09-28 18:46:28');
INSERT INTO devices(id, type, rented_to, rented_at ) VALUES ('rpm-pbi-dev-3','PM6100','Waqas','2020-09-28 18:46:28');
INSERT INTO devices(id, type, rented_to, rented_at ) VALUES ('rpm-pbi-dev-4','PM6100','Ali','2020-09-28 18:46:28');
INSERT INTO devices(id, type, rented_to, rented_at ) VALUES ('rpm-pbi-dev-5','PM6100','Wasim','2020-09-28 18:46:28');





SELECT * FROM create_hypertable('rpmc', 'recorded_at',chunk_time_interval => INTERVAL '1 week');
SELECT * FROM create_hypertable('rpmnc', 'recorded_at',chunk_time_interval => INTERVAL '1 month');