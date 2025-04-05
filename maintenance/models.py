from django.db import models
from equipment.models import Equipment
from core.rbac.models import User

FAULT_STATUS = [
    ('pending', '待处理'),
    ('processing', '维修中'),
    ('completed', '已完成')
]

class FaultReport(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, verbose_name='故障设备')
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='报告人')
    description = models.TextField('故障描述')
    images = models.FileField('故障照片', upload_to='fault_reports/')
    project_source = models.CharField('来源项目', max_length=100)
    fault_time = models.DateTimeField('故障时间', auto_now_add=True)
    is_confirmed = models.BooleanField('已确认', default=False)

    class Meta:
        verbose_name = '故障报告'
        indexes = [models.Index(fields=['equipment', 'fault_time'])]

class MaintenanceRecord(models.Model):
    fault = models.ForeignKey(FaultReport, on_delete=models.CASCADE, related_name='maintenance_records')
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='维修人员')
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('完成时间')
    procedure = models.TextField('维修过程')
    replaced_parts = models.JSONField('更换配件', default=list)
    cost = models.DecimalField('维修费用', max_digits=10, decimal_places=2, null=True)
    status = models.CharField('处理状态', max_length=20, choices=FAULT_STATUS)

    class Meta:
        verbose_name = '维修台账'

class Depreciation(models.Model):
    equipment = models.OneToOneField(Equipment, on_delete=models.CASCADE, verbose_name='设备', related_name='depreciation')
    current_value = models.DecimalField('当前净值', max_digits=12, decimal_places=2)
    last_calculated = models.DateField('最后计算日期')
    next_calculation = models.DateField('下次计算日期')

    class Meta:
        verbose_name = '折旧跟踪'