create database medsecure360;
use  medsecure360;
RENAME TABLE medsecure360_with_tests TO med_source;



-- -------------------PATIENT TABLE

CREATE TABLE patient (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(10),
    blood_group VARCHAR(5),
    allergies VARCHAR(100),
    existing_conditions VARCHAR(100),
    insurance_provider VARCHAR(100),
    address TEXT,
    marital_status VARCHAR(20),
    is_insured BOOLEAN
);


-- ------------Insert data into patient table
INSERT INTO patient (
    first_name,
    last_name,
    email,
    phone_number,
    date_of_birth,
    gender,
    blood_group,
    allergies,
    existing_conditions,
    insurance_provider,
    address,
    marital_status,
    is_insured
)
SELECT
    First_Name,
    Last_Name,
    Email,
    Phone_Number,
    Date_of_Birth,
    Gender,
    Blood_Group,
    Allergies,
    Existing_Conditions,
    Insurance_Provider,
    Address,
    Marital_Status,
    CASE WHEN Is_Insured = 'Yes' THEN TRUE ELSE FALSE END
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY Email ORDER BY Date_of_Birth DESC) AS rn
    FROM med_source
) AS ranked
WHERE rn = 1;



-- --------------------DOCTOR table--------------
CREATE TABLE doctor (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    doctor_name VARCHAR(100),
    specialization VARCHAR(100),
    department VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(20)
);

-- --------------------Insert data into doctor table----------------
INSERT INTO doctor (
    doctor_name,
    specialization,
    department,
    email,
    phone_number
)
SELECT DISTINCT
    Doctor_Name,
    Specialization,
    Department,
    Doctor_Email,
    Doctor_Phone
FROM med_source;

-- --------------VISIT table--------------------
CREATE TABLE visit (
    visit_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT,
    doctor_id INT,
    visit_date DATE,
    reason TEXT,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id)
);

-- --------------insert data into visit table---------------------------
INSERT INTO visit (
    patient_id,
    doctor_id,
    visit_date,
    reason
)
SELECT
    p.patient_id,
    d.doctor_id,
    m.Visit_Date,
    m.Reason
FROM med_source m
JOIN patient p ON m.Email = p.email
JOIN doctor d ON m.Doctor_Email = d.email;

-- -------------------MEDICATION table--------------------------------

CREATE TABLE medication (
    medication_id INT PRIMARY KEY AUTO_INCREMENT,
    visit_id INT,
    medication_name VARCHAR(100),
    dosage VARCHAR(50),
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (visit_id) REFERENCES visit(visit_id)
);

-- --------------insert data into medication table---------------------------
INSERT INTO medication (
    visit_id,
    medication_name,
    dosage,
    start_date,
    end_date
)
SELECT
    v.visit_id,
    m.Medication_Name,
    m.Dosage,
    m.Start_Date,
    m.End_Date
FROM med_source m
JOIN patient p ON m.Email = p.email
JOIN doctor d ON m.Doctor_Email = d.email
JOIN visit v ON v.patient_id = p.patient_id
             AND v.doctor_id = d.doctor_id
             AND v.visit_date = m.Visit_Date;
   
-- ----------------VITALS table-----------------------------------
CREATE TABLE vitals (
    vital_id INT PRIMARY KEY AUTO_INCREMENT,
    visit_id INT,
    heart_rate INT,
    bp_systolic INT,
    bp_diastolic INT,
    spo2 INT,
    recorded_time DATETIME,
    FOREIGN KEY (visit_id) REFERENCES visit(visit_id)
);

-- --------------insert data into vitals table---------------------------
INSERT INTO vitals (
    visit_id,
    heart_rate,
    bp_systolic,
    bp_diastolic,
    spo2,
    recorded_time
)
SELECT
    v.visit_id,
    m.Heart_Rate,
    m.BP_Systolic,
    m.BP_Diastolic,
    m.SpO2,
    m.Recorded_Time
FROM med_source m
JOIN patient p ON m.Email = p.email
JOIN doctor d ON m.Doctor_Email = d.email
JOIN visit v ON v.patient_id = p.patient_id
             AND v.doctor_id = d.doctor_id
             AND v.visit_date = m.Visit_Date;
             
      
-- ---------------------------DIAGNOSTICS table---------------------------------
CREATE TABLE diagnostics (
    diagnostics_id INT PRIMARY KEY AUTO_INCREMENT,
    visit_id INT,
    test_name VARCHAR(100),
    test_result VARCHAR(100),
    FOREIGN KEY (visit_id) REFERENCES visit(visit_id)
);

-- --------------insert data into diagnotics table---------------------------
INSERT INTO diagnostics (
    visit_id,
    test_name,
    test_result
)
SELECT
    v.visit_id,
    m.Test_Name,
    m.Test_Result
FROM med_source m
JOIN patient p ON m.Email = p.email
JOIN doctor d ON m.Doctor_Email = d.email
JOIN visit v ON v.patient_id = p.patient_id
             AND v.doctor_id = d.doctor_id
             AND v.visit_date = m.Visit_Date;
  
-- -----------------------REPORTS-------------------------
 -- 1. Average Vitals per Department
SELECT 
    d.department,
    ROUND(AVG(vt.heart_rate), 1) AS avg_heart_rate,
    ROUND(AVG(vt.bp_systolic), 1) AS avg_bp_systolic,
    ROUND(AVG(vt.bp_diastolic), 1) AS avg_bp_diastolic,
    ROUND(AVG(vt.spo2), 1) AS avg_spo2
FROM vitals vt
JOIN visit vi ON vt.visit_id = vi.visit_id
JOIN doctor d ON vi.doctor_id = d.doctor_id
GROUP BY d.department
ORDER BY d.department;

-- 2. Patient Count by Department

SELECT 
    d.department,
    COUNT(DISTINCT vi.patient_id) AS total_patients
FROM visit vi
JOIN doctor d ON vi.doctor_id = d.doctor_id
GROUP BY d.department
ORDER BY total_patients DESC;

-- 3. Anomaly Identification
-- Let’s define basic thresholds (customize as needed):
-- Heart rate < 50 or > 120
-- Systolic BP > 140
-- Diastolic BP > 90
-- SpO₂ < 92

SELECT 
    p.first_name,
    p.last_name,
    p.email,
    d.department,
    vt.heart_rate,
    vt.bp_systolic,
    vt.bp_diastolic,
    vt.spo2,
    vt.recorded_time
FROM vitals vt
JOIN visit vi ON vt.visit_id = vi.visit_id
JOIN patient p ON vi.patient_id = p.patient_id
JOIN doctor d ON vi.doctor_id = d.doctor_id
WHERE 
    vt.heart_rate < 50 OR vt.heart_rate > 90 OR
    vt.bp_systolic >= 140 OR
    vt.bp_diastolic >= 90 OR
    vt.spo2 < 92
ORDER BY vt.recorded_time DESC;


