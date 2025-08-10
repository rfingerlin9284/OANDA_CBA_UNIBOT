# 🎯 FVG Dashboard Integration Guide

## 📊 Real-Time FVG Monitoring Dashboards

Your wolfpack-lite system now includes live FVG monitoring dashboards that display:

- **Live FVG signals** as they're detected
- **Entry, SL, TP levels** for each signal  
- **Confidence scores** and trade status
- **Active trade counts** across platforms
- **Real-time updates** every 10 seconds

---

## 🚀 Quick Start

### Launch Individual Dashboards
```bash
# OANDA Forex Dashboard
python dashboards/oanda_fvg_cli.py

# Coinbase Spot Crypto Dashboard  
python dashboards/coinbase_fvg_cli.py
```

### Launch Both Dashboards (Recommended)
```bash
./launch_dashboards.sh
```

---

## 🔧 Integration with Your Sniper Bots

### Step 1: Import the Feed Updater
Add this to your `main.py` or sniper bot files:

```python
from dashboards.feed_updater import FVGDashboardFeeder

# Initialize dashboard feeder
dashboard_feeder = FVGDashboardFeeder()
```

### Step 2: Update Dashboard When FVG Detected

**For OANDA signals:**
```python
# When your OANDA sniper detects an FVG
if fvg_signal:
    signal_data = {
        "direction": fvg_signal["type"],  # "BUY" or "SELL"
        "confidence": fvg_signal["signal_strength"],
        "entry": fvg_signal["entry_price"],
        "sl": fvg_signal["stop_loss"],
        "tp": fvg_signal["take_profit"],
        "status": "PENDING",  # or "ACTIVE" if trade placed
        "reason": "Bullish FVG + RSI Confluence"
    }
    
    dashboard_feeder.update_oanda_feed(pair, signal_data, active_trades_count)
```

**For Coinbase signals:**
```python
# When your Coinbase sniper detects an FVG
if fvg_signal:
    signal_data = {
        "direction": fvg_signal["type"],  # "BUY" or "SELL"
        "confidence": fvg_signal["signal_strength"],
        "entry": fvg_signal["entry_price"],
        "sl": fvg_signal["stop_loss"],
        "tp": fvg_signal["take_profit"],
        "status": "PENDING",  # or "ACTIVE" if trade placed
        "reason": "Bearish FVG + EMA Break"
    }
    
    dashboard_feeder.update_coinbase_feed(pair, signal_data, active_trades_count)
```

### Step 3: Clear Signals When Trades Close
```python
# When a trade closes or signal expires
dashboard_feeder.clear_pair_signal("EUR/USD", platform="oanda")
dashboard_feeder.clear_pair_signal("BTC-USD", platform="coinbase")
```

### Step 4: Update System Status
```python
# Keep dashboards updated with system status
dashboard_feeder.update_system_status("oanda", "LIVE SCANNING", active_trades=2)
dashboard_feeder.update_system_status("coinbase", "LIVE SCANNING", active_trades=1)
```

---

## 📁 Dashboard Files

```
dashboards/
├── oanda_fvg_cli.py           # OANDA terminal dashboard
├── coinbase_fvg_cli.py        # Coinbase terminal dashboard  
├── feed_updater.py            # Integration helper
├── fvg_feed_oanda.json        # OANDA data feed
├── fvg_feed_coinbase.json     # Coinbase data feed
└── launch_dashboards.sh       # Dashboard launcher
```

---

## 🎨 Dashboard Features

### OANDA Dashboard
- 💱 **Forex pairs** (EUR/USD, GBP/USD, etc.)
- 🎯 **5-decimal precision** for forex pricing
- 🔴 **Live trading warnings**
- 📊 **Real-time confidence scoring**

### Coinbase Dashboard  
- 💰 **Spot crypto pairs** (BTC-USD, ETH-USD, etc.)
- 💲 **USD pricing** with 2-decimal precision
- 🚫 **NO PERPS/MARGIN** - spot only
- 📈 **Live market status**

---

## 🔥 Pro Tips

1. **Run dashboards on separate terminals** while your bots trade
2. **Monitor confidence scores** - only signals >0.8 should trade
3. **Check active trade counts** to avoid overexposure
4. **Use tmux/screen** for persistent dashboard sessions
5. **Dashboard updates every 10 seconds** - no manual refresh needed

---

## ⚠️ Dashboard Safety

- **Real money monitoring** - all signals are live
- **Platform separation** - OANDA and Coinbase feeds isolated
- **No trading execution** - dashboards are view-only

---

**🎯 Your FVG snipers can now feed live data to beautiful terminal dashboards!**
