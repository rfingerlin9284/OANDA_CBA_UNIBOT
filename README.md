# 🎯 WOLFPACK-LITE FVG SNIPER

**Aggressive FVG hunting system with mandatory OCO execution**

Live trading bot designed for 35-50% win rate with 1:3+ risk/reward ratio. Pure logic-based approach without ML complexity.

---

## 🚀 QUICK START

### 1. **Setup Environment**
```bash
# Navigate to wolfpack-lite directory
cd wolfpack-lite

# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. **Configure API Keys**
Edit `credentials.py` and replace the placeholder values:

```python
# OANDA Live Trading
OANDA_API_KEY = "your_actual_oanda_api_token"
OANDA_ACCOUNT_ID = "your_actual_account_id"

# Coinbase Advanced Trade
COINBASE_API_KEY = "your_actual_coinbase_key"
COINBASE_SECRET = "your_actual_coinbase_secret"
COINBASE_PASSPHRASE = "your_actual_passphrase"
SANDBOX_MODE = True  # Change to False for real money
```

### 3. **Test System**
```bash
```

### 4. **Start Live Trading**
```bash
# Launch the sniper bot
python main.py
```

---

## 🎯 SYSTEM OVERVIEW

### **Core Strategy**
- **FVG Detection**: Institutional-grade Fair Value Gap hunting
- **Confluence Validation**: RSI + momentum + proximity scoring
- **Mandatory OCO**: Every trade has stop-loss and take-profit
- **Smart Trailing**: Dynamic stop adjustment when in profit
- **Streak Scaling**: Position sizing based on win/loss streaks

### **Target Performance**
- **Win Rate**: 35-50%
- **Risk/Reward**: 1:3+ minimum
- **Daily Target**: $400 profit from $3-5k capital
- **Risk per Trade**: 1% of account balance

---

## 📊 TRADING PAIRS

### **Coinbase (Crypto)**
```
BTC/USD, ETH/USD, SOL/USD, ADA/USD, XRP/USD
DOGE/USD, AVAX/USD, DOT/USD, MATIC/USD, LINK/USD
```

### **OANDA (Forex)**
```
EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD
USD/CHF, NZD/USD, EUR/GBP, EUR/JPY, GBP/JPY
```

---

## ⚡ FEATURES

### **✅ FVG Detection**
- 3-candle sequence analysis
- Minimum gap requirements (0.15% of price)
- Momentum candle validation
- Unfilled gap confirmation

### **✅ Confluence Scoring (10-point scale)**
- RSI positioning (3 points)
- FVG gap size (2 points)
- Price proximity (2 points)
- Momentum alignment (2 points)
- FVG freshness (1 point)

### **✅ Risk Management**
- Mandatory stop-loss on every trade
- Position sizing based on account risk
- Win/loss streak position scaling
- Maximum concurrent trades limit

### **✅ Smart Execution**
- Real-time OCO bracket orders
- Trailing stop when 50%+ profit
- Emergency close all function
- Comprehensive trade logging

---

## 📈 LIVE MONITORING

### **Terminal Output**
- Real-time trade notifications with colors
- P&L tracking with running balance
- Signal detection with confluence scores
- Error logging and system status

### **Log Files**
```
logs/trade_log.txt       # All trade activity
logs/pnl_log.txt         # Profit/loss history
logs/missed_log.txt      # Missed opportunities
logs/streak_data.json    # Performance analytics
```

### **Daily Stats Display**
```
📊 WOLFPACK-LITE DAILY STATS
💰 Balance: $3,247.50
📈 Total P&L: +$247.50
🎯 Trades: 12 | Win Rate: 41.7%
🔥 Win Streak: 3 | Loss Streak: 0
🏆 Best Streak: 5 | Worst: -2
⚡ Current Multiplier: 1.25x
```

---

## 🛠️ FILE STRUCTURE

```
wolfpack-lite/
├── main.py              # Master control system
├── credentials.py       # API keys and configuration
├── sniper_core.py       # FVG detection logic
├── oco_executor.py      # OCO trading engine
├── logger.py            # Logging and analytics
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── venv/               # Virtual environment
└── logs/               # Trade logs and analytics
    ├── trade_log.txt
    ├── pnl_log.txt
    ├── missed_log.txt
    └── streak_data.json
