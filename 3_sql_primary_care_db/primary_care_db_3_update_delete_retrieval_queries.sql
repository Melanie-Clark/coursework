USE primary_care_db;

-- Demo queries to display all information for each table
-- SELECT * FROM patients;
-- SELECT * FROM titles;
-- SELECT * FROM addresses;
-- SELECT * FROM appointments;
-- SELECT * FROM staff_members;
-- SELECT * FROM staff_roles;

-- DELETE: Administrator Willing N-Able, turned out not to be very willing or able and has been fired
DELETE
FROM staff_members
WHERE staff_member_id = 5;

-- RESULTS CHECK
SELECT * FROM staff_members;

-- UPDATE: Patient cancels appointment
UPDATE appointments
SET patient_id = NULL
WHERE patient_id = 2
AND appointment_date = '2024-11-01'
AND appointment_time = '09:30';

-- RESULTS CHECK (Can also can be used to check results from queries 3 and 4 below)
SELECT a.appointment_date, a.appointment_time, sr.staff_role_description, sm.staff_member_forename, sm.staff_member_surname, p.patient_forename, p.patient_surname
FROM appointments a
LEFT JOIN staff_members sm
ON a.staff_member_id = sm.staff_member_id
LEFT JOIN staff_roles sr
ON sm.staff_member_role_id = sr.staff_role_id
LEFT JOIN patients p
ON a.patient_id = p.patient_id
ORDER BY appointment_date, sr.staff_role_description, sm.staff_member_surname;


-- 1a. Add Age to date_of_birth column for age queries
ALTER TABLE patients
ADD COLUMN age INT
AFTER date_of_birth;

UPDATE patients
SET age = TIMESTAMPDIFF(YEAR, date_of_birth, NOW());

-- 1b. All patients aged over 65 for vaccine invitation
SELECT patient_id, patient_forename, patient_surname, house_number_name, street, town_city, county, postcode, age
FROM patients p
JOIN addresses a
ON p.address_id = a.address_id
WHERE age >= 65
ORDER BY age DESC;

-- 1. RESULTS CHECK (Can only be run after 1a)
SELECT *
FROM patients
ORDER BY age DESC;


-- 2. Patients with the highest HbA1c result in the practice (May need an immediate referral for suspected pancreactic cancer).
-- ONLY the highest HbA1c across the practice is required, NOT all patients with a result over 80
SELECT p.patient_id, p.patient_forename, p.patient_surname, test, test_result
FROM medical_history mh
JOIN patients p
ON mh.patient_id = p.patient_id
WHERE test = 'HbA1c'
AND test_result IN (
	SELECT MAX(test_result) AS most_recent_hba1c_result
	FROM medical_history mh
	JOIN patients p
	ON mh.patient_id = p.patient_id
	WHERE test = 'HbA1c'
    AND test_result > 80
    )
ORDER BY patient_surname;

-- 2. RESULTS CHECK
SELECT *
FROM medical_history
ORDER BY test DESC, test_result DESC;


-- 3. Patients with active Diabetes (not resolved)
SELECT p.patient_id, p.patient_forename, p.patient_surname, diagnosis
FROM medical_history mh
JOIN patients p
ON mh.patient_id = p.patient_id
WHERE diagnosis LIKE 'Diabetes Type%'
AND mh.patient_id NOT IN (
	SELECT patient_id
	FROM medical_history
	WHERE diagnosis = 'Diabetes resolved'
	AND entry_date IN (
		SELECT MAX(entry_date) AS most_recent_diabetes_diagnosis
		FROM medical_history
		WHERE diagnosis LIKE 'Diabetes%'
		GROUP BY patient_id
        )
    )
GROUP BY mh.patient_id, patient_forename, patient_surname, diagnosis
ORDER BY mh.patient_id;

-- 3.RESULTS CHECK

SELECT patient_id, entry_date, diagnosis
FROM medical_history
ORDER BY patient_id;


-- 4. Number of booked appointments by Doctors and Nurses in November
SELECT sr.staff_role_description, sm.staff_member_surname, COUNT(patient_id) AS total_number_of_appointments
FROM appointments a
JOIN staff_members sm
ON a.staff_member_id = sm.staff_member_id
JOIN staff_roles sr
ON sm.staff_member_role_id = sr.staff_role_id
WHERE MONTH(appointment_date) = 11
GROUP BY sr.staff_role_description, sm.staff_member_surname
HAVING sr.staff_role_description = 'Doctor'
OR sr.staff_role_description = 'Nurse'
ORDER BY total_number_of_appointments DESC;


-- 5. Number of booked and total appointments, and % of booked appointments for Dr. Do Little in November (Dr. under investigation)
SELECT COUNT(patient_id) AS dr_little_booked_appointments, COUNT(*) AS dr_little_total_appointments, CONCAT(ROUND(((COUNT(patient_id) / COUNT(*)) * 100), 1), '%') AS percentage_of_dr_little_booked_appointments
FROM appointments a
JOIN staff_members sm
ON a.staff_member_id = sm.staff_member_id
JOIN staff_roles sr
ON sm.staff_member_role_id = sr.staff_role_id
WHERE MONTH(appointment_date) = 11
AND sm.staff_member_surname = 'Little';