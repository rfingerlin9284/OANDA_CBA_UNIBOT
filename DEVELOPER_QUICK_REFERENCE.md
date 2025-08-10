# 🛠️ DEVELOPMENTAL ENGINEER QUICK REFERENCE
**Wolfpack-Lite Live Trading System | Constitutional PIN: 841921**

---

## 🚀 QUICK DEPLOYMENT

### One-Command Setup
```bash
# Clone and deploy complete system
./deploy_wolfpack_live_system.sh
```

### Manual Step-by-Step
```bash
# 1. Environment Setup
python3 -m venv wolfpack_live_env
source wolfpack_live_env/bin/activate
pip install -r requirements.txt

# 2. Configure System
cp config/config_live.json.template config/config_live.json
# Edit credentials.py with live API keys

# 3. Initialize Database
python3 scripts/setup_database.py

# 4. Start System
./start_wolfpack_live.sh
```

---

## 🏗️ SYSTEM ARCHITECTURE OVERVIEW

### Core Components Map
```
main.py                    → Primary live trading controller
├── credentials.py         → Constitutional PIN: 841921 + API keys
├── coinbase_ed25519_auth.py → JWT ED25519 Coinbase authentication
├── go_live.py             → Live trading system launcher
├── executor.py            → Trade execution engine
├── guardian_fresh.py      → Safety monitoring system
├── dashboard/app.py       → Flask web interface (localhost:8000)
└── logger.py              → Comprehensive logging system
```

### Data Flow Architecture
```
Constitutional PIN (841921) → Credential Validation → API Authentication
    ↓
OANDA Forex API ←→ Trading Engine ←→ Coinbase Advanced Trade API
    ↓                    ↓                    ↓
FVG Signal Detection → ML Decision Filter → OCO Order Execution
    ↓                    ↓                    ↓
Risk Management → Portfolio Update → Dashboard Display
    ↓                    ↓                    ↓
Audit Logging → Database Storage → Performance Tracking
```

---

## 🎯 TRADING ENGINE COMPONENTS

### Signal Detection System
```python
# FVG (Fair Value Gap) Strategy
class FVGDetector:
    def __init__(self):
        self.min_gap_percent = 0.15      # 15 pips minimum
        self.max_fvg_age = 5             # 5 candles max age
        self.min_confluence_score = 7.0   # Minimum signal strength
    
    def detect_opportunities(self, market_data):
        # Core FVG detection logic
        gaps = self.find_price_gaps(market_data)
        return self.validate_confluence(gaps)
```

### Risk Management Engine
```python
# OCO (One Cancels Other) Mandatory Execution
class RiskManager:
    def __init__(self):
        self.risk_per_trade = 1.0        # 1% capital risk
        self.max_concurrent = 3          # Maximum 3 positions
        self.min_risk_reward = 2.5       # Minimum 1:2.5 R:R
        self.constitutional_pin = "841921"
    
    def calculate_position_size(self, account_balance, risk_percent):
        return account_balance * (risk_percent / 100)
```

### Authentication Protocol
```python
# ED25519 JWT Authentication for Coinbase
class CoinbaseAuth:
    def __init__(self):
        self.algorithm = "ed25519"
        self.jwt_expiry = 120           # 2 minutes
        self.constitutional_pin = "841921"
    
    def generate_jwt_token(self, method, path):
        # JWT generation with ED25519 signing
        return self.sign_request(method, path)
```

---

## 📊 CONFIGURATION MANAGEMENT

### Live Configuration (config_live.json)
```json
{
    "constitutional_pin": "841921",
    "trading_mode": "LIVE_ONLY",
    "risk_per_trade": 1.0,
    "max_concurrent_trades": 3,
    "min_risk_reward": 2.5,
    "oanda_environment": "live",
    "coinbase_algorithm": "ed25519"
}
```

### Environment Variables (.env)
```bash
CONSTITUTIONAL_PIN=841921
TRADING_MODE=LIVE_ONLY
FLASK_ENV=production
DASHBOARD_PORT=8000
LIVE_TRADING_ONLY=true
```

