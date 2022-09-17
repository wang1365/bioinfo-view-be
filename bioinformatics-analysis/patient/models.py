from django.db import models
from django.utils.timezone import now

from account.models import Account

# Create your models here.

class Patient(models.Model):
    MALE = 'male'
    FEMAIL = 'female'
    UNKNOWN = 'unknown'
    GENDER = (
        (MALE, 'male'),
        (FEMAIL, 'female'),
        (UNKNOWN, 'unknown'),
    )
    age = models.PositiveSmallIntegerField()
    birthday = models.DateField()
    name = models.CharField(max_length=256, null=True, blank=True)
    id_card = models.CharField(max_length=32, unique=True, null=True, blank=True)
    medical_doctor = models.CharField(max_length=128, null=True, blank=True)
    gender = models.CharField(max_length=12, choices=GENDER)
    location = models.CharField(max_length=256, null=True, blank=True)
    identifier = models.CharField(max_length=256, unique=True)  # 患者识别号
    inspection_agency = models.CharField(max_length=256, null=True, blank=True)  # 送检机构
    tumor_stage = models.CharField(max_length=256, null=True, blank=True)
    diagnosis = models.CharField(max_length=256, null=True, blank=True)  # 临床诊断
    disease = models.CharField(max_length=256, null=True, blank=True)  # 遗传病
    family_history = models.CharField(max_length=256, null=True, blank=True)  # 家族史
    medication_history = models.CharField(max_length=256, null=True, blank=True)  # 用药史
    treatment_history = models.CharField(max_length=256, null=True, blank=True)  # 治疗史
    creator = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    prognosis_time = models.IntegerField(default=0)  # 预后时间
    recurrence_time = models.IntegerField(default=0)  # 复发时间
    survival_time = models.IntegerField(default=0)  # 存活时间
    create_time = models.DateTimeField("创建时间", default=now)
    update_time = models.DateTimeField("修改时间", auto_now=True)