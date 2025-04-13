--- 患者新增字段 2025 金域平台功能需求

ALTER TABLE patient
ADD COLUMN general_pathology_number VARCHAR(256) DEFAULT '' NULL;
COMMENT ON COLUMN patient.general_pathology_number IS '常规病理编号';

ALTER TABLE patient
ADD COLUMN molecular_pathology_number VARCHAR(256) DEFAULT '' NULL;
COMMENT ON COLUMN patient.molecular_pathology_number IS '分子病理编号';

ALTER TABLE patient
ADD COLUMN submitting_department VARCHAR(256) DEFAULT '' NULL;
COMMENT ON COLUMN patient.submitting_department IS '送检科室';

ALTER TABLE patient
ADD COLUMN patient_phone_number VARCHAR(256) DEFAULT '' NULL;
COMMENT ON COLUMN patient.patient_phone_number IS '患者电话';

ALTER TABLE patient
ADD COLUMN outpatient_or_inpatient_number VARCHAR(256) DEFAULT '' NULL;
COMMENT ON COLUMN patient.outpatient_or_inpatient_number IS '门诊/住院号';

ALTER TABLE patient
ADD COLUMN bed_number VARCHAR(256) DEFAULT '' NULL;
COMMENT ON COLUMN patient.bed_number IS '床号';