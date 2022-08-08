import os

from datetime import datetime
from django.db import models
from account.models import Account
from django.core.exceptions import ObjectDoesNotExist


class Sample(models.Model):
    # 送测日期
    test_date = models.DateField(default=datetime(1990, 1, 1))

    # 项目编码
    project_index = models.CharField(max_length=1024, blank=True, default='')

    # 测序平台
    platform = models.CharField(max_length=1024, blank=True, default='')

    # 测序公司
    company = models.CharField(max_length=1024, blank=True, default='')

    # 测序类型
    test_type = models.CharField(max_length=1024, blank=True, default='')

    # index 类型
    index_type = models.CharField(max_length=1024, default='')

    # 原始样本信息
    origin_sample_info = models.CharField(max_length=1024, default='')

    # 样本类型-01
    sample_orginization = models.CharField(max_length=1024,
                                           blank=True,
                                           default='')

    # 样本类型-02
    sample_type = models.CharField(max_length=1024, default='')

    # 文库编号
    library_type = models.CharField(max_length=256, default='')

    # 侦探内容
    prob_content = models.CharField(max_length=1024, default='')

    # Pooling 文库
    pooling_library = models.CharField(max_length=256, default='')

    # index 编号
    index_number = models.CharField(max_length=1024, default='')

    # barcode 1
    barocode_1 = models.CharField(max_length=1024, blank=True, default='')

    # barcode 2
    barocode_2 = models.CharField(max_length=1024, blank=True, default='')

    # 测序量
    sequence_size = models.DecimalField(max_digits=10,
                                        decimal_places=2,
                                        default=-1)

    # 实际数据量
    real_size = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    default=-1)

    # Q-30
    quality_30 = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     default=-1)

    # 分析类型
    analysis_type = models.CharField(max_length=1024, blank=True, default='')

    # 建库方式
    building_library_type = models.CharField(max_length=1024,
                                             blank=True,
                                             default='')

    # 打断方式
    break_type = models.CharField(max_length=1024, blank=True, default='')

    # 循环数
    circle_numbers = models.IntegerField(default=0)

    # fastq1_path
    fastq1_path = models.CharField(max_length=1024, blank=True, default='')

    # fastq2_path
    fastq2_path = models.CharField(max_length=1024, blank=True, default='')

    # bam1_path
    bam1_path = models.CharField(max_length=1024, blank=True, default='')

    # bam1_tool
    bam1_tool = models.CharField(max_length=1024, blank=True, default='')

    # bam2_path
    bam2_path = models.CharField(max_length=1024, blank=True, default='')

    # bam2_tool
    bam2_tool = models.CharField(max_length=1024, blank=True, default='')

    # bam 文件地址
    bam_location = models.CharField(max_length=1024, default='')

    task_id = models.BigIntegerField(null=True)
    result_path = models.CharField(max_length=1024, null=True)

    # 样本所有者
    user_id = models.BigIntegerField(default=1)

    # 标准品编号
    standard_code = models.CharField(max_length=1024, blank=True, default='')

    backup1 = models.CharField(max_length=128, blank=True, default='')
    backup2 = models.CharField(max_length=128, blank=True, default='')
    backup3 = models.CharField(max_length=128, blank=True, default='')
    backup4 = models.CharField(max_length=128, blank=True, default='')
    backup5 = models.CharField(max_length=128, blank=True, default='')
    backup6 = models.CharField(max_length=128, blank=True, default='')
    backup7 = models.CharField(max_length=128, blank=True, default='')
    backup8 = models.CharField(max_length=128, blank=True, default='')
    backup9 = models.CharField(max_length=128, blank=True, default='')
    backup10 = models.CharField(max_length=128, blank=True, default='')

    create_time = models.DateTimeField(null=True,
                                       blank=True,
                                       auto_now_add=True)
    modify_time = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        db_table = "sample"
        ordering = ["-id"]
        verbose_name = "样本"
        verbose_name_plural = verbose_name
        get_latest_by = "id"

        unique_together = ('test_date', 'library_type', 'pooling_library')

    def _real_path(self, path):
        return path if os.path.exists(path) else None

    @property
    def real_fastq1_path(self):
        return self._real_path(self.fastq1_path)

    @property
    def real_fastq2_path(self):
        return self._real_path(self.fastq2_path)

    @property
    def real_bam1_path(self):
        return self._real_path(self.bam1_path)

    @property
    def real_bam2_path(self):
        return self._real_path(self.bam2_path)

    def has_bam_path(self):
        return self._real_path(self.bam1_path) and self._real_path(
            self.bam2_path)

    @property
    def name(self):
        return '{}--{}'.format(self.library_type, self.index_number)

    @property
    def is_standard(self):
        return self.standard_code.lower() != 'no'

    @property
    def username(self):
        try:
            account = Account.objects.get(id=self.user_id)
            return account.username
        except ObjectDoesNotExist:
            return ""
