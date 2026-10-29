import sqlite3
import os
from flask import current_app

def get_db():
    db_path = current_app.config['DB_NAME']
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT NOT NULL,
            client_name TEXT NOT NULL,
            client_address TEXT,
            date TEXT NOT NULL,
            due_date TEXT,
            total_amount REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            description TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

class InvoiceService:
    @staticmethod
    def get_all_invoices():
        conn = get_db()
        invoices = conn.execute('SELECT * FROM invoices ORDER BY id DESC').fetchall()
        conn.close()
        return invoices

    @staticmethod
    def get_invoice_by_id(invoice_id):
        conn = get_db()
        invoice = conn.execute('SELECT * FROM invoices WHERE id = ?', (invoice_id,)).fetchone()
        items = conn.execute('SELECT * FROM invoice_items WHERE invoice_id = ?', (invoice_id,)).fetchall()
        conn.close()
        return invoice, items

    @staticmethod
    def create_invoice(invoice_number, client_name, client_address, date, due_date, descriptions, quantities, prices):
        total_amount = 0
        items = []
        for desc, qty, price in zip(descriptions, quantities, prices):
            if not desc or desc.strip() == '':
                continue
            q = float(qty)
            p = float(price)
            subtotal = q * p
            total_amount += subtotal
            items.append((desc, q, p, subtotal))

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO invoices (invoice_number, client_name, client_address, date, due_date, total_amount)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (invoice_number, client_name, client_address, date, due_date, total_amount))
        invoice_id = cursor.lastrowid

        for item in items:
            cursor.execute('''
                INSERT INTO invoice_items (invoice_id, description, quantity, price, subtotal)
                VALUES (?, ?, ?, ?, ?)
            ''', (invoice_id, item[0], item[1], item[2], item[3]))

        conn.commit()
        conn.close()
        return invoice_id

    @staticmethod
    def delete_invoice(invoice_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM invoice_items WHERE invoice_id = ?', (invoice_id,))
        cursor.execute('DELETE FROM invoices WHERE id = ?', (invoice_id,))
        conn.commit()
        conn.close()
