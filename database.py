import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(user_id, trans_type, amount, category=None):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO transactions (user_id, type, amount, category, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, trans_type, amount, category, date))
    conn.commit()
    conn.close()

def get_balance(user_id):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END)
        FROM transactions
        WHERE user_id = ?
    ''', (user_id,))
    result = cursor.fetchone()[0]
    conn.close()
    return result if result else 0.0

def get_summary(user_id):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT type, SUM(amount) FROM transactions
        WHERE user_id = ?
        GROUP BY type
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    income = 0
    expense = 0
    for row in rows:
        if row[0] == 'income':
            income = row[1]
        elif row[0] == 'expense':
            expense = row[1]
    return income, expense