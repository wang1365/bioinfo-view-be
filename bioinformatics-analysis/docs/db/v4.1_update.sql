-- 2024.12.31 患者新增字段
ALTER TABLE public.patient_patient ADD gestation varchar(128) NULL;
COMMENT ON COLUMN public.patient_patient.gestation IS '妊娠期';
ALTER TABLE public.patient_patient ADD pregnancy_status varchar(128) NULL;
COMMENT ON COLUMN public.patient_patient.pregnancy_status IS '怀孕状态';

-- 2024.12.31 样本新增字段
ALTER TABLE public.sample_meta ADD sampling_tube_brand varchar(128) NULL;
COMMENT ON COLUMN public.sample_meta.sampling_tube_brand IS '采样管品牌';
ALTER TABLE public.sample_meta ADD specimen_type varchar(128) NULL;
COMMENT ON COLUMN public.sample_meta.specimen_type IS '标本类型';


alter table flow add config jsonb default '{"taskLimit": 99999}'::jsonb;

