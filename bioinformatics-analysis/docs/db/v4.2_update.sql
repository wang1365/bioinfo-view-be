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

-- 用户诊断表
create table verdict
(
    id                 integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    patient_identifier varchar(100),
    gene_identifier    varchar(100),
    result             jsonb,
    created_at         timestamp not null,
    is_deleted         smallint default 0,
    deleted_at         timestamp,
    constraint unique_patient_gene  unique (patient_identifier, gene_identifier)
);

comment on table verdict is '用户诊断';
comment on column verdict.patient_identifier is '患者识别号';
comment on column verdict.gene_identifier is '基因标识';
comment on column verdict.result is '诊断结果';
comment on column verdict.created_at is '创建时间';
comment on column verdict.is_deleted is '删除标识';
comment on column verdict.deleted_at is '删除时间';

-- 任务表增加字段：cohort状态
alter table task add cohort_status varchar(100) default 'todo' not null;

create table cohort
(
    id          integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    gene_info   varchar(1000) default ''::character varying,
    panel_id    integer,
    task_id     integer,
    user_id     integer       not null,
    create_time timestamp     default CURRENT_TIMESTAMP not null,
    del_flag    integer       default 0
);
comment on table cohort is '队列分析数据表';
comment on column cohort.gene_info is '参考序列';
comment on column cohort.panel_id is 'panel名称';
comment on column cohort.task_id is '关联任务ID';
comment on column cohort.user_id is '用户ID';
comment on column cohort.create_time is '创建时间';
comment on column cohort.del_flag is '删除标识(0-未删除,非0-已删除)';
create index cohort_task_id_index on cohort (task_id);