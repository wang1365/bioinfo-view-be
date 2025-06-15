
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