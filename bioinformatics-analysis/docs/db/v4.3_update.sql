-- 任务表新增cdc相关流程的任务参数
ALTER TABLE "task" ADD COLUMN "cdc_parameter" jsonb DEFAULT '{}'::jsonb NULL;

-- 为task_sample表添加custom_name字段
ALTER TABLE task_sample ADD COLUMN custom_name VARCHAR(255);

-- 为task_sample表添加sampling_rate字段
ALTER TABLE task_sample ADD COLUMN sampling_rate DOUBLE PRECISION;

ALTER TABLE flow ADD COLUMN support_custom_sample_name BOOLEAN NOT NULL DEFAULT FALSE;

-- 为flow表添加support_sample_ratio字段
ALTER TABLE flow ADD COLUMN support_sample_ratio BOOLEAN NOT NULL DEFAULT FALSE;