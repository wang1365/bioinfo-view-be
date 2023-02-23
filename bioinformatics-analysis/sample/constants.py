#!/usr/bin/env python3
import os


class SearchType:
    ranges = 'range'
    choices = 'choices'
    exact = 'exact'
    not_support = 'not_support'


class ValueType:
    date = 'date'
    bool = 'bool'
    string = 'string'
    number = 'number'


SAMPLE_TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "resources",
    "data-meta.xlsx"
)
SAMPLE_META_TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "resources",
    "sample-meta.xlsx"
)


FIELDS_OPERATORS = {
    (ValueType.date, SearchType.ranges): ['between'],
    (ValueType.bool, SearchType.exact): ['eq', 'ne'],
    (ValueType.string, SearchType.choices): ['in'],
    (ValueType.string, SearchType.exact): ['ne'],
    (ValueType.number, SearchType.exact): ['eq', 'ne', 'between', 'gt', 'gte', 'lt', 'lte'],
}

SAMPLE_META_MODEL_ATTRS = [
    {
        'key': 'sample_date',
        'name': '采样日期（YYYY-MM-DD）',
        'value_type': 'date',
        'search_type': SearchType.ranges
    },
    {
        'key': 'test_date',
        'name': '送测日期（YYYY-MM-DD）',
        'value_type': 'date',
        'search_type': SearchType.ranges
    },
    # {
    #     'key': 'project_index',
    #     'name': '项目编码',
    #     'value_type': 'string',
    #     'search_type': SearchType.exact
    # },
    {
        'key': 'sample_componet',
        'name': '采样部位',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'sample_type',
        'name': '样本类型',
        'value_type': 'string',
        'search_type': SearchType.choices
    },
    {
        'key': 'panel_proportion',
        'name': '肿瘤含量',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'is_panel',
        'name': '肿瘤样本',
        'value_type': 'bool',
        'search_type': SearchType.exact
    },
    {
        'key': 'patient_identifier',
        'name': '患者识别号',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
]

SAMPLE_MODEL_ATTRS = [
    {
        'key': 'project_index',
        'name': '数据详情',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'library_number',
        'name': '文库编号',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'reagent_box',
        'name': '捕获试剂盒',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'nucleic_break_type',
        'name': '核酸打断方式',
        'value_type': 'string',
        'search_type': SearchType.exact,
    },
    {
        'key': 'library_input',
        'name': '建库input（ng）',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'index_type',
        'name': 'index类型',
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
        'key': 'hybrid_input',
        'name': '杂交input',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'risk',
        'name': '风险上机',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'nucleic_level',
        'name': '核酸降解等级',
        'value_type': 'string',
        'search_type': SearchType.choices
    },
    {
        'key': 'company',
        'name': '送检机构',
        'value_type': 'string',
        'search_type': SearchType.exact,
    },
    {
        'key': 'nucleic_type',
        'name': '核酸类型',
        'value_type': 'string',
        'search_type': SearchType.choices
    },
    {
        'key': 'fastq1_path',
        'name': 'R1文件',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'fastq2_path',
        'name': 'R2文件',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'sample_identifier',
        'name': '样本识别号',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
]

