-- 自建参考基因组表的PostgreSQL建表语句
-- 基于Django模型 ReferenceGenome 生成 (更新版本 - 允许部分字段为空)

CREATE TABLE reference_genome (
    -- 主键ID (Django自动生成的AutoField)
    id SERIAL PRIMARY KEY,
    
    -- 自定义数据库名
    custom_database VARCHAR(255) NOT NULL,
    
    -- 病毒种名 (JSON格式)
    virus_name JSONB NOT NULL DEFAULT '{}',
    
    -- 病毒分型 (JSON格式)
    virus_type JSONB NOT NULL DEFAULT '{}',
    
    -- 宿主
    host VARCHAR(255) NOT NULL,
    
    -- 宿主基因组版本
    host_genome_version VARCHAR(255) NOT NULL,
    
    -- 宿主原序列文件路径 (允许为空)
    host_seq_file VARCHAR(500),
    
    -- 病原原序列文件路径 (允许为空)
    virus_seq_file VARCHAR(500),
    
    -- 宿主原序列信息 (JSON格式，允许为空)
    host_info JSONB DEFAULT '{}',
    
    -- 病原原序列信息 (JSON格式，允许为空)
    virus_info JSONB DEFAULT '{}',
    
    -- 创建时间
    create_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- 更新时间
    update_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- 软删除标识
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- 创建者外键 (关联到account_account表)
    creator_id INTEGER REFERENCES account_account(id) ON DELETE CASCADE
);

-- 创建索引以提高查询性能
CREATE INDEX idx_reference_genome_creator_id ON reference_genome(creator_id);
CREATE INDEX idx_reference_genome_create_time ON reference_genome(create_time DESC);
CREATE INDEX idx_reference_genome_is_deleted ON reference_genome(is_deleted);
CREATE INDEX idx_reference_genome_custom_database ON reference_genome(custom_database);
CREATE INDEX idx_reference_genome_host ON reference_genome(host);

-- 为JSON字段创建GIN索引以提高JSON查询性能
CREATE INDEX idx_reference_genome_virus_name_gin ON reference_genome USING GIN(virus_name);
CREATE INDEX idx_reference_genome_virus_type_gin ON reference_genome USING GIN(virus_type);
CREATE INDEX idx_reference_genome_host_info_gin ON reference_genome USING GIN(host_info);
CREATE INDEX idx_reference_genome_virus_info_gin ON reference_genome USING GIN(virus_info);

-- 添加表注释
COMMENT ON TABLE reference_genome IS '自建参考基因组表';
COMMENT ON COLUMN reference_genome.id IS '主键ID';
COMMENT ON COLUMN reference_genome.custom_database IS '自定义数据库名称';
COMMENT ON COLUMN reference_genome.virus_name IS '病毒种名信息，JSON格式';
COMMENT ON COLUMN reference_genome.virus_type IS '病毒分型信息，JSON格式';
COMMENT ON COLUMN reference_genome.host IS '宿主信息';
COMMENT ON COLUMN reference_genome.host_genome_version IS '宿主基因组版本信息';
COMMENT ON COLUMN reference_genome.host_seq_file IS '宿主原序列文件路径（可为空）';
COMMENT ON COLUMN reference_genome.virus_seq_file IS '病原原序列文件路径（可为空）';
COMMENT ON COLUMN reference_genome.host_info IS '宿主原序列详细信息，JSON格式（可为空）';
COMMENT ON COLUMN reference_genome.virus_info IS '病原原序列详细信息，JSON格式（可为空）';
COMMENT ON COLUMN reference_genome.create_time IS '创建时间';
COMMENT ON COLUMN reference_genome.update_time IS '修改时间';
COMMENT ON COLUMN reference_genome.is_deleted IS '软删除标识，TRUE表示已删除';
COMMENT ON COLUMN reference_genome.creator_id IS '创建者ID，关联account_account表';

-- 创建更新时间自动更新的触发器
CREATE OR REPLACE FUNCTION update_reference_genome_update_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_time = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_reference_genome_update_time
    BEFORE UPDATE ON reference_genome
    FOR EACH ROW
    EXECUTE FUNCTION update_reference_genome_update_time();