### Credentials Template (credentials.py)
```python
class WolfpackCredentials:
    # Constitutional Authorization
    CONSTITUTIONAL_PIN = "841921"
    
    # OANDA Live Trading
    OANDA_API_KEY = "your-live-api-key"
    OANDA_ACCOUNT_ID = "your-live-account-id"
    OANDA_ENVIRONMENT = "live"
    
    # Coinbase Advanced Trade (ED25519)
    COINBASE_API_KEY_ID = "your-api-key-id"
    COINBASE_PRIVATE_KEY = "your-ed25519-private-key"
```

---

## 🔧 SYSTEM MANAGEMENT

### Service Management
```bash
# Systemd Service
sudo systemctl start wolfpack-lite
sudo systemctl stop wolfpack-lite
sudo systemctl status wolfpack-lite
sudo journalctl -u wolfpack-lite -f

# Manual Control
./start_wolfpack_live.sh          # Start complete system
./scripts/start_dashboard.sh       # Dashboard only
./scripts/health_check.sh          # System health check
./scripts/backup_system.sh         # Create backup
```

### Log Management
```bash
# Real-time Logs
tail -f logs/trading.log           # Trading operations
tail -f logs/dashboard.log         # Dashboard activity
tail -f logs/auth.log              # Authentication events
tail -f logs/guardian.log          # Safety monitoring

# Log Rotation
./scripts/rotate_logs.sh           # Manual rotation
# Automatic: Daily at 2 AM via cron
```

### Database Operations
```bash
# Database Access
sqlite3 data/wolfpack_trading.db

# Common Queries
SELECT * FROM trades ORDER BY entry_time DESC LIMIT 10;
SELECT * FROM performance_metrics ORDER BY date DESC;
SELECT COUNT(*) as total_trades FROM trades WHERE constitutional_pin = '841921';
```

---

## 🛡️ SECURITY PROTOCOLS

### Constitutional PIN System
```python
# All operations require Constitutional PIN verification
def verify_constitutional_pin(pin):
    if pin != "841921":
        raise SecurityError("Invalid Constitutional PIN")
    return True

# Example usage in trading functions
def execute_trade(trade_data, constitutional_pin):
    verify_constitutional_pin(constitutional_pin)
    # Proceed with live trade execution
```

### Live Trading Validation
```python
def validate_live_mode():
    if not config.get('live_trading_only'):
        raise SecurityError("Live trading only mode required")
    
    if config.get('trading_mode') != 'LIVE_ONLY':
        raise SecurityError("Invalid trading mode")
    
    return True
```

### Emergency Protocols
```bash
# Emergency Stop
python3 kill_all_trades.py --constitutional-pin 841921

# Emergency Backup
./scripts/backup_system.sh

# System Recovery
python3 emergency_bail.py --constitutional-pin 841921
```

---

## 📈 PERFORMANCE MONITORING

### Dashboard Metrics (localhost:8000)
- **Real-time P&L**: Current profit/loss
- **Active Positions**: Open trades monitoring
- **Daily Statistics**: Win rate, trade count
- **System Health**: API status, connectivity
- **Risk Metrics**: Current exposure, remaining capacity
- **Performance Charts**: Historical performance visualization

### Key Performance Indicators
```python
# System Performance Metrics
current_metrics = {
    'total_trades': 6945,           # Completed trades
    'current_pnl': 248.99,          # Current profit
    'win_rate': 71.2,               # Success rate %
    'active_positions': 2,          # Open trades
    'daily_trades': 12,             # Today's trades
    'risk_utilization': 65.0,       # Risk capacity used %
    'system_uptime': 99.9,          # Operational uptime %
    'constitutional_status': 'VERIFIED'  # PIN status
}
```

### Performance Optimization
```python
# Trade Execution Optimization
def optimize_execution():
    # Minimize latency
    use_market_orders = True
    
    # Optimize position sizing
    dynamic_position_sizing = True
    
    # Enhanced signal filtering
    ml_confidence_threshold = 0.75
    
    # OCO order optimization
    intelligent_sl_tp_placement = True
```

---

## 🔍 TROUBLESHOOTING GUIDE

### Common Issues

#### Authentication Failures
```bash
# Check API credentials
python3 -c "from credentials import *; print('Credentials loaded')"

# Test OANDA connection
curl -H "Authorization: Bearer $OANDA_API_KEY" https://api-fxtrade.oanda.com/v3/accounts

# Test Coinbase ED25519
```

