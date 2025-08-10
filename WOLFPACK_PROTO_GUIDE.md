# 🚀 WOLFPACK-PROTO: Enhanced Autonomous Trading System

## 🌟 Mass Psychology Quantifier Edition

This is the enhanced version of the Wolfpack trading system that quantifies human market psychology through algorithmic precision. The system combines day trading intuition with 24/7 execution across OANDA's forex markets and Coinbase's crypto markets.

## 🧠 Core Psychology Quantification

### Mass Market Behavior Analysis
- **FVG Gaps**: Institutional imbalances revealing crowd sentiment crystallization
- **RSI Levels**: Herd overreactions (oversold panic, overbought euphoria)
- **Volume Surges**: Breakout frenzies and crowd participation
- **Fibonacci Zones**: Exhaustion points where psychology shifts
- **EMA Alignment**: Trend-follower positioning and alignment
- **Gap Size Weighting**: Larger displacements = higher psychological urgency

### Platform-Specific Psychology
- **Crypto (Coinbase)**: Momentum focus - thin books create whipsaws, volume surges signal breakouts
- **Forex (OANDA)**: Mean reversion - deep liquidity favors range-bound behavior

## 🔥 Enhanced Features

### 1. Dynamic OCO Wave Riders
- **Initial Setup**: 1:3 RR OCO with stop loss and take profit
- **Wave Activation**: At 2.5R profit, automatically remove TP cap
- **Trail Logic**: 1.25% trailing below peak (buys) or above peak (sells)
- **Peak Tracking**: Real-time monitoring every 15 seconds
- **Breakeven Protection**: Move SL to breakeven after 2R profit

### 2. Market-Aware FVG Scoring
- **Crypto Momentum Boost**: +0.4 score for RSI>60 + volume>2x + EMA alignment
- **Forex Mean Reversion**: +0.3 score for RSI extremes + EMA alignment
- **Volume Surge Filter**: Crypto signals require >2x average volume
- **Gap Psychology**: Larger gaps get +0.3 to +0.6 score boost

### 3. Session-Aware Bias Dispatch
- **Bullish Sessions**: Wider SL (1.005x) to give room for climbs
- **Bearish Sessions**: Tighter SL (0.995x) for quick drops
- **Momentum Periods**: London/NY overlap favors breakouts
- **Range Periods**: Asian session favors mean reversion

### 4. Lock Mode for Ultra Signals
- **Activation**: Signal strength ≥9.0 OR RR≥3.0 OR psychology score≥5.0
- **Behavior**: No TP from start, pure trailing only
- **Purpose**: Let exceptional setups run unlimited

### 5. OCO Guardian Watchdog
- **Compliance**: Ensures every trade has proper OCO protection
- **Auto-Kill**: Removes orphaned positions without SL/TP
- **Heartbeat**: 15-second health checks with dashboard updates
- **Emergency**: Automatic shutdown after 5 OCO violations

### 6. Enhanced Dashboard Integration
- **Trail Status**: 🟢 Trail Active, 🟡 Ready to Trail, 🔴 Static
- **Psychology Scores**: Real-time gap analysis and volume surge indicators
- **Session Info**: Current market session and bias recommendations
- **Performance**: Signal rates, execution rates, R:R tracking

## 📊 Trading Configuration

### Risk Management
- **Risk Per Trade**: 1% of capital
- **Minimum RR**: 1:3 (configurable)
- **Maximum Concurrent**: 3 positions
- **Streak Scaling**: Win streaks increase position size

### Signal Requirements
- **Minimum Confluence**: 7.0 (enhanced scoring)
- **FVG Gap Size**: ≥0.15% of current price
- **Volume Surge**: >2x average (crypto only)
- **Psychology Score**: Integrated into confluence

### Wave Ride Settings
- **Threshold**: 2.5R profit to activate
- **Trail Distance**: 1.25% below/above peak
- **Update Frequency**: Every 15 seconds
- **Lock Mode**: Ultra-high probability signals

## 🌍 Session-Aware Trading

### Hamilton, NJ Timezone Focus
- **London Session** (3AM-12PM EST): Breakout hunting
- **NY Session** (8AM-5PM EST): Trend continuation/reversal
- **London/NY Overlap** (8AM-12PM EST): Maximum volatility, momentum
- **Asian Session** (7PM-4AM EST): Range trading, mean reversion

