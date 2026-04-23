-- 样本管理（sample_meta）新增字段：NC样本

ALTER TABLE sample_meta
    ADD COLUMN IF NOT EXISTS is_nc_sample BOOLEAN DEFAULT NULL;
COMMENT ON COLUMN sample_meta.is_nc_sample IS 'NC样本';

-- 样本数据（samples）新增字段：Tag标签
ALTER TABLE samples
    ADD COLUMN IF NOT EXISTS tag_label TEXT DEFAULT NULL;
COMMENT ON COLUMN samples.tag_label IS 'Tag标签';

-- tag_label 从 sample_meta 迁移到 samples
UPDATE samples
SET tag_label = sample_meta.tag_label
FROM sample_meta
WHERE samples.sample_meta_id = sample_meta.id
  AND (samples.tag_label IS NULL OR samples.tag_label = '')
  AND sample_meta.tag_label IS NOT NULL
  AND sample_meta.tag_label <> '';

ALTER TABLE sample_meta
    DROP COLUMN IF EXISTS tag_label;


CREATE TABLE task_sample (
    id SERIAL PRIMARY KEY,
    create_time TIMESTAMP WITH TIME ZONE NOT NULL,
    update_time TIMESTAMP WITH TIME ZONE NOT NULL,
    sample_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL
);
COMMENT ON TABLE task_sample IS '任务样本关联表';

ALTER TABLE task_sample
    ADD CONSTRAINT task_sample_sample_id_task_id_key UNIQUE (sample_id, task_id);

-- RP2 task_sample 新增样本级自定义报告字段
ALTER TABLE task_sample
    ADD COLUMN IF NOT EXISTS custom_report_path_cn TEXT DEFAULT NULL;
COMMENT ON COLUMN task_sample.custom_report_path_cn IS 'RP2自定义报告CN路径';

ALTER TABLE task_sample
    ADD COLUMN IF NOT EXISTS custom_report_path_en TEXT DEFAULT NULL;
COMMENT ON COLUMN task_sample.custom_report_path_en IS 'RP2自定义报告EN路径';

ALTER TABLE task_sample
    ADD COLUMN IF NOT EXISTS active_report_type VARCHAR(32) DEFAULT 'default';
COMMENT ON COLUMN task_sample.active_report_type IS 'RP2当前生效报告类型(default/custom)';

ALTER TABLE task_sample
    ADD COLUMN IF NOT EXISTS custom_report_updated_at TIMESTAMP WITH TIME ZONE DEFAULT NULL;
COMMENT ON COLUMN task_sample.custom_report_updated_at IS 'RP2自定义报告最后更新时间';