# Daily Report System

## Overview
A Flask-based web application for creating daily financial reports with automatic PDF generation and Telegram delivery. Designed for business teams to submit daily sales, expenses, and bank balances, with reports automatically sent to a Telegram group.

## Features
- **Web Form**: Bootstrap 5-powered responsive form for data entry
- **Dynamic Data Entry**: Add/remove sales items and expenses on the fly
- **Real-time Calculations**: Automatic totals for sales, expenses, and cash balance
- **PDF Generation**: Professional PDF reports with tables using reportlab
- **Telegram Integration**: Automatic delivery of PDF reports to specified Telegram group
- **Data Storage**: JSON-based report history
- **Multi-currency**: Kazakh Tenge (₸) formatting
- **Timezone**: Configured for UTC+5

## Project Structure
```
.
├── app.py              # Flask backend with PDF generation and Telegram bot
├── index.html          # Frontend form with Bootstrap 5
├── reports.json        # Stored reports (auto-generated)
├── .gitignore         # Git ignore configuration
├── pyproject.toml     # Python dependencies (auto-managed)
└── replit.md          # This file
```

## Recent Changes
- **2025-10-17**: Initial setup on Replit
  - Installed Flask, pyTelegramBotAPI, and reportlab
  - Created Flask backend with PDF generation and robust validation
  - Built responsive HTML form with Bootstrap 5
  - Configured Telegram bot integration with proper error handling
  - Fixed timezone calculation to accurately display UTC+5
  - Added comprehensive input validation to prevent server errors
  - Set up workflow to run on port 5000

## Validation Features
- Type checking and conversion for all numeric inputs
- Range validation (no negative values, quantities > 0)
- Proper error messages returned as 400 Bad Request
- Prevents PDF generation crashes from malformed data
- Sanitizes text inputs and validates required fields

## Configuration
### Environment Variables
- `TELEGRAM_BOT_TOKEN`: Bot token from @BotFather (required for Telegram delivery)
- `SESSION_SECRET`: Flask session secret (auto-configured)

### Telegram Setup
1. Create bot via @BotFather in Telegram
2. Add bot to your target group
3. Get group ID (currently configured: -1003095770924)
4. Update GROUP_ID in app.py if needed
5. Ensure bot has admin rights to send messages

## Usage
1. Open the web application
2. Fill in employee name (ФИО сотрудника)
3. Add sales items with quantity and price
4. Add expense descriptions with amounts
5. Enter cash balance and bank balances (Halyk, BCC, Kaspi)
6. Submit to generate PDF and send to Telegram group

## Report Format
The PDF includes:
- Employee name and timestamp
- Sales table with items, quantities, prices, and totals
- Expenses table with descriptions and amounts
- Cash balance calculation: Sales - Expenses + Cash Balance
- Bank balances for Halyk Bank, BCC, and Kaspi Bank

## Technical Details
- **Framework**: Flask 3.x
- **Frontend**: Vanilla JavaScript + Bootstrap 5
- **PDF Library**: reportlab 4.x
- **Bot Library**: pyTelegramBotAPI 4.x
- **Storage**: JSON file (reports.json)
- **Port**: 5000 (configured for Replit)

## Future Enhancements
- SQLite database for scalable storage
- Report history viewing and search
- User authentication system
- Data visualization dashboard
- Export to Excel/CSV formats
- Multi-language support
