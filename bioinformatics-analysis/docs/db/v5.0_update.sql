-- 样本管理（sample_meta）新增字段：NC样本、Tag标签

ALTER TABLE sample_meta
    ADD COLUMN IF NOT EXISTS is_nc_sample BOOLEAN DEFAULT NULL;
COMMENT ON COLUMN sample_meta.is_nc_sample IS 'NC样本';

ALTER TABLE sample_meta
    ADD COLUMN IF NOT EXISTS tag_label TEXT DEFAULT NULL;
COMMENT ON COLUMN sample_meta.tag_label IS 'Tag标签';

