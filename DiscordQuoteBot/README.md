# Daily Report System

A web-based application for creating daily financial reports with automatic PDF generation and Telegram delivery.

## Features

✅ **Responsive Web Form** - Bootstrap 5-powered interface for easy data entry  
✅ **Dynamic Data Entry** - Add/remove sales items and expenses on the fly  
✅ **Real-time Calculations** - Automatic totals for sales, expenses, and cash balance  
✅ **PDF Generation** - Professional reports with tables and formatted data  
✅ **Telegram Integration** - Automatic delivery to your group  
✅ **Robust Validation** - Comprehensive input validation and error handling  
✅ **Timezone Support** - Configured for UTC+5  
✅ **Currency Formatting** - Kazakh Tenge (₸) display

## How to Use

1. **Open the Application** - Click the web preview to access the form
2. **Fill in the Report:**
   - Employee name (ФИО сотрудника)
   - Sales items (товар, количество, цена)
   - Expenses (описание, сумма)
   - Cash and bank balances
3. **Submit** - The report will be saved and sent to your Telegram group

## Telegram Setup

Your bot is configured with the `TELEGRAM_BOT_TOKEN` secret. To receive reports:

1. Make sure your bot is added to the target Telegram group
2. Ensure the bot has permission to send messages
3. Update the `GROUP_ID` in `app.py` if needed (currently: -1003095770924)

## Technical Stack

- **Backend**: Flask with Python 3.11
- **PDF Generation**: reportlab
- **Telegram**: pyTelegramBotAPI
- **Frontend**: Bootstrap 5 + Vanilla JavaScript
- **Storage**: JSON-based persistence

## Project Structure

```
├── app.py          # Flask backend with PDF and Telegram integration
├── index.html      # Frontend form
├── reports.json    # Stored reports (auto-generated)
├── replit.md      # Project documentation
└── README.md      # This file
```

## Data Validation

The system includes comprehensive validation:
- All numeric fields are type-checked and converted safely
- No negative values allowed for prices or balances
- Quantities must be greater than 0
- All required fields are validated
- Meaningful error messages for invalid input

## Next Steps

To customize the application:
- Update `GROUP_ID` in `app.py` for your Telegram group
- Modify the PDF layout in the `generate_pdf()` function
- Add more fields or calculations as needed
- Export report history to Excel/CSV
- Add user authentication

## Publishing

When ready to deploy, click the **Deploy** button to publish your application with a live URL!
