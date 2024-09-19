alter table task
	add samples_first jsonb  null,
	add samples_second jsonb null;

alter table task_sample
	add create_time_timestamp integer generated always as (EXTRACT(epoch FROM (create_time AT TIME ZONE 'UTC'::text))) stored;

alter table task_sample
	add update_time_timestamp integer generated always as (EXTRACT(epoch FROM (create_time AT TIME ZONE 'UTC'::text))) stored;

-- config增加字符串类型配置字段，方便保存各类配置
alter table config
    add data varchar(1000);

-- 2024.05.09 删除字段约束, 不需要>0的限制
alter table account
    drop constraint account_disk_limit_check,
    drop constraint account_used_disk_check;

-- 2024.09.08 添加字段, 支持样本数据合并
ALTER TABLE "samples"
    ADD COLUMN "fastq1_path_list"     varchar(1024) DEFAULT ''    NULL,
    ADD COLUMN "fastq2_path_list"     varchar(1024) DEFAULT ''    NULL,
    ADD COLUMN "fastq_merge_required" boolean       DEFAULT false NOT NULL;
