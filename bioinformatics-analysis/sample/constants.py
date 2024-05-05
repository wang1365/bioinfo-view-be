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
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources",
    "data-meta.xlsx")

SAMPLE_TEMPLATE_EN_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources",
    "data-meta-en.xlsx")

SAMPLE_META_TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources",
    "sample-meta.xlsx")

SAMPLE_META_TEMPLATE_EN_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources",
    "sample-meta-en.xlsx")

FIELDS_OPERATORS = {
    (ValueType.date, SearchType.ranges): ['between'],
    (ValueType.bool, SearchType.exact): ['eq', 'ne'],
    (ValueType.string, SearchType.choices): ['in'],
    (ValueType.string, SearchType.exact): ['ne'],
    (ValueType.number, SearchType.exact):
    ['eq', 'ne', 'between', 'gt', 'gte', 'lt', 'lte'],
}

SAMPLE_META_MODEL_ATTRS = [
    {
        'key': 'sample_date',
        'name': '采样日期（YYYY-MM-DD）',
        'en_name': 'Sampling Date',
        'value_type': 'date',
        'search_type': SearchType.ranges
    },
    {
        'key': 'test_date',
        'name': '送测日期（YYYY-MM-DD）',
        'en_name': 'Submission Date',
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
        'en_name': 'Sampling Site',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'sample_type',
        'name': '样本类型',
        'en_name': 'Sample Type',
        'en_value_map': {
            'FFPE蜡块': 'FFPE',
            '新鲜组织': 'Fresh Tissue',
            '血液': 'Blood',
            '脑脊液': 'Cerebrospinal Fluid',
            '胸水': 'Pleural Effusion',
            '其他体液': 'Other Body Fluids',
            '骨髓': 'Bone Marrow',
        },
        'value_type': 'string',
        'search_type': SearchType.choices
    },
    {
        'key': 'panel_proportion',
        'name': '肿瘤含量',
        'en_name': 'Tumor Content',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'is_panel',
        'name': '肿瘤样本',
        'en_name': 'Tumor Sample',
        'value_type': 'bool',
        'search_type': SearchType.exact
    },
    {
        'key': 'patient_identifier',
        'name': '患者识别号',
        'en_name': 'Patient ID',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
]

SAMPLE_MODEL_ATTRS = [
    {
        'key': 'project_index',
        'name': '数据详情',
        'en_name': 'Data Details',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'library_number',
        'name': '文库编号',
        'en_name': 'Library Number',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'reagent_box',
        'name': '捕获试剂盒',  # 注意这里由于历史翻译原因,导致这里名称不一致
        'en_name': 'Capture Kit',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'nucleic_break_type',
        'name': '核酸打断方式',
        'en_name': 'Nucleic Acid Fragmentation Method',
        'value_type': 'string',
        'search_type': SearchType.exact,
    },
    {
        'key': 'library_input',
        'name': '建库input（ng）',
        'en_name': 'Library Construction Input(ng)',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'index_type',
        'name': 'index类型',
        'en_name': 'Index Type',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'index_number',
        'name': 'index编号',
        'en_name': 'Index Number',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'hybrid_input',
        'name': '杂交input',
        'en_name': 'Hybrid Input (ng)',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'risk',
        'name': '风险上机',
        'en_name': 'Risk Sequencing',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'nucleic_level',
        'name': '核酸降解等级',
        'en_name': 'Degradation Grade of Nucleic Acids',
        'value_type': 'string',
        'search_type': SearchType.choices
    },
    {
        'key': 'company',
        'name': '送检机构',
        'en_name': 'Submission Unit',
        'value_type': 'string',
        'search_type': SearchType.exact,
    },
    {
        'key': 'nucleic_type',
        'name': '核酸类型',
        'en_name': 'Type of Nucleic Acids',
        'value_type': 'string',
        'search_type': SearchType.choices
    },
    {
        'key': 'fastq1_path',
        'name': 'R1文件',
        'en_name': 'Data Name Of R1',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'fastq2_path',
        'name': 'R2文件',
        'en_name': 'Data Name Of R2',
        'value_type': 'string',
        'search_type': SearchType.not_support
    },
    {
        'key': 'sample_identifier',
        'name': '样本识别号',
        'en_name': 'Sample Identification Number',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
]
