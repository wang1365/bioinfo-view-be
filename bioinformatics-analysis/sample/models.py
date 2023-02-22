from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import DO_NOTHING

from account.models import Account
from patient.models import Patient


class SampleMeta(models.Model):
    """样本元信息."""

    # 采样日期
    sample_date = models.DateField()

    # 送测日期
    test_date = models.DateField()

    # 采样部位
    sample_componet = models.CharField(max_length=128)

    # 样本类型
    sample_type = models.CharField(max_length=128)

    # 肿瘤含量
    panel_proportion = models.FloatField(default=0.0)

    # 肿瘤样本
    is_panel = models.BooleanField(default=False)

    # 样本所有者
    user = models.ForeignKey(to=Account, on_delete=models.CASCADE, blank=True, null=True)

    # 患者 ID
    patient = models.ForeignKey(to=Patient,
                                null=True,
                                db_constraint=False,
                                default=None,
                                on_delete=DO_NOTHING)

    # 患者识别号
    patient_identifier = models.CharField(max_length=256, null=True)

    # 样本识别号
    identifier = models.CharField(max_length=256, unique=True)

    create_time = models.DateTimeField(null=True,
                                       blank=True,
                                       auto_now_add=True)
    modify_time = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        db_table = "sample_meta"
        ordering = ["-id"]
        verbose_name = "样本"
        verbose_name_plural = verbose_name
        get_latest_by = "id"

    @property
    def username(self):
        try:
            account = Account.objects.get(id=self.user_id)
            return account.username
        except ObjectDoesNotExist:
            return ""


class Sample(models.Model):
    """样本数据."""

    class NucleicLevelChoices(models.TextChoices):
        A = "A", "A"
        B = "B", "B"
        C = "C", "C"
        D = "D", "D"

    class NucleicTypeChoices(models.TextChoices):
        GDNA = "gDNA", "gDNA"
        CFDNA = "cfDNA", "cfDNA"
        RNA = "RNA", "RNA"

    # 项目编码
    project_index = models.CharField(max_length=1024, blank=True, default='')

    # 文库编号
    library_number = models.CharField(max_length=1024, blank=True, default='')

    # 捕获试剂盒
    reagent_box = models.CharField(max_length=128)

    # 核酸打断方式
    nucleic_break_type = models.CharField(max_length=128)

    # 建库input
    library_input = models.CharField(max_length=128)

    # index 类型
    index_type = models.CharField(max_length=1024, blank=True, default='')

    # index 编号
    index_number = models.CharField(max_length=1024, blank=True, default='')

    # 杂交 input
    hybrid_input = models.CharField(max_length=1024, blank=True, default='')

    # 风险上机
    risk = models.BooleanField()

    # 核酸降解等级
    nucleic_level = models.CharField(max_length=4,
                                     choices=NucleicLevelChoices.choices)

    # 样本元信息 ID
    sample_meta = models.ForeignKey(to=SampleMeta,
                                    null=True,
                                    db_constraint=False,
                                    default=None,
                                    on_delete=DO_NOTHING)

    # 样本识别号
    sample_identifier = models.CharField(max_length=256)

    # 数据识别号
    identifier = models.CharField(max_length=256, unique=True)

    # 送检机构
    company = models.CharField(max_length=1024)

    # 核酸类型
    nucleic_type = models.CharField(max_length=16,
                                    choices=NucleicTypeChoices.choices)

    # R1 / R2 数据名称
    fastq1_path = models.CharField(max_length=1024)
    fastq2_path = models.CharField(max_length=1024)

    # 样本所有者
    user = models.ForeignKey(to=Account, on_delete=models.CASCADE, blank=True, null=True)

    create_time = models.DateTimeField(null=True,
                                       blank=True,
                                       auto_now_add=True)
    modify_time = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        db_table = "samples"
        ordering = ["-id"]
        verbose_name = "样本数据"
        verbose_name_plural = verbose_name
        get_latest_by = "id"
