-- 任务表新增cdc相关流程的任务参数
ALTER TABLE "task" ADD COLUMN "cdc_parameter" jsonb DEFAULT '{}'::jsonb NULL;