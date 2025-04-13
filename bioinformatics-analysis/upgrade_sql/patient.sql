--- 患者新增字段 2025 金域平台功能需求

ALTER TABLE patient_patient
ADD COLUMN general_pathology_number VARCHAR(256) DEFAULT '' NULL;
COMMENT ON COLUMN patient_patient.general_pathology_number IS '常规病理编号';

ALTER TABLE patient_patient
ADD COLUMN molecular_pathology_number VARCHAR(256) DEFAULT '' NULL;
COMMENT ON COLUMN patient_patient.molecular_pathology_number IS '分子病理编号';

ALTER TABLE patient_patient
ADD COLUMN submitting_department VARCHAR(256) DEFAULT '' NULL;
COMMENT ON COLUMN patient_patient.submitting_department IS '送检科室';

ALTER TABLE patient_patient
ADD COLUMN patient_phone_number VARCHAR(256) DEFAULT '' NULL;
COMMENT ON COLUMN patient_patient.patient_phone_number IS '患者电话';

ALTER TABLE patient_patient
ADD COLUMN outpatient_or_inpatient_number VARCHAR(256) DEFAULT '' NULL;
COMMENT ON COLUMN patient_patient.outpatient_or_inpatient_number IS '门诊/住院号';

ALTER TABLE patient_patient
ADD COLUMN bed_number VARCHAR(256) DEFAULT '' NULL;
COMMENT ON COLUMN patient_patient.bed_number IS '床号';