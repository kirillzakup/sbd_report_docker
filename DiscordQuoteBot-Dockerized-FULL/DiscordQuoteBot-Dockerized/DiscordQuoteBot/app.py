import telebot
import json
import os
from flask import Flask, request, jsonify, send_from_directory
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
GROUP_ID = -1003095770924
REPORTS_FILE = 'reports.json'

app = Flask(__name__)
bot = telebot.TeleBot(TOKEN) if TOKEN else None

if os.path.exists(REPORTS_FILE):
    with open(REPORTS_FILE, 'r', encoding='utf-8') as f:
        reports = json.load(f)
else:
    reports = []

pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='CustomNormal', fontName='DejaVuSans', fontSize=12, leading=14))
styles.add(ParagraphStyle(name='CustomHeading', fontName='DejaVuSans-Bold', fontSize=14, leading=16))

def generate_pdf(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []

    elements.append(Paragraph("Ежедневный отчёт", styles['CustomHeading']))
    elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph(f"ФИО сотрудника: {data['fio']}", styles['CustomNormal']))
    elements.append(Paragraph(f"Дата и время: {data['datetime']}", styles['CustomNormal']))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph("Продажи за день:", styles['CustomNormal']))
    table_data = [['Товар', 'Количество', 'Цена за единицу (₸)', 'Сумма (₸)']]
    total_sales = 0
    for sale in data['sales']:
        amount = sale['quantity'] * sale['price']
        total_sales += amount
        table_data.append([sale['item'], str(sale['quantity']), f"{sale['price']:.2f}", f"{amount:.2f}"])
    table_data.append(['Итого продаж:', '', '', f"{total_sales:.2f}"])
    
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'DejaVuSans', 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONT', (0, -1), (-1, -1), 'DejaVuSans-Bold'),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph("Расходы за день:", styles['CustomNormal']))
    table_data = [['Описание', 'Сумма (₸)']]
    total_expenses = 0
    for expense in data['expenses']:
        total_expenses += expense['amount']
        table_data.append([expense['description'], f"{expense['amount']:.2f}"])
    table_data.append(['Итого расходы:', f"{total_expenses:.2f}"])
    
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'DejaVuSans', 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONT', (0, -1), (-1, -1), 'DejaVuSans-Bold'),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.5*cm))

    total_cash = total_sales - total_expenses + data['cash_balance']
    
    elements.append(Paragraph("Остатки:", styles['CustomNormal']))
    elements.append(Spacer(1, 0.3*cm))
    
    cash_table_data = [
        ['Остаток налички в кассе:', f"{data['cash_balance']:.2f} ₸"],
        ['Итого в кассе:', f"{total_cash:.2f} ₸"]
    ]
    
    cash_table = Table(cash_table_data, colWidths=[10*cm, 5*cm])
    cash_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'DejaVuSans', 10),
        ('FONT', (0, 1), (-1, 1), 'DejaVuSans-Bold', 11),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('BACKGROUND', (1, 1), (1, 1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(cash_table)
    elements.append(Spacer(1, 0.8*cm))
    
    elements.append(Paragraph("Остатки в банках:", styles['CustomNormal']))
    elements.append(Spacer(1, 0.3*cm))
    
    bank_table_data = [
        ['Halyk Bank:', f"{data['halyk_balance']:.2f} ₸"],
        ['BCC:', f"{data['bcc_balance']:.2f} ₸"],
        ['Kaspi Bank:', f"{data['kaspi_balance']:.2f} ₸"]
    ]
    
    bank_table = Table(bank_table_data, colWidths=[10*cm, 5*cm])
    bank_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'DejaVuSans', 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('BACKGROUND', (1, 0), (1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.grey),
        ('LINEBELOW', (0, 1), (-1, 1), 2, colors.grey),
    ]))
    elements.append(bank_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/submit', methods=['POST'])
def submit_report():
    try:
        data = request.get_json()
        print("Получены данные:", data)
        
        if not data or not all(key in data for key in ['fio', 'datetime', 'sales', 'expenses', 'cash_balance', 'halyk_balance', 'bcc_balance', 'kaspi_balance']):
            return jsonify({'error': 'Недостаточно данных'}), 400
        
        if not isinstance(data['sales'], list) or len(data['sales']) == 0:
            return jsonify({'error': 'Необходимо добавить хотя бы одну продажу'}), 400
        
        if not isinstance(data['expenses'], list) or len(data['expenses']) == 0:
            return jsonify({'error': 'Необходимо добавить хотя бы один расход'}), 400
        
        validated_data = {
            'fio': str(data['fio']).strip(),
            'datetime': str(data['datetime']),
            'sales': [],
            'expenses': [],
            'cash_balance': 0,
            'halyk_balance': 0,
            'bcc_balance': 0,
            'kaspi_balance': 0
        }
        
        if not validated_data['fio']:
            return jsonify({'error': 'ФИО сотрудника не может быть пустым'}), 400
        
        for sale in data['sales']:
            if not all(key in sale for key in ['item', 'quantity', 'price']):
                return jsonify({'error': 'Неполные данные продажи'}), 400
            try:
                quantity = int(sale['quantity'])
                price = float(sale['price'])
                if quantity <= 0 or price < 0:
                    return jsonify({'error': 'Количество должно быть больше 0, цена не может быть отрицательной'}), 400
                validated_data['sales'].append({
                    'item': str(sale['item']).strip(),
                    'quantity': quantity,
                    'price': price
                })
            except (ValueError, TypeError):
                return jsonify({'error': 'Неверный формат данных продажи'}), 400
        
        for expense in data['expenses']:
            if not all(key in expense for key in ['description', 'amount']):
                return jsonify({'error': 'Неполные данные расхода'}), 400
            try:
                amount = float(expense['amount'])
                if amount < 0:
                    return jsonify({'error': 'Сумма расхода не может быть отрицательной'}), 400
                validated_data['expenses'].append({
                    'description': str(expense['description']).strip(),
                    'amount': amount
                })
            except (ValueError, TypeError):
                return jsonify({'error': 'Неверный формат суммы расхода'}), 400
        
        try:
            validated_data['cash_balance'] = float(data['cash_balance'])
            validated_data['halyk_balance'] = float(data['halyk_balance'])
            validated_data['bcc_balance'] = float(data['bcc_balance'])
            validated_data['kaspi_balance'] = float(data['kaspi_balance'])
            
            if any(val < 0 for val in [validated_data['cash_balance'], validated_data['halyk_balance'], 
                                        validated_data['bcc_balance'], validated_data['kaspi_balance']]):
                return jsonify({'error': 'Остатки не могут быть отрицательными'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Неверный формат остатков'}), 400
        
        reports.append(validated_data)
        with open(REPORTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(reports, f, ensure_ascii=False, indent=2)
        
        pdf_buffer = generate_pdf(validated_data)
        
        if bot and TOKEN:
            try:
                pdf_filename = f"Отчёт_{validated_data['fio']}_{validated_data['datetime'].replace(' ', '_').replace(':', '-')}.pdf"
                pdf_buffer.name = pdf_filename
                bot.send_document(GROUP_ID, pdf_buffer)
                print("PDF отправлен в группу!")
                return jsonify({'message': 'Отчёт отправлен в группу в формате PDF'}), 200
            except Exception as e:
                print(f"Ошибка отправки в Telegram: {e}")
                return jsonify({'message': 'Отчёт сохранён, но не удалось отправить в Telegram. Проверьте токен бота.'}), 200
        else:
            print("Telegram bot токен не настроен")
            return jsonify({'message': 'Отчёт сохранён локально. Настройте TELEGRAM_BOT_TOKEN для отправки в Telegram.'}), 200
            
    except Exception as e:
        print(f"Ошибка: {e}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

if __name__ == '__main__':
    if bot and TOKEN:
        import threading
        threading.Thread(target=bot.infinity_polling, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
