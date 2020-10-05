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
	"user_id" SERIAL NOT NULL,
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
	CONSTRAINT "device_rentals_pk" PRIMARY KEY ("transaction_id")
);



CREATE TABLE "rpm_cont_data" (
	"recorded_at" TIMESTAMP NOT NULL,
	"device_id" VARCHAR NOT NULL,
	"rented_to_id" VARCHAR NOT NULL,
	"rented_to_name" VARCHAR NOT NULL,
	"temperature" DECIMAL(2) NOT NULL,
	"oxygen_saturation" smallint,
	"heart_rate" smallint,
	"respiratory_rate" smallint,
	"mews" smallint
);



CREATE TABLE "rpm_cont_data copy" (
	"recorded_at" TIMESTAMP NOT NULL,
	"device_id" VARCHAR NOT NULL,
	"rented_to_id" VARCHAR NOT NULL,
	"rented_to_name" VARCHAR NOT NULL,
	"bp_systolic" smallint,
	"bp_diastolic" smallint
);





ALTER TABLE "device_rentals" ADD CONSTRAINT "device_rentals_fk0" FOREIGN KEY ("device_id") REFERENCES "devices_meta"("device_id");
ALTER TABLE "device_rentals" ADD CONSTRAINT "device_rentals_fk1" FOREIGN KEY ("rented_to_uid") REFERENCES "users_meta"("user_id");
ALTER TABLE "device_rentals" ADD CONSTRAINT "device_rentals_fk2" FOREIGN KEY ("rented_to_name") REFERENCES "users_meta"("user_name");

ALTER TABLE "rpm_cont_data" ADD CONSTRAINT "rpm_cont_data_fk0" FOREIGN KEY ("device_id") REFERENCES "devices_meta"("device_id");
ALTER TABLE "rpm_cont_data" ADD CONSTRAINT "rpm_cont_data_fk1" FOREIGN KEY ("rented_to_id") REFERENCES "users_meta"("user_id");
ALTER TABLE "rpm_cont_data" ADD CONSTRAINT "rpm_cont_data_fk2" FOREIGN KEY ("rented_to_name") REFERENCES "users_meta"("user_name");

ALTER TABLE "rpm_cont_data copy" ADD CONSTRAINT "rpm_cont_data copy_fk0" FOREIGN KEY ("device_id") REFERENCES "devices_meta"("device_id");
ALTER TABLE "rpm_cont_data copy" ADD CONSTRAINT "rpm_cont_data copy_fk1" FOREIGN KEY ("rented_to_id") REFERENCES "users_meta"("user_id");
ALTER TABLE "rpm_cont_data copy" ADD CONSTRAINT "rpm_cont_data copy_fk2" FOREIGN KEY ("rented_to_name") REFERENCES "users_meta"("user_name");

