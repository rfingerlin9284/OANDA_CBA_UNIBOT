# 🐺 Wolfpack-Lite: Live FVG Sniper System

## 🎯 Strategy Overview
**Simple enough to be bulletproof. Smart enough to snipe.**

### Fair Value Gap (FVG) Rules - Explicitly Defined:
- **Timeframe**: 5-minute candles
- **Bullish FVG**: `Candle1.high < Candle3.low` AND `Candle2.close < Candle3.close`
- **Bearish FVG**: `Candle1.low > Candle3.high` AND `Candle2.close > Candle3.close`
- **Gap Threshold**: Must be ≥ 0.2% of asset price
- **Entry**: Mid-gap = `(Candle1.extreme + Candle3.extreme) / 2`
- **Stop Loss**: Candle1.extreme (opposite side of gap)
- **Take Profit**: 1:3 Risk-Reward ratio minimum
- **Min Confidence**: 80% (FVG + Fibonacci + RSI confluence)

---

## 📊 Market Coverage

### OANDA Forex (12 pairs):
```
EUR/USD, GBP/USD, USD/JPY, USD/CHF, AUD/USD, USD/CAD, 
NZD/USD, EUR/GBP, EUR/JPY, GBP/JPY, AUD/JPY, EUR/AUD
```

### Coinbase Spot Crypto (8 pairs):
```
BTC/USD, ETH/USD, SOL/USD, ADA/USD, 
DOT/USD, AVAX/USD, MATIC/USD, LINK/USD
```

**NO PERPS/MARGIN** - Spot trading only = safer, no liquidation risk

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Credentials
Edit `credentials.py` with your **LIVE** API keys:
```python
# LIVE OANDA credentials
OANDA_API_KEY = "your_live_oanda_api_key"
OANDA_ACCOUNT_ID = "your_live_account_id"

# LIVE Coinbase credentials  
COINBASE_API_KEY = "your_live_coinbase_api_key"
COINBASE_SECRET = "your_live_secret"
COINBASE_PASSPHRASE = "your_live_passphrase"
```

### 3. Start Live Trading
```bash
./start_sniper.sh
```

---

## 📁 File Structure

```
wolfpack-lite/
├── fvg_strategy.py      # Core FVG detection with explicit rules
├── oanda_sniper.py      # OANDA forex scanner (LIVE only)
├── coinbase_sniper.py   # Coinbase spot scanner (LIVE only)
├── executor.py          # OCO trade execution (LIVE only)
├── credentials.py       # LIVE API credentials
├── logger.py            # Trade logging and PnL tracking
├── start_sniper.sh      # Launch both snipers
├── requirements.txt     # Python dependencies
└── logs/               # Trade logs and performance data
```

---

## 🔐 Security & Risk Management

### Position Sizing:
- **Fixed 1% risk per trade** based on account balance
- **Auto-calculated position sizes** based on stop-loss distance
- **Max 1 trade per pair** - no doubling down

### OCO Protection:
- **Mandatory stop-loss** on every trade
- **1:3 minimum Risk:Reward** ratio
- **Auto-cancellation** if OCO fails to attach

### Account Monitoring:
- **Real-time balance checks** every 10 scans
- **Daily loss limits** (configurable)
- **Heartbeat monitoring** to detect stalled bots

---

## 📊 Signal Confluence System

### Base Score: 50% (Valid FVG detected)
- **+10%** if gap size > 0.3%
- **+10%** if RSI confirms direction (>50 bullish, <50 bearish)  
- **+10%** if price above/below EMA21
- **+10%** if ATR shows sufficient volatility (≥0.5%)
- **+10%** if entry near Fibonacci 61.8% or 78.6% levels

### Minimum 80% confidence required for trade execution

---

## 🧪 Testing & Validation

### Run System Test:
```bash
```

### Test Individual Components:
```bash
# Test FVG strategy
python fvg_strategy.py

# Test OANDA connection
python oanda_sniper.py

# Test Coinbase connection  
python coinbase_sniper.py
```

---

## 📈 Live Trading Features

### Real-Time Scanning:
- **10-second intervals** for OANDA forex
- **12-second intervals** for Coinbase crypto (rate limit friendly)
- **Parallel processing** of all pairs
- **Active trade tracking** to prevent overlapping positions

### Smart Execution:
- **Market orders** with immediate OCO attachment
- **Position size calculation** based on account balance
- **Trade confirmation** logging with all parameters

### Performance Tracking:
- **Real-time PnL** calculations
- **Win rate statistics** per pair
- **Streak multipliers** for hot streaks
- **Daily performance** summaries

---

## ⚠️ Important Warnings

### 🚨 LIVE TRADING ONLY
- **Mandatory OCO orders** - trades cancelled if SL/TP fails

### 💰 Risk Disclaimer
- **Past performance ≠ future results**
- **Only trade with capital you can afford to lose**
- **Start with small position sizes** until system is proven
- **Monitor trades actively** - don't set and forget

---

## 🔧 Future Expansion (Planned)

### Perps/Derivatives Support:
- Coinbase CDP API integration
- Funding rate monitoring
- Liquidation protection logic

### Advanced Features:
- Multi-timeframe analysis
- Machine learning confidence scoring
- Smart trailing stops
- Portfolio correlation analysis

**For now: Spot markets provide safer, simpler real money trading.**

---

## 📞 Support

### Logs Location:
```bash
tail -f logs/trades.log     # Live trade log
tail -f logs/signals.log    # Signal detection log
tail -f logs/errors.log     # Error tracking
```

### Manual Override:
```bash
kill [PID]                  # Stop individual sniper
pkill -f "python.*sniper"   # Stop all snipers
```

---

**🐺 Ready to hunt FVG setups with real money - stay sharp, stay profitable!**
