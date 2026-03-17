# 需求变更汇总（2025 年 12 月之后）

基于 Git 提交记录对 `v4.4` 分支在 **2025-12-01（含）之后**的变更进行汇总，用于需求变更回顾/测试回归范围确认。

- 分支：`v4.4`
- 时间范围：`2025-12-01` ~ `现在`
- 统计口径：`git log v4.4 --since=2025-12-01 --no-merges`
- 提交数量（不含 merge）：4

## 变更概览

### 1) 流程检索：移除 `location` 字段模糊搜索

- 变更内容：流程列表搜索字段 `FlowFilters.SEARCH_FIELDS` 中移除 `location`
- 影响范围：
  - 依赖流程搜索的前端/调用方，如果仍按 `location` 进行 keyword 检索，将不再命中
  - 搜索字段缩小后，返回结果可能减少，但查询更准确、也避免对非预期字段的扫描
- 关联提交：
  - `2026-01-25 fa7c401 fix: 从FlowFilters搜索字段中移除'location'`
- 关键文件：
  - [flow/filters.py](file:///d:/private_code/naangda/bioinfo-view-be/bioinformatics-analysis/flow/filters.py)
  - [test_flow_filter.py](file:///d:/private_code/naangda/bioinfo-view-be/bioinformatics-analysis/test_flow_filter.py)

### 2) 队列分析（cohort）：后台扫描任务的周期调整 & 日志体系替换

- 变更内容：
  - 调整检查队列任务的间隔时间与函数命名（定时任务仍为 interval 触发）
  - 将 `print` 输出替换为 `loguru` 日志记录
- 影响范围：
  - cohort 解析任务的执行频率变化，可能影响入库延迟与系统负载曲线
  - 日志由 stdout 改为 loguru，日志聚合/检索方式可能随环境配置变化
- 关联提交：
  - `2025-12-20 85b6dbd refactor(cohort): 调整检查队列任务的间隔时间并重命名函数`
  - `2025-12-20 0b256c6 refactor(cohort): 替换print为loguru日志记录并调整检查间隔`
- 关键文件：
  - [cohort/job.py](file:///d:/private_code/naangda/bioinfo-view-be/bioinformatics-analysis/cohort/job.py)

### 3) 数据库连接：增加连接保活与连接复用配置

- 变更内容：在 dev/uat/prod 环境的数据库配置中加入连接复用与 TCP keepalive/timeout 等参数
- 预期收益：
  - 减少短连接频繁建立带来的开销
  - 降低长时间空闲连接被中间设备回收导致的偶发断连
- 风险点：
  - 连接复用时间过长可能放大“脏连接/网络抖动”带来的影响，需要结合部署环境观察
- 关联提交：
  - `2025-12-20 0d69233 perf(数据库配置): 添加数据库连接池和保活配置以优化性能`
- 关键文件：
  - [dev.py](file:///d:/private_code/naangda/bioinfo-view-be/bioinformatics-analysis/bioinformatics/settings/dev.py)
  - [uat.py](file:///d:/private_code/naangda/bioinfo-view-be/bioinformatics-analysis/bioinformatics/settings/uat.py)
  - [prod.py](file:///d:/private_code/naangda/bioinfo-view-be/bioinformatics-analysis/bioinformatics/settings/prod.py)

## 提交清单（2025-12-01 之后，不含 merge）

- 2026-01-25 fa7c401 fix: 从FlowFilters搜索字段中移除'location'
  - M bioinformatics-analysis/flow/filters.py
  - A bioinformatics-analysis/test_flow_filter.py
- 2025-12-20 0b256c6 refactor(cohort): 替换print为loguru日志记录并调整检查间隔
  - M bioinformatics-analysis/cohort/job.py
- 2025-12-20 85b6dbd refactor(cohort): 调整检查队列任务的间隔时间并重命名函数
  - M bioinformatics-analysis/cohort/job.py
- 2025-12-20 0d69233 perf(数据库配置): 添加数据库连接池和保活配置以优化性能
  - M bioinformatics-analysis/bioinformatics/settings/dev.py
  - M bioinformatics-analysis/bioinformatics/settings/uat.py
  - M bioinformatics-analysis/bioinformatics/settings/prod.py

## 建议回归点

- 流程列表搜索：使用 keyword 搜索，确认不再使用/依赖 `location` 字段命中
- cohort 定时任务：观察任务状态从 todo -> done 的链路是否按预期运行；检查日志输出位置与格式
- 数据库连接：在 dev/uat 环境进行基本接口压测或长时间空闲后访问，确认无频繁断连与异常堆积

