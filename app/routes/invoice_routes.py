from flask import Blueprint, render_template, request, redirect, url_for
from app.services.invoice_service import InvoiceService

invoice_bp = Blueprint('invoice', __name__)

@invoice_bp.route('/')
def index():
    invoices = InvoiceService.get_all_invoices()
    return render_template('index.html', invoices=invoices)

@invoice_bp.route('/create', methods=['GET', 'POST'])
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
        
        invoice_id = InvoiceService.create_invoice(
            invoice_number, client_name, client_address, date, due_date,
            descriptions, quantities, prices
        )
        return redirect(url_for('invoice.view_invoice', invoice_id=invoice_id))
        
    return render_template('create.html')

@invoice_bp.route('/invoice/<int:invoice_id>')
def view_invoice(invoice_id):
    invoice, items = InvoiceService.get_invoice_by_id(invoice_id)
    if not invoice:
        return "Faktur tidak ditemukan", 404
        
    return render_template('view.html', invoice=invoice, items=items)

@invoice_bp.route('/delete/<int:invoice_id>', methods=['POST'])
def delete_invoice(invoice_id):
    InvoiceService.delete_invoice(invoice_id)
    return redirect(url_for('invoice.index'))
