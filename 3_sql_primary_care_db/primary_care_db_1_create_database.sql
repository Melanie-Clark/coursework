DROP DATABASE IF EXISTS primary_care_db;

CREATE DATABASE primary_care_db;

USE primary_care_db;

-- Creation of tables
CREATE TABLE titles (
	title_id INT AUTO_INCREMENT,
	title_description VARCHAR(20) NOT NULL UNIQUE,
	PRIMARY KEY (title_id)
);

CREATE TABLE staff_roles (
	staff_role_id INT AUTO_INCREMENT,
	staff_role_description VARCHAR(50) NOT NULL UNIQUE,
	PRIMARY KEY (staff_role_id)
);

CREATE TABLE staff_members (
	staff_member_id INT AUTO_INCREMENT,
    staff_member_title_id INT,
	staff_member_forename VARCHAR(40) NOT NULL,
	staff_member_surname VARCHAR(40) NOT NULL,
	staff_member_role_id INT,
	PRIMARY KEY (staff_member_id),
    FOREIGN KEY (staff_member_title_id) REFERENCES titles (title_id),
	FOREIGN KEY (staff_member_role_id) REFERENCES staff_roles (staff_role_id)
);

CREATE TABLE addresses (
	address_id INT AUTO_INCREMENT,
	house_number_name VARCHAR(30) NOT NULL,
	street VARCHAR(200),
    town_city VARCHAR(200),
    county VARCHAR(200),
    postcode VARCHAR(10) NOT NULL,
	PRIMARY KEY (address_id),
    CONSTRAINT unique_address UNIQUE (house_number_name, postcode)
);

CREATE TABLE patients (
	patient_id INT AUTO_INCREMENT,
	patient_title_id INT,
	patient_forename VARCHAR(40) NOT NULL,
	patient_surname VARCHAR(40) NOT NULL,
    address_id INT,
    date_of_birth DATE NOT NULL,
	nhs_number VARCHAR(10) NOT NULL UNIQUE,
	registered_gp_id INT NOT NULL,
	PRIMARY KEY (patient_id),
	FOREIGN KEY (patient_title_id) REFERENCES titles (title_id),
    FOREIGN KEY (address_id) REFERENCES addresses (address_id),
	FOREIGN KEY (registered_gp_id) REFERENCES staff_members (staff_member_id)
);

CREATE TABLE appointments (
	appointment_id INT AUTO_INCREMENT,
	appointment_date DATE NOT NULL,
	appointment_time TIME NOT NULL,
	staff_member_id INT NOT NULL,
	patient_id INT,
	PRIMARY KEY (appointment_id),
	FOREIGN KEY (staff_member_id) REFERENCES staff_members (staff_member_id),
	FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
);

CREATE TABLE medical_history (
	history_id INT AUTO_INCREMENT,
    patient_id INT NOT NULL,
    entry_date DATE,
    diagnosis VARCHAR(100),
    test VARCHAR(100),
    test_result INT,
    PRIMARY KEY (history_id),
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
);


-- Data insertion
INSERT INTO titles (title_description)
VALUES
('Miss'),
('Mrs'),
('Ms'),
('Mr'),
('Master'),
('Sir'),
('Doctor'),
('Professor');

INSERT INTO staff_roles (staff_role_description)
VALUES
('Doctor'),
('Nurse'),
('Phlebotomist'),
('Practice Manager'),
('Administrator'),
('Senior Administrator'),
('Receptionist'),
('Dietician');

INSERT INTO staff_members (staff_member_title_id, staff_member_forename, staff_member_surname, staff_member_role_id)
VALUES
(7, 'Doing', 'Well', 1),
(2, 'Know', 'It-All', 2),
(4, 'Phil', 'It-Up', 3),
(2, 'Running-Around', 'All-Day', 4),
(1, 'Willing', 'N-Able', 5),
(1, 'Super', 'Achiever', 6),
(4, 'Ringing', 'All-Day', 7),
(4, 'Do', 'More', 8),
(7, 'Do', 'Little', 1)
;

INSERT INTO addresses (house_number_name, street, town_city, county, postcode)
VALUES
(100, 'Secret_Street', 'Anon', NULL, 'AN01 0NS'),
(1, 'Disney_Way', 'Orlando', 'Florida', 'DI55 0EY'),
(5, 'Love_Avenue', 'Notting Hill', 'London', 'HG01 2JR')
;

