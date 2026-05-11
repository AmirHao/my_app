import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_name='ledger.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.init_database()

    def connect(self):
        """连接数据库"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()

    def init_database(self):
        """初始化数据库表"""
        self.connect()

        # 创建分类表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                type TEXT NOT NULL CHECK(type IN ('income', 'expense'))
            )
        ''')

        # 创建交易记录表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category_id INTEGER NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                date TEXT NOT NULL,
                note TEXT,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')

        # 插入默认分类
        default_categories = [
            ('工资', 'income'),
            ('奖金', 'income'),
            ('其他收入', 'income'),
            ('餐饮', 'expense'),
            ('交通', 'expense'),
            ('购物', 'expense'),
            ('旅游', 'expense'),
            ('生活', 'expense'),
            ('娱乐', 'expense'),
            ('其他支出', 'expense')
        ]

        for name, type_ in default_categories:
            try:
                self.cursor.execute('INSERT INTO categories (name, type) VALUES (?, ?)', (name, type_))
            except sqlite3.IntegrityError:
                pass

        self.conn.commit()
        self.close()

    def add_transaction(self, amount, category_id, trans_type, date, note=''):
        """添加交易记录"""
        self.connect()
        self.cursor.execute('''
            INSERT INTO transactions (amount, category_id, type, date, note)
            VALUES (?, ?, ?, ?, ?)
        ''', (amount, category_id, trans_type, date, note))
        self.conn.commit()
        self.close()

    def get_categories(self, trans_type=None):
        """获取分类列表"""
        self.connect()
        if trans_type:
            self.cursor.execute('SELECT * FROM categories WHERE type = ?', (trans_type,))
        else:
            self.cursor.execute('SELECT * FROM categories')
        categories = self.cursor.fetchall()
        self.close()
        return categories

    def add_category(self, name, trans_type):
        """添加新分类"""
        self.connect()
        try:
            self.cursor.execute('INSERT INTO categories (name, type) VALUES (?, ?)', (name, trans_type))
            self.conn.commit()
            self.close()
            return True
        except sqlite3.IntegrityError:
            self.close()
            return False

    def get_transactions(self, start_date=None, end_date=None, category_id=None):
        """获取交易记录"""
        self.connect()
        query = '''
            SELECT t.id, t.amount, c.name, t.type, t.date, t.note
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE 1=1
        '''
        params = []

        if start_date:
            query += ' AND t.date >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND t.date <= ?'
            params.append(end_date)
        if category_id:
            query += ' AND t.category_id = ?'
            params.append(category_id)

        query += ' ORDER BY t.date DESC'

        self.cursor.execute(query, params)
        transactions = self.cursor.fetchall()
        self.close()
        return transactions

    def get_statistics(self, start_date, end_date, group_by_category=False):
        """获取统计数据"""
        self.connect()

        if group_by_category:
            query = '''
                SELECT c.name, t.type, SUM(t.amount) as total
                FROM transactions t
                JOIN categories c ON t.category_id = c.id
                WHERE t.date >= ? AND t.date <= ?
                GROUP BY c.name, t.type
                ORDER BY total DESC
            '''
        else:
            query = '''
                SELECT t.type, SUM(t.amount) as total
                FROM transactions t
                WHERE t.date >= ? AND t.date <= ?
                GROUP BY t.type
            '''

        self.cursor.execute(query, (start_date, end_date))
        stats = self.cursor.fetchall()
        self.close()
        return stats

    def delete_transaction(self, trans_id):
        """删除交易记录"""
        self.connect()
        self.cursor.execute('DELETE FROM transactions WHERE id = ?', (trans_id,))
        self.conn.commit()
        self.close()
