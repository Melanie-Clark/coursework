# Assignment Three

The **primary care database** is used for storing patient and staff details, appointments and basic medical history. 
The database contains fictious data.

The .sql files should be run in the following order:
 
## 1. Database creation:
Creation and population of a primary care database.
 
## 2. Stored procedure - New patient registration:
A new patient registers at a GP practice. 
- The patient is added to the patients table. If the address doesn't exist in the `addresses` table, it's then also added.
- The earliest available appointment is automatically booked with the Nurse.\
If no appointments are available, a message is displayed.
 
## 3. Delete, update and retrieval queries:
- A member of staff _(Miss Willing N-Able)_ has been fired for not being very willing or able - Staff member is **deleted** from `staff_members` table.
- A patient cancels an appointment - Appointment table is **updated**.
 
### Retrieval queries:
1.	All patients aged over 65 _(required for a vaccine invitation)_
2.	Patients with the highest HbA1c in the practice _(required for a possible review for potential referral)_
3.	All patients with active diabetes _(excluding patients where diabetes has now been resolved)_
4.	Number of booked appointments in November for all doctors and nurses
5.	Number of booked and total appointments, and % of booked appointments for Dr. Do Little in November _(Dr. is under investigation)_


## Requirements
The following have been used across the three files:
 
**Data Types**:
- INT
- VARCHAR
- DATE
- TIME

**Constraints (not pk, fk)**:
- NOT NULL
- UNIQUE

**Aggregate Functions**:
- MIN
- MAX
- COUNT

**In-built functions**
- CONCAT
- DATE
- TIME
- DAYNAME
- TIMESTAMPDIFF
