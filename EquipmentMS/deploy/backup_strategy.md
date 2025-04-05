# 备份策略指南

## 数据库备份
```bash
# 每日凌晨执行pg_dump
pg_dump -h db -U equipment_user equipment_prod | gzip > /backups/equipment_db_$(date +%Y%m%d).sql.gz

# 保留最近30天备份
find /backups -name '*.sql.gz' -mtime +30 -exec rm {} \;
```

## 文件备份
- 静态文件：/app/static目录每日同步到OSS
- 日志文件：使用logrotate每日切割Nginx/uWSGI日志

## 恢复流程
1. 停止应用服务
2. gunzip -c 备份文件.sql.gz | psql -h db -U equipment_user equipment_prod
3. 同步静态文件
4. 启动服务