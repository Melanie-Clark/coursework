USE primary_care_db;

DROP PROCEDURE IF EXISTS new_patient_registration;
DROP FUNCTION IF EXISTS find_earliest_available_appointment;

-- Stored function to find earliest available appointment
DELIMITER //
CREATE FUNCTION find_earliest_available_appointment()
RETURNS DATETIME
DETERMINISTIC
BEGIN
	DECLARE earliest_date_time DATETIME;
	SELECT MIN(CONCAT(appointment_date, ' ', appointment_time)) AS earliest_appointment_date_time INTO earliest_date_time
	FROM appointments
	WHERE patient_id IS NULL AND staff_member_id = 2;
	RETURN earliest_date_time;
END //
DELIMITER ;

-- Stored procedure to register patient, add address (if new) and books earliest available appointment if available
DELIMITER //
CREATE PROCEDURE new_patient_registration(
	IN new_pt_title_description VARCHAR(20),
	IN patient_forename VARCHAR(40),
	IN patient_surname VARCHAR(40),
    IN new_pt_house_number_name INT,
	IN new_pt_street VARCHAR(200),
    IN new_pt_town_city VARCHAR(200),
    IN new_pt_county VARCHAR(200),
    IN new_pt_postcode VARCHAR(10),
    IN date_of_birth DATE,
	IN nhs_number VARCHAR(10),
    IN new_pt_staff_member_surname VARCHAR(40)
)
BEGIN

	-- Assigns id variables for INSERT statements below
    SELECT title_id INTO @new_pt_title_id
    FROM titles t
    WHERE title_description = new_pt_title_description;

    SELECT staff_member_id INTO @new_pt_staff_member_id
    FROM staff_members
    WHERE staff_member_surname = new_pt_staff_member_surname;

    SELECT address_id INTO @new_pt_address_id
    FROM addresses
    WHERE house_number_name = new_pt_house_number_name
    AND postcode = new_pt_postcode;

    -- Registers new patient
    INSERT IGNORE INTO patients (patient_title_id, patient_forename, patient_surname, address_id, date_of_birth, nhs_number, registered_gp_id)
	VALUES
	(@new_pt_title_id, patient_forename, patient_surname, @new_pt_address_id, date_of_birth, nhs_number, @new_pt_staff_member_id);

    -- If address (postcode and NHS number) doesn't already exist, add address to table
    INSERT IGNORE INTO addresses (house_number_name, street, town_city, county, postcode)
	VALUES
	(new_pt_house_number_name, new_pt_street, new_pt_town_city, new_pt_county, new_pt_postcode);

	-- Book new patient appointment with Nurse if available, otherwise displays no appointments
	IF find_earliest_available_appointment() IS NULL THEN
		SELECT CONCAT(
			new_pt_title_description, ' ', patient_forename, ' ', patient_surname, ' has been registered.',
            ' There are NO available Nurse appointments.',
            ' Advise patient to call back tomorrow to book an appointment.'
            ) AS message;
    ELSE
		-- Books earliest available appointment with Nurse for the patient
		SET @earliest_date = DATE(find_earliest_available_appointment());
		SET @earliest_time = TIME(find_earliest_available_appointment());

		SELECT CONCAT(
			new_pt_title_description, ' ', patient_forename, ' ', patient_surname,
			': The earliest available appointment with the Nurse is: ',
			DAYNAME(@earliest_date), ' ',
			find_earliest_available_appointment()
		) AS message;

		UPDATE appointments
		SET patient_id = LAST_INSERT_ID()
		WHERE appointment_date = @earliest_date
		AND appointment_time = @earliest_time
		AND staff_member_id = 2;

	END IF;

END//
DELIMITER ;


-- New patient registration
CALL new_patient_registration('Professor', 'Okie', 'Dokie', 10, 'Clever_Street', 'Oxford', 'Oxfordshire', 'OX01 1FO', '1964-05-01', 1237894560, 'Little');
CALL new_patient_registration('Ms', 'Kylie', 'Minogue', 40, NULL, NULL, NULL, 'AUS 1RA', '1972-03-03', 2223334445, 'Well');
CALL new_patient_registration('Miss', 'Julia', 'Roberts', 5, 'Love_Avenue', 'Notting Hill', 'London', 'HG01 2JR', '1968-08-08', 4444444444, 'Well');


-- RESULTS CHECK (PATIENT, ADDRESSES AND APPOINTMENT TABLES)
SELECT * FROM patients;
SELECT * FROM addresses;

SELECT a.appointment_date, a.appointment_time, sr.staff_role_description, sm.staff_member_forename, sm.staff_member_surname, p.patient_forename, p.patient_surname
FROM appointments a
LEFT JOIN staff_members sm
ON a.staff_member_id = sm.staff_member_id
LEFT JOIN staff_roles sr
ON sm.staff_member_role_id = sr.staff_role_id
LEFT JOIN patients p
ON a.patient_id = p.patient_id
ORDER BY sr.staff_role_description, sm.staff_member_surname, appointment_date, appointment_time;