from django.db import models
from django.utils.timezone import now

from account.models import Account

# Create your models here.

class Patient(models.Model):
    MALE = '男'
    FEMAIL = '女'
    UNKNOWN = '未知'
    GENDER = (
        (MALE, '男'),
        (FEMAIL, '女'),
        (UNKNOWN, '未知'),
    )
    TRUE = "是"
    FALSE = "否"
    BOOL = (
        (TRUE, "是"),
        (FALSE, "否"),
    )
    age = models.IntegerField(default=0, null=True, blank=True)
    birthday = models.DateField()
    name = models.CharField(max_length=256)
    id_card = models.CharField(max_length=32, unique=True)
    medical_doctor = models.CharField(max_length=128, null=True, blank=True)  # 诊疗医生
    gender = models.CharField(max_length=12, choices=GENDER, default=MALE)
    location = models.CharField(max_length=256, null=True, blank=True)
    identifier = models.CharField(max_length=256, unique=True)  # 患者识别号
    blood_type = models.CharField(max_length=256, blank=True, null=True)  # 血型
    inspection_agency = models.CharField(max_length=256, null=True, blank=True)  # 送检机构
    tumor_stage = models.CharField(max_length=256, null=True, blank=True)
    diagnosis = models.CharField(max_length=256, null=True, blank=True)  # 临床诊断
    disease = models.CharField(max_length=256, null=True, blank=True)  # 遗传病
    family_history = models.CharField(max_length=256, null=True, blank=True)  # 家族史
    medication_history = models.CharField(max_length=256, null=True, blank=True)  # 用药史
    smoking = models.CharField(max_length=16, default=False, choices=BOOL)  # 吸烟
    drinking = models.CharField(max_length=16, default=False, choices=BOOL) # 饮酒
    viral_infection = models.CharField(max_length=16, default=False, choices=BOOL)  # 病毒感染
    viral_result = models.CharField(max_length=256, default='')  # 病原培养鉴定结果
    viral_focus = models.CharField(max_length=256, default='')  # 重点关注病原
    treatment_history = models.CharField(max_length=256, null=True, blank=True)  # 治疗史
    prognosis = models.CharField(max_length=512, blank=True, null=True)  # 预后信息
    prognosis_time = models.IntegerField(default=0)  # 预后时间
    diagnosis_time = models.IntegerField(default=0)  # 诊断时间
    recurrence_time = models.IntegerField(default=0)  # 复发时间
    survival_time = models.IntegerField(default=0)  # 存活时间
    creator = models.ForeignKey(to=Account, on_delete=models.CASCADE, blank=True, null=True)
    create_time = models.DateTimeField("创建时间", default=now)
    update_time = models.DateTimeField("修改时间", auto_now=True)