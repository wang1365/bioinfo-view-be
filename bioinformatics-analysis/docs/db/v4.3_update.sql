
-- 用户诊断表
create table verdict
(
    id                 integer  default nextval('diagnosis_id_seq'::regclass) not null primary key,
    patient_identifier varchar(100),
    gene_identifier    varchar(100),
    result             jsonb,
    created_at         timestamp  not null,
    is_deleted         smallint default 0,
    deleted_at         timestamp,
    constraint unique_patient_gene unique (patient_identifier, gene_identifier)
);

comment on table verdict is '用户诊断';
comment on column verdict.patient_identifier is '患者识别号';
comment on column verdict.gene_identifier is '基因标识';
comment on column verdict.result is '诊断结果';
comment on column verdict.created_at is '创建时间';
comment on column verdict.is_deleted is '删除标识';
comment on column verdict.deleted_at is '删除时间';


alter table task add cohort_status varchar(100) default 'todo' not null;


CREATE TABLE cohort (
    id SERIAL PRIMARY KEY,
    ref_gene VARCHAR(255) DEFAULT '',
    chr VARCHAR(50) DEFAULT '',
    chr_start VARCHAR(50) DEFAULT '',
    chr_end VARCHAR(50) DEFAULT '',
    ref VARCHAR(255) DEFAULT '',
    alt VARCHAR(255) DEFAULT '',
    count INTEGER NOT NULL DEFAULT 0,
    panel VARCHAR(255) DEFAULT '',
    task_id INTEGER NULL,
    user_id INTEGER NOT NULL,
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    del_flag INTEGER DEFAULT 0
);

COMMENT ON TABLE cohort IS '队列分析数据表';
COMMENT ON COLUMN cohort.ref_gene IS '参考基因';
COMMENT ON COLUMN cohort.chr IS '染色体';
COMMENT ON COLUMN cohort.chr_start IS '起始位置';
COMMENT ON COLUMN cohort.chr_end IS '结束位置';
COMMENT ON COLUMN cohort.ref IS '参考序列';
COMMENT ON COLUMN cohort.alt IS '变异序列';
COMMENT ON COLUMN cohort.count IS '计数';
COMMENT ON COLUMN cohort.panel IS 'panel名称';
COMMENT ON COLUMN cohort.task_id IS '关联任务ID';
COMMENT ON COLUMN cohort.user_id IS '用户ID';
COMMENT ON COLUMN cohort.create_time IS '创建时间';
COMMENT ON COLUMN cohort.del_flag IS '删除标识(0-未删除,非0-已删除)';