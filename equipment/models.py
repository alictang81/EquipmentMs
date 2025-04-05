from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField('设备类别', max_length=50, unique=True)
    color = models.CharField('颜色标识', max_length=7, default='#909399')

    class Meta:
        verbose_name = '设备分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField('供应商', max_length=100)
    contact = models.CharField('联系人', max_length=50)
    phone = models.CharField('联系电话', max_length=20)

    class Meta:
        verbose_name = '供应商'
        verbose_name_plural = verbose_name

class Equipment(models.Model):
    CATEGORY_CHOICES = [
        ('geophysical', '物探设备'),
        ('survey', '测绘仪器'),
        ('transport', '交通工具'),
    ]

    name = models.CharField('设备名称', max_length=100)
    serial_num = models.CharField('设备编码', max_length=30, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='设备分类')
    purchase_year = models.SmallIntegerField(
        '采购年份',
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    invoice = models.FileField('发票扫描件', upload_to='invoices/')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, verbose_name='供应商')
    DEPRECIATION_RATE = models.DecimalField('折旧率', max_digits=5, decimal_places=2, default=0.10)

    class Meta:
        verbose_name = '设备主数据'
        verbose_name_plural = verbose_name
        indexes = [models.Index(fields=['serial_num'])]

class Component(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='components')
    name = models.CharField('配件名称', max_length=100)
    model = models.CharField('型号', max_length=50)
    quantity = models.PositiveIntegerField('数量')

    class Meta:
        verbose_name = '设备配件'
        verbose_name_plural = verbose_name