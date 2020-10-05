CREATE TABLE "devices_meta" (
	"device_id" VARCHAR NOT NULL,
	"device_name" VARCHAR NOT NULL,
	"vendor" VARCHAR,
	"created_at" TIMESTAMP,
	"is_device_in_hub" BOOLEAN,
	"created_at_hub" TIMESTAMP,
	CONSTRAINT "devices_meta_pk" PRIMARY KEY ("device_id")
);



CREATE TABLE "users_meta" (
	"user_id" VARCHAR NOT NULL,
	"user_name" VARCHAR NOT NULL,
	"address" VARCHAR,
	"dob" DATE NOT NULL,
	"created_at" TIMESTAMP,
	CONSTRAINT "users_meta_pk" PRIMARY KEY ("user_id")
);



CREATE TABLE "device_rentals" (
	"device_id" VARCHAR NOT NULL,
	"rented_at" TIMESTAMP NOT NULL,
	"rented_to_uid" VARCHAR NOT NULL,
	"rented_to_name" VARCHAR NOT NULL,
	"transaction_id" SERIAL NOT NULL,
	"is_returned" BOOLEAN,
	"returned_at" TIMESTAMP,
	FOREIGN KEY (device_id) REFERENCES devices_meta (device_id),
	FOREIGN KEY (rented_to_uid) REFERENCES users_meta (user_id),
	CONSTRAINT "device_rentals_pk" PRIMARY KEY ("transaction_id")
);



CREATE TABLE "rpm_cont_data" (
	"recorded_at" TIMESTAMP NOT NULL,
	"device_id" VARCHAR NOT NULL,
	"rented_to_uid" VARCHAR NOT NULL,
	"rented_to_name" VARCHAR NOT NULL,
	"temperature" DECIMAL(2) NOT NULL,
	"oxygen_saturation" smallint,
	"heart_rate" smallint,
	"respiratory_rate" smallint,
	"mews" smallint
);



CREATE TABLE "rpm_non_cont_data" (
	"recorded_at" TIMESTAMP NOT NULL,
	"device_id" VARCHAR NOT NULL,
	"rented_to_uid" VARCHAR NOT NULL,
	"rented_to_name" VARCHAR NOT NULL,
	"bp_systolic" smallint,
	"bp_diastolic" smallint
);

SELECT * FROM create_hypertable('rpm_cont_data', 'recorded_at',chunk_time_interval => INTERVAL '1 week');
SELECT * FROM create_hypertable('rpm_non_cont_data', 'recorded_at',chunk_time_interval => INTERVAL '1 month');

INSERT INTO devices_meta(device_id, device_name, vendor,created_at, is_device_in_hub,  created_at_hub ) VALUES ('rpm-pbi-dev-1','PM6100','BerryMed','2020-09-28 18:46:28','1','2020-09-28 18:46:28');
INSERT INTO devices_meta(device_id, device_name, vendor,created_at, is_device_in_hub,  created_at_hub ) VALUES ('rpm-pbi-dev-2','PM6100','BerryMed','2020-09-28 18:46:28','1','2020-09-28 18:46:28');
INSERT INTO devices_meta(device_id, device_name, vendor,created_at, is_device_in_hub) VALUES ('rpm-pbi-dev-3','PM6100','BerryMed','2020-09-28 18:46:28','0');
INSERT INTO devices_meta(device_id, device_name, vendor,created_at, is_device_in_hub) VALUES ('rpm-pbi-dev-4','PM6100','BerryMed','2020-09-28 18:46:28','0');
INSERT INTO devices_meta(device_id, device_name, vendor,created_at, is_device_in_hub) VALUES ('rpm-pbi-dev-5','PM6100','BerryMed','2020-09-28 18:46:28','0');
INSERT INTO devices_meta(device_id, device_name, vendor,created_at, is_device_in_hub) VALUES ('rpm-pbi-dev-6','PM6100','BerryMed','2020-09-28 18:46:28','0');
UPDATE devices_meta SET created_at_hub = NULL WHERE device_id = 'rpm-pbi-dev-3';


INSERT INTO users_meta(user_id, user_name, address, dob, created_at ) VALUES ('100001','Hussnain Ahmed','H8/4 Islamabad','1982-04-04','2020-09-28 18:46:28');
INSERT INTO users_meta(user_id, user_name, address, dob, created_at ) VALUES ('100002','Ali Ahmed','H8/4 Islamabad','1982-04-04','2020-09-28 18:46:28');
INSERT INTO users_meta(user_id, user_name, address, dob, created_at ) VALUES ('100003','Shehnaz Akhter','I8/3 Islamabad','1965-07-05','2020-09-28 18:46:28');
INSERT INTO users_meta(user_id, user_name, address, dob, created_at ) VALUES ('100004','Shahid Hameed','F7/4 Islamabad','1982-09-08','2020-09-28 18:46:28');
INSERT INTO users_meta(user_id, user_name, address, dob, created_at ) VALUES ('100005','Farhan Ali','H8/3 Islamabad','1976-05-03','2020-09-28 18:46:28');
INSERT INTO users_meta(user_id, user_name, address, dob, created_at ) VALUES ('100006','Shazia Khan','H8/2 Islamabad','2001-03-04','2020-09-28 18:46:28');




INSERT INTO device_rentals (device_id, rented_at, rented_to_uid, rented_to_name ) VALUES ('rpm-pbi-dev-1','2020-09-28 18:46:28','100001','Hussnain Ahmed');
INSERT INTO device_rentals (device_id, rented_at, rented_to_uid, rented_to_name ) VALUES ('rpm-pbi-dev-2','2020-09-28 18:46:28','100002','Ali Ahmed');
INSERT INTO device_rentals (device_id, rented_at, rented_to_uid, rented_to_name ) VALUES ('rpm-pbi-dev-3','2020-09-28 18:46:28','100003','Shehnaz Akhter');



INSERT INTO devices(id, type, rented_to, rented_at ) VALUES ('rpm-pbi-dev-4','PM6100','Ali','2020-09-28 18:46:28');
INSERT INTO devices(id, type, rented_to, rented_at ) VALUES ('rpm-pbi-dev-5','PM6100','Wasim','2020-09-28 18:46:28');