INSERT INTO patients (patient_title_id, patient_forename, patient_surname, address_id, date_of_birth, nhs_number, registered_gp_id)
VALUES
(1, 'Jane', 'Doe', 1, '1960-01-01', 1234567890, 1),
(2, 'Minnie', 'Mouse', 2, '1950-12-25', 2345678901, 1),
(4, 'Mickey', 'Mouse', 2, '1950-02-14', 3456789012, 1),
(NULL, 'John', 'Doe', 1, '1993-09-29', 4567890123, 1),
(5, 'Jack', 'Doe', 1, '1974-05-02', 5678901234, 1),
(6, 'Hugh', 'Grant', 3, '1980-09-23', 6789012345, 1),
(7, 'Donald', 'Duck', 2, '1945-08-15', 7890123456, 1),
(8, 'Daisy', 'Duck', 2, '1948-06-14', 8901234567, 1);

INSERT INTO medical_history	(patient_id, entry_date, diagnosis, test, test_result)
VALUES
(1, '2023-01-01', 'Asthma', NULL, NULL),
(2, '2017-05-03', 'Diabetes Type 2', 'HbA1c', 58),
(2, '2018-02-03', 'Diabetes resolved', 'HbA1c', 40),
(2, '2020-05-03', 'Diabetes Type 2', 'HbA1c', 50),
(3, '2019-05-03', 'Diabetes Type 2', 'HbA1c', 48),
(4, '2018-05-03', 'Diabetes Type 1', 'HbA1c', 99),
(5, '2015-09-30', 'Diabetes Type 2', 'HbA1c', 60),
(5, '2024-04-02', 'Diabetes resolved', 'HbA1c' , 41),
(6, NULL, NULL, 'HbA1c', 42),
(7, '2020-07-03', 'Diabetes Type 2', 'HbA1c', 99),
(7, '2020-05-08', 'Asthma', NULL, NULL),
(8, '2015-11-10', 'Diabetes Type 1', 'HbA1c' , 56)
;

-- Appointment list for Nurse/Doctor, with a sample of patients booked
INSERT INTO appointments (appointment_date, appointment_time, staff_member_id, patient_id)
VALUES
('2024-11-01', '09:00:00', 1, 1),
('2024-11-01', '09:30:00', 1, 2),
('2024-11-01', '10:00:00', 1, 3),
('2024-11-01', '10:30:00', 1, NULL),
('2024-11-01', '11:00:00', 1, NULL),
('2024-11-01', '11:30:00', 1, 4),
('2024-11-01', '12:00:00', 1, NULL),
('2024-11-01', '12:30:00', 1, 6),
('2024-11-01', '13:00:00', 1, NULL),
('2024-11-01', '09:00:00', 2, 1),
('2024-11-01', '09:30:00', 2, NULL),
('2024-11-01', '10:00:00', 2, NULL),
('2024-11-01', '10:30:00', 2, 4),
('2024-11-01', '11:00:00', 2, NULL),
('2024-11-01', '11:30:00', 2, NULL),
('2024-11-01', '12:00:00', 2, 7),
('2024-11-01', '12:30:00', 2, NULL),
('2024-11-01', '13:00:00', 2, NULL),
('2024-11-02', '09:00:00', 9, NULL),
('2024-11-02', '09:30:00', 9, NULL),
('2024-11-02', '10:00:00', 9, NULL),
('2024-11-02', '10:30:00', 9, NULL),
('2024-11-02', '11:00:00', 9, 5),
('2024-11-02', '11:30:00', 9, NULL),
('2024-11-02', '12:00:00', 9, NULL),
('2024-11-02', '12:30:00', 9, NULL),
('2024-11-02', '13:00:00', 9, NULL),
('2024-12-01', '09:00:00', 3, NULL),
('2024-12-01', '09:30:00', 3, 2),
('2024-12-01', '10:00:00', 3, 6),
('2024-12-01', '10:30:00', 3, NULL),
('2024-12-02', '11:00:00', 3, 4),
('2024-12-02', '11:30:00', 3, NULL),
('2024-12-02', '12:00:00', 3, NULL),
('2024-12-02', '12:30:00', 3, NULL),
('2024-12-02', '13:00:00', 3, NULL),
('2024-12-01', '09:00:00', 1, NULL),
('2024-12-01', '09:30:00', 1, 2),
('2024-12-01', '10:00:00', 1, 3),
('2024-12-01', '10:30:00', 1, NULL),
('2024-12-01', '11:00:00', 1, 1),
('2024-12-01', '11:30:00', 1, 4),
('2024-12-01', '12:00:00', 1, NULL),
('2024-12-01', '12:30:00', 1, NULL),
('2024-12-01', '13:00:00', 1, NULL)
;