#### Dashboard Issues
```bash
# Check Flask process
ps aux | grep "dashboard/app.py"

# Test dashboard endpoint
curl -f http://localhost:8000/

# Restart dashboard
pkill -f "dashboard/app.py"
./scripts/start_dashboard.sh
```

#### Trading System Issues
```bash
# Check main process
ps aux | grep "main.py"

# Verify Constitutional PIN
grep -r "841921" logs/

# Check database connectivity
sqlite3 data/wolfpack_trading.db ".tables"
```

#### Performance Issues
```bash
# Monitor system resources
htop

# Check log file sizes
du -sh logs/*

# Monitor network connectivity
ping api-fxtrade.oanda.com
ping api.coinbase.com
```

### Diagnostic Commands
```bash
# Complete system diagnostic
./scripts/health_check.sh

# Detailed system status
python3 -c "
from dashboard.app import get_system_status
import json
print(json.dumps(get_system_status(), indent=2))
"

# Database integrity check
sqlite3 data/wolfpack_trading.db "PRAGMA integrity_check;"
```

---

## 🚀 DEVELOPMENT WORKFLOW

### Code Structure Standards
```python
# File header template
"""
🚀 WOLFPACK-LITE LIVE TRADING COMPONENT
Constitutional PIN: 841921
LIVE TRADING ONLY - NO DEMO/PRACTICE/SIMULATION

Component: [Component Name]
Purpose: [Component Purpose]
Author: Developmental Engineer
Date: $(date +%Y-%m-%d)
"""

# Import standards
import sys
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Constitutional validation
from credentials import WolfpackCredentials
```

### Testing Protocols
```python
    """Test live trading system with minimal risk"""
    
    # Validate Constitutional PIN
    assert verify_constitutional_pin("841921")
    
    # Test with minimum position size
        'pair': 'EUR_USD',
        'size': 100,  # Minimum units
        'constitutional_pin': '841921'
    }
    
    # Execute with full safety protocols
    return result
```

### Deployment Checklist
```markdown
- [ ] Constitutional PIN verified (841921)
- [ ] Live API credentials configured
- [ ] Database initialized and accessible
- [ ] Dashboard responsive at localhost:8000
- [ ] All core files present and executable
- [ ] Virtual environment activated
- [ ] Dependencies installed and up-to-date
- [ ] Log directories created and writable
- [ ] Systemd service configured (optional)
- [ ] Backup system functional
- [ ] Performance metrics baseline established
```

---

## 📞 SUPPORT & DOCUMENTATION

### System Documentation
- **WOLFPACK_LITE_SYSTEM_BLUEPRINT.md**: Complete system architecture
- **DEPLOYMENT_SUMMARY.md**: Post-deployment summary
- **config/config_live.json**: Live trading configuration
- **logs/**: Real-time system logs
- **scripts/**: Management and utility scripts

### Command Reference
```bash
# System Operations
./deploy_wolfpack_live_system.sh     # Full system deployment
./start_wolfpack_live.sh             # Start trading system
./scripts/health_check.sh            # System diagnostics
./scripts/backup_system.sh           # Create system backup

# Development Operations
python3 main.py --help               # Command line options
python3 go_live.py --constitutional-pin 841921  # Direct launch
python3 dashboard/app.py             # Dashboard standalone

# Maintenance Operations
./scripts/rotate_logs.sh             # Log rotation
./scripts/setup_cron.sh             # Automated maintenance
sudo systemctl restart wolfpack-lite # Service restart
```

### Emergency Contacts
```
🚨 EMERGENCY PROCEDURES:
1. Execute: python3 kill_all_trades.py --constitutional-pin 841921
2. Create backup: ./scripts/backup_system.sh
3. Document incident: echo "Emergency: $(date)" >> logs/emergency.log
4. Review logs: tail -f logs/trading.log
5. Verify system state: ./scripts/health_check.sh
```

---

**Constitutional PIN: 841921 | Live Trading Only**  
**System Status**: OPERATIONAL  
**Last Updated**: August 6, 2025  
**For Developmental Engineers Reference**
