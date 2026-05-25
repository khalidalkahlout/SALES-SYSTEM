import sqlite3

# 1. الاتصال بقاعدة البيانات (سيتم إنشاء الملف تلقائياً إذا لم يكن موجوداً)
conn = sqlite3.connect('store_database.db')
cursor = conn.cursor()

print("[جاري انشاء الجداول في قاعدةالبيانات]")

# 2. كود SQL لإنشاء الجداول
sql_create_tables = """

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Managers (
    manager_id INTEGER PRIMARY KEY AUTOINCREMENT,
    manager_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    hire_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS Employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name TEXT NOT NULL,
    role TEXT NOT NULL,
    salary REAL,
    manager_id INTEGER,
    hire_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (manager_id) REFERENCES Managers(manager_id)
);

CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category TEXT,
    price REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    employee_id INTEGER,
    quantity INTEGER NOT NULL,
    total_price REAL NOT NULL,
    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);
"""

# تنفيذ كود إنشاء الجداول
cursor.executescript(sql_create_tables)
print("تم انشاء الجداول بنجاح")

# 3. إضافة بيانات تجريبية (Mock Data) للتأكد من أن كل شيء يعمل
print("جاري ادخل بيانات تجريبية حقيقية ")

try:
    # إدخال مدراء
    cursor.executemany("INSERT OR IGNORE INTO Managers (manager_id, manager_name, email, phone) VALUES (?, ?, ?, ?)", [
        (1, 'احمد علي', 'ahmed@store.com', '01012345678'),
        (2, 'سارة محمود', 'sara@store.com', '01223456789')
    ])

    # إدخال موظفين
    cursor.executemany("INSERT OR IGNORE INTO Employees (employee_id, employee_name, role, salary, manager_id) VALUES (?, ?, ?, ?, ?)", [
        (101, 'عمر شريف', 'كاشير', 5000.0, 1),
        (102, 'منة خالد', 'مسؤل مبيعات', 6000.0, 1),
        (103, 'يوسف حسين', 'كاشير', 5200.0, 2)
    ])

    # إدخال منتجات
    cursor.executemany("INSERT OR IGNORE INTO Products (product_id, product_name, category, price, stock) VALUES (?, ?, ?, ?, ?)", [
        (1, 'شاحن سريعType-C', 'الكترونيات', 350.0, 50),
        (2, 'سماعة بلوتوث', 'الكترونيات', 800.0, 30),
        (3, 'زجاجة مياه رياضية', 'أدوات منزلية', 150.0, 100),
        (4, 'ساعة ذكية Smart Watch', 'الكترونيات', 1500.0, 15)
    ])

    # إدخال مبيعات تجريبية (الكمية * السعر يحسب تلقائياً هنا للتسهيل)
    cursor.executemany("INSERT OR IGNORE INTO Sales (product_id, employee_id, quantity, total_price) VALUES (?, ?, ?, ?)", [
        (1, 101, 2, 700.0),   # عمر باع 2 شاحن
        (2, 102, 1, 800.0),   # منة باعت سماعة
        (4, 101, 1, 1500.0),  # عمر باع ساعة
        (3, 103, 3, 450.0)    # يوسف باع 3 زجاجات مياه
    ])

    # حفظ التغييرات
    conn.commit()
    print("تم ادخال البيانات التجريبية بنجاح")

except sqlite3.Error as e:
    print(f"حدث خطأ أثناء ادخال البيانات : {e}")

finally:
    # إغلاق الاتصال
    conn.close()
    print("\nقاعدةالبيانات جاهزة للاستخدام والربط ")
    