### Bias Dispatch Rules
- **Momentum Bias**: Wider SL, faster scanning, lower confluence threshold
- **Range Bias**: Tighter SL, slower scanning, higher confluence threshold
- **Breakout Bias**: High threshold, quality over quantity
- **Reversal Bias**: Very high threshold, counter-trend setups

## 🚀 Quick Start Guide

### 1. Configure Credentials
Edit `credentials.py` with your live API keys:
```python
# OANDA Live Credentials
OANDA_API_KEY = "your-live-key"
OANDA_ACCOUNT_ID = "your-account-id"

# Coinbase Advanced Trade Credentials  
COINBASE_API_KEY = "your-api-key"
COINBASE_PRIVATE_KEY_B64 = "your-ed25519-private-key"
```

### 2. Install Dependencies
```bash
pip install ccxt oandapyV20 pandas numpy ta cryptography PyJWT pycryptodome rich pytz requests
```

### 3. Launch System
```bash
chmod +x start_wolfpack_proto.sh
./start_wolfpack_proto.sh
```

### 4. Monitor Performance
```bash
# Watch live logs
tail -f logs/trade_log.txt

# Monitor heartbeat
tail -f logs/heartbeat.log

# Check position status
python3 -c "from position_tracker import print_daily_summary; print_daily_summary()"
```

## ⚠️ Live Trading Warnings

### Real Money Trading
- This system executes real trades with real money
- Start with small position sizes to validate performance
- Monitor drawdowns and performance metrics closely
- Understand the risks of automated trading

### Market Risks
- Crypto markets: High volatility, potential for large gaps
- Forex markets: Weekend gaps, news events can cause slippage
- System failures: Internet, power, or API outages can affect performance

### Compliance
- Ensure trading is legal in your jurisdiction
- Understand tax implications of automated trading
- Keep detailed records for compliance

## 📈 Performance Expectations

### Target Metrics
- **Win Rate**: 35-50% (high RR compensates for lower win rate)
- **Average RR**: 1:3 to 1:5 (wave riding extends winners)
- **Daily Profit**: $400+ target with proper risk management
- **Maximum Drawdown**: <15% with proper position sizing

### Psychology Edge
- Quantifies crowd behavior patterns
- Adapts to different market personalities (crypto vs forex)
- Session-aware timing for optimal entry conditions
- Wave riding captures extended momentum moves

## 🛠️ Advanced Configuration

### Customizing Psychology Scoring
```python
# In sniper_core.py - adjust psychology weights
GAP_SIZE_WEIGHT = 0.3          # Boost for larger gaps
VOLUME_SURGE_MULTIPLIER = 2.0  # Volume threshold for crypto
MOMENTUM_BOOST = 0.4           # Crypto momentum bonus
REVERSION_BOOST = 0.3          # Forex mean reversion bonus
```

### Adjusting Wave Ride Settings
```python
# In credentials.py
WAVE_RIDE_THRESHOLD = 2.5      # R:R to activate wave riding
TRAIL_PERCENT = 0.0125         # 1.25% trailing distance
LOCK_MODE_THRESHOLD = 9.0      # Signal strength for lock mode
```

### Session Bias Adjustments
```python
# In credentials.py
BULL_SL_ADJUSTMENT = 1.005     # Wider SL in bull markets
BEAR_SL_ADJUSTMENT = 0.995     # Tighter SL in bear markets
```

## 📚 Additional Resources

- **System Architecture**: See `COMPLETE_SYSTEM_AUDIT.md`
- **Performance Analysis**: See `DETAILED_PERFORMANCE_ANALYSIS.md`
- **API Documentation**: Coinbase Advanced Trade, OANDA v20 APIs

## 🔧 Troubleshooting

### Common Issues
1. **Credential Errors**: Verify API keys and permissions
2. **OCO Violations**: Check trade guardian logs for compliance issues
3. **Connection Issues**: Monitor API rate limits and connectivity
4. **Performance Issues**: Review position sizing and risk management

### Emergency Commands
```bash
# Emergency stop all trading
killall python3

# Check running processes
ps aux | grep python

# Force close positions (if system accessible)
python3 -c "from main import WolfpackProto; w=WolfpackProto(); w.emergency_stop()"
```

---

**🐺 The wolfpack's psychological edge is now eternal. Deploy with dominance!**