```

---

## 🔧 CONFIGURATION

### **Risk Settings** (`credentials.py`)
```python
STARTING_CAPITAL = 3000      # Starting balance
RISK_PER_TRADE = 1.0        # 1% risk per trade
MIN_RISK_REWARD = 2.5       # Minimum 1:2.5 R:R
MIN_CONFLUENCE_SCORE = 7.0   # Entry threshold
SCAN_INTERVAL = 2           # Seconds between scans
```

### **Streak Scaling**
```python
# Position size multipliers
WIN_STREAK_3+ = 1.25x       # +25% after 3 wins
WIN_STREAK_5+ = 1.4x        # +40% after 5 wins
LOSS_STREAK_2+ = 0.5x       # -50% after 2 losses
```

---

## 🚨 SAFETY FEATURES

### **Emergency Controls**
- **Ctrl+C**: Graceful shutdown with position monitoring
- **Emergency Close**: `oco_executor.emergency_close_all()`
- **Rate Limiting**: Built-in API request throttling
- **Error Recovery**: Automatic retry on connection issues

### **Position Limits**
- Maximum 3 concurrent trades
- Maximum 10 trades per day
- Automatic position scaling based on performance
- Stop-loss mandatory on every trade

---

## 📱 OPERATION COMMANDS

### **Start Trading**
```bash
cd wolfpack-lite
source venv/bin/activate
python main.py
```

### **Run Tests**
```bash
```

### **Check Logs**
```bash
# Live trade log
tail -f logs/trade_log.txt

# P&L history
tail -f logs/pnl_log.txt

# Performance data
cat logs/streak_data.json
```

### **Emergency Stop**
```bash
# Graceful shutdown
Ctrl+C

# Force kill (if needed)
pkill -f "python main.py"
```

---

## 🔍 TROUBLESHOOTING

### **Common Issues**

**Import Errors**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**API Connection Failed**
- Verify API keys in `credentials.py`
- Check internet connection
- Confirm API permissions (trading enabled)
- Validate account IDs

**No Signals Generated**
- FVGs are rare - expect 5-15 signals per day
- Lower `MIN_CONFLUENCE_SCORE` if needed
- Check if pairs are actively trading (market hours)

**OCO Orders Failing**
- Verify account has sufficient balance
- Check minimum order sizes for pairs
- Ensure stop-loss/take-profit levels are valid

---

## 📊 PERFORMANCE MONITORING

### **Key Metrics**
- **Win Rate**: Target 35-50%
- **Average R:R**: Target 3.0+
- **Daily Profit**: Target $400 from $3k capital
- **Maximum Drawdown**: Monitor < 10%

### **Optimization Guidelines**
1. **Confluence Threshold**: Adjust `MIN_CONFLUENCE_SCORE` based on signal frequency
2. **Risk Per Trade**: Increase gradually as account grows
3. **Pair Selection**: Focus on most liquid pairs during your trading hours
4. **Timeframes**: 5M charts for entries, monitor 1H for trend alignment

---

## ⚠️ IMPORTANT DISCLAIMERS

1. **Risk Warning**: Trading involves substantial risk of loss
3. **Market Conditions**: Performance varies with volatility
4. **Capital Requirements**: Recommended minimum $3,000 for proper position sizing
5. **Monitoring Required**: Bot requires periodic supervision

---

## 🏆 ACHIEVEMENT TARGETS

### **Week 1 Goals**
- [ ] Generate 20+ signals with >7.0 confluence
- [ ] Achieve 40%+ win rate
- [ ] Maintain 1:3+ average R:R

### **Month 1 Goals** 
- [ ] Transition to live trading
- [ ] Consistent daily profitability
- [ ] Optimize for your trading schedule
- [ ] Build performance analytics

### **Advanced Features** (Future)
- Web dashboard interface
- Multi-timeframe confluence
- News sentiment integration
- Portfolio correlation analysis

---

**🎯 Ready to hunt FVGs like the institutions! Good luck!**
