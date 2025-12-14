# SQLite 到 MySQL 数据库转换工具
## 注意：工具转换后发现bug（用户组容量更改不了）
## 解决办法：打开你的数据库管理工具设计表，或者宝塔的数据库管理工具
|  字段名 | 修改前类型  | 修改后类型 | 修改后排序 |
| :------------: | :------------: | :------------: | :------------: |
|  name | 	text  | varchar(255)  | utf8mb4_bin	 |
| max_storage  | int(11)  | bigint(20)  | 无 |
| 	speed_limit  |  int(11) | bigint(20)  | 无 |

本项目提供将 SQLite 数据库（特别是 Cloudreve 数据库）转换为 MySQL 数据库的工具和脚本。
以及实现多个网站无损装换   建议本地操作再导入
本地自行搭建mysql+Navicat Premium （速度快）
远程也可以但是速度很慢（远程记得把数据库权限设置为所有人）
## 本地操作
- mysql新建数据库
- Navicat Premium作为辅助导入远程数据库
- 运行python sql.py按照操作下一步就行了
```bash
127.0.0.1
3306
root
密码
数据库名
```
然后导出完成后使用Navicat Premium数据传输或者转储sql（结构+目录）
链接远程数据库
导入你转储的数据库文件 等待执行完就可以无损的把数据转到mysql
## 环境要求

### 系统要求
- Python 3.6 或更高版本
- MySQL 5.7 或更高版本（或 MariaDB 10.2+）
- 足够的磁盘空间用于存储转换后的数据

### Python 依赖

项目需要以下 Python 包：

- `sqlite3-to-mysql`: 用于 SQLite 到 MySQL 的数据库转换

## 安装配置

### 1. 安装 Python 依赖

运行主脚本 `sql.py` 时，脚本会自动检查并安装 `sqlite3-to-mysql` 包。如果需要手动安装：

```bash
pip install sqlite3-to-mysql
```

### 2. MySQL 数据库准备

在开始转换之前，请确保：

1. **MySQL 服务已启动**
   ```bash
   # Windows
   net start MySQL
   
   # Linux/Mac
   sudo systemctl start mysql
   ```

2. **创建目标数据库**
   ```sql
   CREATE DATABASE your_database_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **确保有足够的权限**
   - 需要 CREATE、INSERT、SELECT 等权限
   - 建议使用具有完整权限的用户账户

### 3. 配置文件

确保 SQLite 数据库文件（`cloudreve.db`）位于项目根目录，或修改脚本中的文件路径。

## 使用方法

### 方法一：使用 sql.py 直接转换（推荐）

1. **运行脚本**
   ```bash
   python sql.py
   ```

2. **按提示输入 MySQL 连接信息**
   - MySQL 主机（默认: localhost）
   - MySQL 端口（默认: 3306）
   - MySQL 用户名
   - MySQL 密码
   - 目标数据库名

3. **等待转换完成**
   - 脚本会自动检查并安装依赖
   - 转换过程会显示进度信息
   - 转换完成后会显示成功提示


## 配置说明

### MySQL 连接配置

在 `sql.py` 中，MySQL 配置通过交互式输入获取，包含以下参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| host | MySQL 主机地址 | localhost |
| port | MySQL 端口 | 3306 |
| user | MySQL 用户名 | 必填 |
| password | MySQL 密码 | 必填 |
| database | 目标数据库名 | 必填 |

### 转换参数

在 `sql.py` 的 `convert_with_sqlite3_to_mysql` 函数中，可以调整以下参数：

```python
chunk_size=10000,  # 每次处理的行数，可根据内存情况调整
quiet=False,       # 是否显示详细进度
```

## 注意事项

### 1. 数据备份

⚠️ **重要**: 转换前请务必备份原始 SQLite 数据库和目标 MySQL 数据库！

```bash
# 备份 SQLite 数据库
cp cloudreve1.db cloudreve1.db.backup

# 备份 MySQL 数据库
mysqldump -u username -p database_name > backup.sql
```

### 2. 字符编码

- 确保 MySQL 数据库使用 `utf8mb4` 字符集
- 脚本会自动处理编码转换，但建议检查转换后的数据完整性

### 3. 数据类型差异

SQLite 和 MySQL 的数据类型存在差异，脚本会自动转换：

| SQLite | MySQL |
|--------|-------|
| INTEGER | INT |
| TEXT | VARCHAR(255) |
| BLOB | LONGBLOB |
| REAL | DOUBLE |
| DATETIME | TIMESTAMP |
| BOOLEAN | TINYINT(1) |
| AUTOINCREMENT | AUTO_INCREMENT |

### 4. 外键约束

- 转换过程中会临时禁用外键检查
- 转换完成后会自动恢复外键检查

### 5. 大文件处理

如果数据库文件较大（> 100MB），建议：
- 增加 `chunk_size` 参数以提高性能
- 确保有足够的系统内存
- 转换过程中避免其他数据库操作

### 6. 错误处理

如果转换失败：
1. 检查 MySQL 连接信息是否正确
2. 确认目标数据库已创建
3. 检查用户权限是否足够
4. 查看错误信息并参考 MySQL 日志

## 常见问题

### Q: 转换后数据丢失怎么办？
A: 使用备份文件恢复，检查转换日志，确认数据类型映射是否正确。

### Q: 转换速度很慢？
A: 可以增加 `chunk_size` 参数，或检查网络连接（远程 MySQL）。

### Q: 出现编码错误？
A: 确保 MySQL 数据库使用 `utf8mb4` 字符集，检查原始数据的编码格式。

### Q: 如何验证转换结果？
A: 对比 SQLite 和 MySQL 中的记录数量，抽样检查关键数据是否正确。

## 许可证

本项目仅供学习和个人使用。

## 技术支持

如遇到问题，请检查：
1. Python 版本是否符合要求
2. 依赖包是否正确安装
3. MySQL 服务是否正常运行
4. 数据库连接信息是否正确

---

**最后更新**: 2025年12月15日

