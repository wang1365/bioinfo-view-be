#!/usr/bin/env python3


class SearchType:
    ranges = 'range'
    choices = 'choices'
    exact = 'exact'
    not_support = 'not_support'


class ValueType:
    date = 'date'
    string = 'string'
    number = 'number'


FIELDS_OPERATORS = {
    (ValueType.date, SearchType.ranges): ['between'],
    (ValueType.string, SearchType.choices): ['in'],
    (ValueType.string, SearchType.exact): ['ne'],
    (ValueType.number, SearchType.exact):
    ['eq', 'ne', 'between', 'gt', 'gte', 'lt', 'lte'],
}

MODEL_ATTRS = [
    {
        'key': 'test_date',
        'name': '送测日期',
        'value_type': 'date',
        'search_type': SearchType.ranges
    },
    {
        'key': 'project_index',
        'name': '项目编码',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'platform',
        'name': '测序平台',
        'value_type': 'string',
        'search_type': SearchType.choices
    },
    {
        'key': 'company',
        'name': '测序公司',
        'value_type': 'string',
        'search_type': SearchType.choices,
    },
    {
        'key': 'test_type',
        'name': '测序类型',
        'value_type': 'string',
        'search_type': SearchType.choices
    },
    {
        'key': 'index_type',
        'name': 'index 类型',
        'value_type': 'string',
        'search_type': SearchType.choices
    },
    {
        'key': 'origin_sample_info',
        'name': '原始样本信息',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'sample_orginization',
        'name': '样本类型1',
        'value_type': 'string',
        'search_type': SearchType.choices
    },
    {
        'key': 'sample_type',
        'name': '样本类型2',
        'value_type': 'string',
        'search_type': SearchType.choices
    },
    {
        'key': 'library_type',
        'name': '文库编号',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'prob_content',
        'name': '探针内容',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'pooling_library',
        'name': '杂交文库',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'index_number',
        'name': 'index编号',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'barocode_1',
        'name': 'Barocode 2/i7',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'barocode_2',
        'name': 'Barocode1/i7',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'sequence_size',
        'name': '测序量（G）',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'real_size',
        'name': '实际数据量（G）',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'quality_30',
        'name': 'Q30（%）',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'analysis_type',
        'name': '分析类型',
        'value_type': 'string',
        'search_type': SearchType.choices
    },
    {
        'key': 'building_library_type',
        'name': '建库方式',
        'value_type': 'string',
        'search_type': SearchType.choices
    },
    {
        'key': 'break_type',
        'name': '打断方式',
        'value_type': 'string',
        'search_type': SearchType.choices
    },
    {
        'key': 'circle_numbers',
        'name': '循环数',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'fastq1_path',
        'name': 'fastq1 文件地址',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'fastq2_path',
        'name': 'fastq2 文件地址',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'bam1_path',
        'name': 'bam1 文件地址',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'bam1_tool',
        'name': 'bam1 比对软件',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'bam2_path',
        'name': 'bam2 文件地址',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'bam2_tool',
        'name': 'bam2 比对软件',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'user_id',
        'alias': 'name',
        'name': '测序发起人',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'standard_code',
        'name': '标准品',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'backup1',
        'name': 'backup1',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'backup2',
        'name': 'backup2',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'backup3',
        'name': 'backup3',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'backup4',
        'name': 'backup4',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'backup5',
        'name': 'backup5',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'backup6',
        'name': 'backup6',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'backup7',
        'name': 'backup7',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'backup8',
        'name': 'backup8',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'backup9',
        'name': 'backup9',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'backup10',
        'name': 'backup10',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
]

TITLES = [
    "送测日期",
    "项目编码",
    "测序平台",
    "测序公司",
    "测序类型",
    "index类型",
    "原始样本信息",
    "样本类型1",
    "样本类型2",
    "文库编号",
    "探针内容",
    "杂交文库",
    "index编号",
    "Barocode2/i7",
    "Barocode1/i7",
    "测序量（G）",
    "实际数据量（G）",
    "Q30（%）",
    "分析类型",
    "建库方式",
    "打断方式",
    "循环数",
    "fastq1文件地址",
    "fastq2文件地址",
    "bam1文件地址",
    "bam1比对软件",
    "bam2文件地址",
    "bam2比对软件",
    "测序发起人",
    "标准品",
    "backup1",
    "backup2",
    "backup3",
    "backup4",
    "backup5",
    "backup6",
    "backup7",
    "backup8",
    "backup9",
    "backup10",
]
