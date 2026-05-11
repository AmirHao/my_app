import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from database import Database
import calendar

class LedgerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("个人账本管理系统")
        self.root.geometry("1000x700")

        self.db = Database()

        # 创建主界面
        self.create_widgets()

    def create_widgets(self):
        """创建主界面组件"""
        # 创建笔记本（标签页）
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # 添加记录页面
        self.add_record_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_record_frame, text='添加记录')
        self.create_add_record_page()

        # 查看记录页面
        self.view_records_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.view_records_frame, text='查看记录')
        self.create_view_records_page()

        # 统计分析页面
        self.statistics_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.statistics_frame, text='统计分析')
        self.create_statistics_page()

        # 分类管理页面
        self.category_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.category_frame, text='分类管理')
        self.create_category_page()

    def create_add_record_page(self):
        """创建添加记录页面"""
        frame = ttk.LabelFrame(self.add_record_frame, text="添加新记录", padding=20)
        frame.pack(fill='both', expand=True, padx=20, pady=20)

        # 类型选择
        ttk.Label(frame, text="类型:").grid(row=0, column=0, sticky='w', pady=5)
        self.trans_type_var = tk.StringVar(value='expense')
        type_frame = ttk.Frame(frame)
        type_frame.grid(row=0, column=1, sticky='w', pady=5)
        ttk.Radiobutton(type_frame, text="支出", variable=self.trans_type_var,
                       value='expense', command=self.update_categories).pack(side='left', padx=5)
        ttk.Radiobutton(type_frame, text="收入", variable=self.trans_type_var,
                       value='income', command=self.update_categories).pack(side='left', padx=5)

        # 金额
        ttk.Label(frame, text="金额:").grid(row=1, column=0, sticky='w', pady=5)
        self.amount_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.amount_var, width=30).grid(row=1, column=1, sticky='w', pady=5)

        # 分类
        ttk.Label(frame, text="分类:").grid(row=2, column=0, sticky='w', pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(frame, textvariable=self.category_var, width=28, state='readonly')
        self.category_combo.grid(row=2, column=1, sticky='w', pady=5)
        self.update_categories()

        # 日期
        ttk.Label(frame, text="日期:").grid(row=3, column=0, sticky='w', pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        ttk.Entry(frame, textvariable=self.date_var, width=30).grid(row=3, column=1, sticky='w', pady=5)
        ttk.Label(frame, text="格式: YYYY-MM-DD", font=('Arial', 8)).grid(row=3, column=2, sticky='w', padx=5)

        # 备注
        ttk.Label(frame, text="备注:").grid(row=4, column=0, sticky='nw', pady=5)
        self.note_text = tk.Text(frame, width=30, height=5)
        self.note_text.grid(row=4, column=1, sticky='w', pady=5)

        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=1, sticky='w', pady=20)
        ttk.Button(btn_frame, text="保存", command=self.save_record).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="清空", command=self.clear_form).pack(side='left', padx=5)

    def update_categories(self):
        """更新分类下拉列表"""
        trans_type = self.trans_type_var.get()
        categories = self.db.get_categories(trans_type)
        self.category_combo['values'] = [cat[1] for cat in categories]
        if categories:
            self.category_combo.current(0)

    def save_record(self):
        """保存记录"""
        try:
            amount = float(self.amount_var.get())
            if amount <= 0:
                raise ValueError("金额必须大于0")

            category_name = self.category_var.get()
            if not category_name:
                raise ValueError("请选择分类")

            # 获取分类ID
            categories = self.db.get_categories(self.trans_type_var.get())
            category_id = None
            for cat in categories:
                if cat[1] == category_name:
                    category_id = cat[0]
                    break

            if not category_id:
                raise ValueError("分类不存在")

            date = self.date_var.get()
            datetime.strptime(date, '%Y-%m-%d')  # 验证日期格式

            note = self.note_text.get('1.0', 'end-1c')

            self.db.add_transaction(amount, category_id, self.trans_type_var.get(), date, note)
            messagebox.showinfo("成功", "记录已保存")
            self.clear_form()

        except ValueError as e:
            messagebox.showerror("错误", str(e))

    def clear_form(self):
        """清空表单"""
        self.amount_var.set('')
        self.date_var.set(datetime.now().strftime('%Y-%m-%d'))
        self.note_text.delete('1.0', 'end')
        self.update_categories()

    def create_view_records_page(self):
        """创建查看记录页面"""
        # 筛选框架
        filter_frame = ttk.LabelFrame(self.view_records_frame, text="筛选条件", padding=10)
        filter_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(filter_frame, text="开始日期:").grid(row=0, column=0, padx=5)
        self.view_start_date = tk.StringVar(value=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        ttk.Entry(filter_frame, textvariable=self.view_start_date, width=15).grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="结束日期:").grid(row=0, column=2, padx=5)
        self.view_end_date = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        ttk.Entry(filter_frame, textvariable=self.view_end_date, width=15).grid(row=0, column=3, padx=5)

        ttk.Button(filter_frame, text="查询", command=self.load_records).grid(row=0, column=4, padx=5)
        ttk.Button(filter_frame, text="删除选中", command=self.delete_selected_record).grid(row=0, column=5, padx=5)

        # 记录列表
        list_frame = ttk.Frame(self.view_records_frame)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # 创建表格
        columns = ('ID', '金额', '分类', '类型', '日期', '备注')
        self.records_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)

        for col in columns:
            self.records_tree.heading(col, text=col)
            if col == 'ID':
                self.records_tree.column(col, width=50)
            elif col == '金额':
                self.records_tree.column(col, width=100)
            elif col == '分类':
                self.records_tree.column(col, width=100)
            elif col == '类型':
                self.records_tree.column(col, width=80)
            elif col == '日期':
                self.records_tree.column(col, width=100)
            else:
                self.records_tree.column(col, width=200)

        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.records_tree.yview)
        self.records_tree.configure(yscrollcommand=scrollbar.set)

        self.records_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.load_records()

    def load_records(self):
        """加载记录"""
        # 清空现有记录
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        try:
            start_date = self.view_start_date.get()
            end_date = self.view_end_date.get()

            records = self.db.get_transactions(start_date, end_date)

            for record in records:
                trans_id, amount, category, trans_type, date, note = record
                type_text = '收入' if trans_type == 'income' else '支出'
                self.records_tree.insert('', 'end', values=(trans_id, f'{amount:.2f}', category, type_text, date, note))

        except Exception as e:
            messagebox.showerror("错误", f"加载记录失败: {str(e)}")

    def delete_selected_record(self):
        """删除选中的记录"""
        selected = self.records_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的记录")
            return

        if messagebox.askyesno("确认", "确定要删除选中的记录吗？"):
            for item in selected:
                trans_id = self.records_tree.item(item)['values'][0]
                self.db.delete_transaction(trans_id)
            self.load_records()
            messagebox.showinfo("成功", "记录已删除")

    def create_statistics_page(self):
        """创建统计分析页面"""
        # 时间范围选择
        range_frame = ttk.LabelFrame(self.statistics_frame, text="统计范围", padding=10)
        range_frame.pack(fill='x', padx=20, pady=10)

        self.stat_range_var = tk.StringVar(value='month')
        ttk.Radiobutton(range_frame, text="本周", variable=self.stat_range_var,
                       value='week', command=self.update_statistics).pack(side='left', padx=10)
        ttk.Radiobutton(range_frame, text="本月", variable=self.stat_range_var,
                       value='month', command=self.update_statistics).pack(side='left', padx=10)
        ttk.Radiobutton(range_frame, text="本年", variable=self.stat_range_var,
                       value='year', command=self.update_statistics).pack(side='left', padx=10)

        # 统计结果显示
        result_frame = ttk.LabelFrame(self.statistics_frame, text="统计结果", padding=10)
        result_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # 总计
        summary_frame = ttk.Frame(result_frame)
        summary_frame.pack(fill='x', pady=10)

        self.income_label = ttk.Label(summary_frame, text="总收入: ¥0.00", font=('Arial', 14, 'bold'), foreground='green')
        self.income_label.pack(side='left', padx=20)

        self.expense_label = ttk.Label(summary_frame, text="总支出: ¥0.00", font=('Arial', 14, 'bold'), foreground='red')
        self.expense_label.pack(side='left', padx=20)

        self.balance_label = ttk.Label(summary_frame, text="结余: ¥0.00", font=('Arial', 14, 'bold'))
        self.balance_label.pack(side='left', padx=20)

        # 分类统计表格
        columns = ('分类', '类型', '金额')
        self.stats_tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=15)

        for col in columns:
            self.stats_tree.heading(col, text=col)
            self.stats_tree.column(col, width=200)

        scrollbar = ttk.Scrollbar(result_frame, orient='vertical', command=self.stats_tree.yview)
        self.stats_tree.configure(yscrollcommand=scrollbar.set)

        self.stats_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.update_statistics()

    def update_statistics(self):
        """更新统计数据"""
        # 清空表格
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)

        # 计算日期范围
        today = datetime.now()
        range_type = self.stat_range_var.get()

        if range_type == 'week':
            start_date = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
        elif range_type == 'month':
            start_date = today.replace(day=1).strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
        else:  # year
            start_date = today.replace(month=1, day=1).strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')

        # 获取统计数据
        stats = self.db.get_statistics(start_date, end_date, group_by_category=True)

        total_income = 0
        total_expense = 0

        for stat in stats:
            category, trans_type, amount = stat
            type_text = '收入' if trans_type == 'income' else '支出'
            self.stats_tree.insert('', 'end', values=(category, type_text, f'¥{amount:.2f}'))

            if trans_type == 'income':
                total_income += amount
            else:
                total_expense += amount

        # 更新总计标签
        self.income_label.config(text=f"总收入: ¥{total_income:.2f}")
        self.expense_label.config(text=f"总支出: ¥{total_expense:.2f}")
        balance = total_income - total_expense
        self.balance_label.config(text=f"结余: ¥{balance:.2f}",
                                 foreground='green' if balance >= 0 else 'red')

    def create_category_page(self):
        """创建分类管理页面"""
        # 添加分类框架
        add_frame = ttk.LabelFrame(self.category_frame, text="添加新分类", padding=20)
        add_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(add_frame, text="分类名称:").grid(row=0, column=0, padx=5, pady=5)
        self.new_category_name = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_category_name, width=20).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="类型:").grid(row=0, column=2, padx=5, pady=5)
        self.new_category_type = tk.StringVar(value='expense')
        type_combo = ttk.Combobox(add_frame, textvariable=self.new_category_type,
                                 values=['收入 (income)', '支出 (expense)'], width=18, state='readonly')
        type_combo.grid(row=0, column=3, padx=5, pady=5)
        type_combo.current(1)

        ttk.Button(add_frame, text="添加", command=self.add_new_category).grid(row=0, column=4, padx=5, pady=5)

        # 分类列表
        list_frame = ttk.LabelFrame(self.category_frame, text="现有分类", padding=10)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)

        columns = ('ID', '分类名称', '类型')
        self.category_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)

        for col in columns:
            self.category_tree.heading(col, text=col)
            if col == 'ID':
                self.category_tree.column(col, width=100)
            else:
                self.category_tree.column(col, width=300)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.category_tree.yview)
        self.category_tree.configure(yscrollcommand=scrollbar.set)

        self.category_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.load_categories()

    def add_new_category(self):
        """添加新分类"""
        name = self.new_category_name.get().strip()
        if not name:
            messagebox.showwarning("警告", "请输入分类名称")
            return

        type_text = self.new_category_type.get()
        trans_type = 'income' if 'income' in type_text else 'expense'

        if self.db.add_category(name, trans_type):
            messagebox.showinfo("成功", "分类已添加")
            self.new_category_name.set('')
            self.load_categories()
        else:
            messagebox.showerror("错误", "分类已存在")

    def load_categories(self):
        """加载分类列表"""
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)

        categories = self.db.get_categories()
        for cat in categories:
            cat_id, name, trans_type = cat
            type_text = '收入' if trans_type == 'income' else '支出'
            self.category_tree.insert('', 'end', values=(cat_id, name, type_text))

def main():
    root = tk.Tk()
    app = LedgerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
