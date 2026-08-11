# 🤖 XAUUSD Trading Analysis Bot

Telegram Bot for Gold Technical Analysis

## Features

✅ Technical Analysis with 5 Indicators
✅ Real-time Market Data
✅ Money Management (3% Risk)
✅ Quick Alerts on Signals
✅ Support for Multiple Timeframes (1m, 5m)

## Commands

- `/start` - Start the bot
- `/help` - Show help and commands
- `/status` - Check bot status
- `/analyze` - Current XAUUSD analysis

## Setup

### Environment Variables

Set these in your hosting platform (Render/Heroku):

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### Installation

```bash
pip install -r requirements.txt
python trading_bot.py
```

## Configuration

### Default Bot Token
```
8757189559:AAFw0VLGnEwKBtxqIWwTouB9nJxz6IBPXn0
```

### Money Management Settings
- Risk Percentage: 3%
- Min Account: $100
- Max Account: $500

### Indicators
- RSI (14 periods)
- MACD (12,26,9)
- Bollinger Bands (20,2)
- EMA (20,50)
- Stochastic (14)

## Files

- `trading_bot.py` - Main bot application
- `requirements.txt` - Python dependencies
- `Procfile` - Deployment configuration
- `README.md` - Documentation

## Deployment

### Render
1. Connect GitHub repository
2. Set environment variables
3. Deploy

### Heroku
1. Connect GitHub repository
2. Set config vars
3. Deploy

## Disclaimer

⚠️ This bot is for **educational purposes only**.
- Not financial advice
- Trade at your own risk
- Use demo accounts first
- Never risk money you can't afford to lose

## Support

For issues and questions: @TradingbyshadiBot

---

Built with ❤️ by Shadi Mahmoud 🇵🇸

**Made for traders, by traders**
