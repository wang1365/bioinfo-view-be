import os

PATIENT_ZH_TO_EN = {
    "患者识别号": "identifier",
    "送检机构": "inspection_agency",
    "年龄": "age",
    "诊疗医生": "medical_doctor",
    "性别": "gender",
    "姓名": "name",
    "出生日期": "birthday",
    "身份证": "id_card",
    "家庭地址": "location",
    "临床诊断": "diagnosis",
    "遗传病": "disease",
    "家族史": "family_history",
    "用药史": "medication_history",
    "治疗史": "treatment_history",
    "预后时间": "prognosis_time",
    "复发时间": "recurrence_time",
    "存活时间": "survival_time",
    "肿瘤分期": "tumor_stage",
}


class SearchType:
    ranges = 'range'
    choices = 'choices'
    exact = 'exact'
    not_support = 'not_support'

PATIENT_MODEL_ATTRS_MAP = {
    "Name": "姓名",
    "Gender": "性别",
    "Date of Birth": "出生日期",
    "ID card": "身份证",
    "Home Address": "家庭地址",
    "Submission Unit": "送检机构",
    "Treating Physician": "诊疗医生",
    "Clinical Diagnosis": "临床诊断",
    "Tumor Staging": "肿瘤分期",
    "Genetic Disease": "遗传病",
    "Family History": "家族史",
    "Grug Using History": "用药史",
    "Smoking": "吸烟",
    "Alcohol Drinking": "饮酒",
    "Viral Infection": "病毒感染",
    "Treatment History": "治疗史",
    "Prognosis Information": "预后信息",
    "Prognosis Time(day)": "预后时间（天）",
    "Time of Recurrence(day)": "复发时间（天）",
    "Survival Time(day)": "存活时间（天）",
}

PATIENT_MODEL_ATTRS = [
    {
        'key': 'id',
        'name': '患者Id',
        'value_type': 'string',
        'search_type': SearchType.exact,
    },
    {
        'key': 'name',
        'name': '姓名',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'medication_history',
        'name': '用药史',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'gender',
        'name': '性别',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'prognosis_time',
        'name': '预后时间（天）',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'birthday',
        'name': '出生日期',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'age',
        'name': '年龄',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'id_card',
        'name': '身份证',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'location',
        'name': '家庭地址',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'identifier',
        'name': '患者识别号',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'inspection_agency',
        'name': '送检机构',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'medical_doctor',
        'name': '诊疗医生',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'diagnosis',
        'name': '临床诊断',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'tumor_stage',
        'name': '肿瘤分期',
        'value_type': 'string',
        'search_type': SearchType.exact,
    },
    {
        'key': 'disease',
        'name': '遗传病',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'family_history',
        'name': '家族史',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'treatment_history',
        'name': '治疗史',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'smoking',
        'name': '吸烟',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'drinking',
        'name': '饮酒',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'viral_infection',
        'name': '病毒感染',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'prognosis',
        'name': '预后信息',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'diagnosis_time',
        'name': '诊断时间（天）',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'recurrence_time',
        'name': '复发时间（天）',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
    {
        'key': 'survival_time',
        'name': '存活时间（天）',
        'value_type': 'string',
        'search_type': SearchType.exact
    },
]

PATIENT_META_TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "resources",
    "patient-meta.xlsx"
)

PATIENT_META_TEMPLATE_EN_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "resources",
    "patient-meta-en.xlsx"
)