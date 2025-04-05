from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import PermissionDenied

ROLE_CHOICES = [
    ('admin', '系统管理员'),
    ('user', '普通用户'),
    ('auditor', '审计员')
]

class User(AbstractUser):
    department = models.CharField('所属部门', max_length=50)
    role = models.CharField('角色', max_length=20, choices=ROLE_CHOICES)
    allowed_equipments = models.ManyToManyField('equipment.Equipment', verbose_name='可操作设备', blank=True)

    def check_perm(self, perm_codename):
        if self.role == 'admin':
            return True
        from .permissions import permissions_map
        required_perms = permissions_map.get(perm_codename, [])
        return all(self.has_perm(perm) for perm in required_perms)

class PermissionGroup(models.Model):
    name = models.CharField('权限组', max_length=50)
    code = models.SlugField('组标识', unique=True)
    permissions = models.TextField('权限清单') 

    class Meta:
        verbose_name = '权限组管理'

class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField('操作时间', auto_now_add=True)
    action = models.CharField('操作类型', max_length=100)
    equipment = models.ForeignKey('equipment.Equipment', on_delete=models.SET_NULL, null=True)
    raw_data = models.JSONField('原始数据', null=True)