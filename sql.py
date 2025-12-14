"""
使用 sqlite3-to-mysql 工具转换 SQLite 数据库到 MySQL

安装方法：
pip install sqlite3-to-mysql

使用方法：
1. 直接运行此脚本（需要配置 MySQL 连接信息）
2. 或使用命令行工具 sqlite3mysql
"""

import subprocess
import sys
import os

def check_and_install_package():
    """检查并安装 sqlite3-to-mysql 包"""
    try:
        import sqlite3_to_mysql
        print("✓ sqlite3-to-mysql 已安装")
        return True
    except ImportError:
        print("正在安装 sqlite3-to-mysql...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "sqlite3-to-mysql"])
            print("✓ 安装成功")
            return True
        except subprocess.CalledProcessError:
            print("✗ 安装失败，请手动运行: pip install sqlite3-to-mysql")
            return False

def convert_with_sqlite3_to_mysql(sqlite_file, mysql_config):
    """
    使用 sqlite3-to-mysql 转换数据库
    
    参数:
        sqlite_file: SQLite 数据库文件路径
        mysql_config: MySQL 配置字典，包含：
            - host: MySQL 主机地址
            - port: MySQL 端口（默认 3306）
            - user: MySQL 用户名
            - password: MySQL 密码
            - database: 目标数据库名
    """
    if not os.path.exists(sqlite_file):
        print(f"错误：找不到 SQLite 文件 {sqlite_file}")
        return False
    
    try:
        from sqlite3_to_mysql import SQLite3toMySQL
        
        converter = SQLite3toMySQL(
            sqlite_file=sqlite_file,
            mysql_user=mysql_config.get('user'),
            mysql_password=mysql_config.get('password'),
            mysql_host=mysql_config.get('host', 'localhost'),
            mysql_port=mysql_config.get('port', 3306),
            mysql_database=mysql_config.get('database'),
            # 可选参数
            chunk_size=10000,  # 每次处理的行数
            quiet=False,  # 显示进度
        )
        
        print(f"开始转换 {sqlite_file} 到 MySQL...")
        converter.transfer()
        print("✓ 转换完成！")
        return True
        
    except Exception as e:
        print(f"转换失败: {e}")
        return False

def convert_to_sql_file(sqlite_file, output_sql_file):
    """
    将 SQLite 数据库导出为 MySQL 兼容的 SQL 文件
    
    这个方法使用 sqlite3-to-mysql 的导出功能
    """
    if not os.path.exists(sqlite_file):
        print(f"错误：找不到 SQLite 文件 {sqlite_file}")
        return False
    
    try:
        from sqlite3_to_mysql import SQLite3toMySQL
        
        # 使用临时配置（不会真正连接 MySQL）
        converter = SQLite3toMySQL(
            sqlite_file=sqlite_file,
            mysql_user='dummy',
            mysql_password='dummy',
            mysql_host='localhost',
            mysql_port=3306,
            mysql_database='dummy',
        )
        
        print(f"正在导出 {sqlite_file} 为 MySQL SQL 文件...")
        # 注意：sqlite3-to-mysql 主要设计用于直接转换到 MySQL 数据库
        # 如果要导出为 SQL 文件，可能需要使用其他方法
        
        # 使用命令行工具导出
        cmd = [
            sys.executable, "-m", "sqlite3_to_mysql",
            "--sqlite-file", sqlite_file,
            "--mysql-database", "export",
            "--mysql-user", "dummy",
            "--mysql-password", "dummy",
            "--mysql-host", "localhost",
        ]
        
        print("提示：sqlite3-to-mysql 主要用于直接转换到 MySQL 数据库")
        return False
        
    except Exception as e:
        print(f"导出失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("使用 sqlite3-to-mysql 工具转换数据库")
    print("=" * 60)
    
    # 检查并安装包
    if not check_and_install_package():
        sys.exit(1)
    
    # 配置 SQLite 文件
    sqlite_file = "cloudreve1.db"
    
    if not os.path.exists(sqlite_file):
        print(f"错误：找不到文件 {sqlite_file}")
        print("\n当前目录中的文件：")
        for f in os.listdir('.'):
            if f.endswith('.db') or f.endswith('.sqlite') or f.endswith('.sqlite3'):
                print(f"  - {f}")
        sys.exit(1)
    
    print(f"\n找到 SQLite 文件: {sqlite_file}")
    print("\n请输入 MySQL 连接信息：")
    mysql_config = {
        'host': input("MySQL 主机 (默认: localhost): ").strip() or 'localhost',
        'port': int(input("MySQL 端口 (默认: 3306): ").strip() or '3306'),
        'user': input("MySQL 用户名: ").strip(),
        'password': input("MySQL 密码: ").strip(),
        'database': input("目标数据库名: ").strip(),
    }
    
    if convert_with_sqlite3_to_mysql(sqlite_file, mysql_config):
        print("\n✓ 转换成功！")
    else:
        print("\n✗ 转换失败")

