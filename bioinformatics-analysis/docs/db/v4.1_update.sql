-- 2024.12.31 患者新增字段
ALTER TABLE public.patient_patient ADD gestation varchar(128) NULL;
COMMENT ON COLUMN public.patient_patient.gestation IS '妊娠期';
ALTER TABLE public.patient_patient ADD pregnancy_status varchar(128) NULL;
COMMENT ON COLUMN public.patient_patient.pregnancy_status IS '怀孕状态';
