
-- config增加字符串类型配置字段，方便保存各类配置
alter table config add data varchar(1000);

-- 2024.05.09 删除字段约束, 不需要>0的限制
alter table account drop constraint account_disk_limit_check;
alter table account drop constraint account_used_disk_check;
