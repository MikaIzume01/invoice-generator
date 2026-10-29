from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_NAME = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
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

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM invoices ORDER BY id DESC')
    invoices = cursor.fetchall()
    conn.close()
    return render_template('index.html', invoices=invoices)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        invoice_number = request.form['invoice_number']
        client_name = request.form['client_name']
        client_address = request.form['client_address']
        date = request.form['date']
        due_date = request.form['due_date']
        
        descriptions = request.form.getlist('description[]')
        quantities = request.form.getlist('quantity[]')
        prices = request.form.getlist('price[]')
        
        total_amount = 0
        items = []
        for desc, qty, price in zip(descriptions, quantities, prices):
            if desc.strip() == '':
                continue
            q = float(qty)
            p = float(price)
            subtotal = q * p
            total_amount += subtotal
            items.append((desc, q, p, subtotal))
            
        conn = sqlite3.connect(DB_NAME)
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
        return redirect(url_for('view_invoice', invoice_id=invoice_id))
        
    return render_template('create.html')

@app.route('/invoice/<int:invoice_id>')
def view_invoice(invoice_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM invoices WHERE id = ?', (invoice_id,))
    invoice = cursor.fetchone()
    
    cursor.execute('SELECT * FROM invoice_items WHERE invoice_id = ?', (invoice_id,))
    items = cursor.fetchall()
    conn.close()
    
    if not invoice:
        return "Faktur tidak ditemukan", 404
        
    return render_template('view.html', invoice=invoice, items=items)

@app.route('/delete/<int:invoice_id>', methods=['POST'])
def delete_invoice(invoice_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM invoice_items WHERE invoice_id = ?', (invoice_id,))
    cursor.execute('DELETE FROM invoices WHERE id = ?', (invoice_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
