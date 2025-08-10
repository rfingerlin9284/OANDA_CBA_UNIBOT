#!/bin/bash
# 🚀 WOLFPACK-LITE LIVE TRADING DEPLOYMENT SCRIPT
# Constitutional PIN: 841921
# LIVE TRADING ONLY - NO DEMO/PRACTICE/SIMULATION LOGIC
# Built for developmental engineers reference and deployment

set -euo pipefail

# ==================== SYSTEM CONFIGURATION ====================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="${SCRIPT_DIR}/deployment_${TIMESTAMP}.log"
CONSTITUTIONAL_PIN="841921"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# ==================== LOGGING FUNCTIONS ====================
log() {
    echo -e "${CYAN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}❌ $1${NC}" | tee -a "$LOG_FILE"
}

log_header() {
    echo -e "${BOLD}${BLUE}$1${NC}" | tee -a "$LOG_FILE"
}

# ==================== BANNER ====================
display_banner() {
    echo -e "${BOLD}${PURPLE}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║               🚀 WOLFPACK-LITE DEPLOYMENT                    ║
║                                                              ║
║                  LIVE TRADING SYSTEM                         ║
║              Constitutional PIN: 841921                      ║
║                                                              ║
║    🎯 OANDA Forex + Coinbase Advanced Trade                  ║
║    💰 6,945+ Trades | $248.99+ Profit                       ║
║    🛡️  Live Only - No Demo/Practice/Simulation               ║
║    📊 Flask Dashboard at localhost:8000                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    log_header "🏗️  DEVELOPMENTAL ENGINEER DEPLOYMENT GUIDE"
    log "📂 Deployment directory: $SCRIPT_DIR"
    log "📝 Log file: $LOG_FILE"
    log "⏰ Deployment timestamp: $TIMESTAMP"
    echo ""
}

# ==================== SYSTEM VALIDATION ====================
validate_system_requirements() {
    log_header "🔍 SYSTEM REQUIREMENTS VALIDATION"
    
    # Check Python version
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log_success "Python detected: $PYTHON_VERSION"
    else
        log_error "Python 3 not found. Please install Python 3.8+"
        exit 1
    fi
    
    # Check pip
    if command -v pip3 &> /dev/null; then
        log_success "pip3 detected"
    else
        log_error "pip3 not found. Please install pip"
        exit 1
    fi
    
    # Check git
    if command -v git &> /dev/null; then
        log_success "Git detected"
    else
        log_warning "Git not found - version control recommended"
    fi
    
    # Check system resources
    TOTAL_RAM=$(free -h | awk '/^Mem:/ {print $2}')
    AVAILABLE_DISK=$(df -h . | awk 'NR==2 {print $4}')
    log "📊 System resources: RAM: $TOTAL_RAM, Disk: $AVAILABLE_DISK"
    
    log_success "System requirements validated"
    echo ""
}

# ==================== DIRECTORY STRUCTURE ====================
create_directory_structure() {
    log_header "📁 CREATING DIRECTORY STRUCTURE"
    
    # Core directories
    directories=(
        "dashboard"
        "dashboard/templates"
        "dashboard/static"
        "dashboard/static/css"
        "dashboard/static/js"
        "logs"
        "data"
        "config"
        "scripts"
        "backups"
    )
    
    for dir in "${directories[@]}"; do
        if [[ ! -d "$dir" ]]; then
            mkdir -p "$dir"
            log "Created directory: $dir"
        else
            log "Directory exists: $dir"
        fi
    done
    
    log_success "Directory structure created"
    echo ""
}

# ==================== VIRTUAL ENVIRONMENT ====================
setup_virtual_environment() {
    log_header "🐍 PYTHON VIRTUAL ENVIRONMENT SETUP"
    
    VENV_NAME="wolfpack_live_env"
    
    if [[ ! -d "$VENV_NAME" ]]; then
        log "Creating virtual environment: $VENV_NAME"
        python3 -m venv "$VENV_NAME"
        log_success "Virtual environment created"
    else
        log "Virtual environment exists: $VENV_NAME"
    fi
    
    # Activate virtual environment
    source "$VENV_NAME/bin/activate"
    log_success "Virtual environment activated"
    
    # Upgrade pip
    pip install --upgrade pip
    
    echo ""
}

# ==================== DEPENDENCIES INSTALLATION ====================
install_dependencies() {
    log_header "📦 INSTALLING PYTHON DEPENDENCIES"
    
    # Core trading dependencies
    core_packages=(
        "requests>=2.31.0"
        "flask>=2.3.0"
        "numpy>=1.24.0"
        "pandas>=2.0.0"
        "python-dateutil>=2.8.2"
        "pytz>=2023.3"
        "cryptography>=41.0.0"
        "PyJWT>=2.8.0"
        "websocket-client>=1.6.0"
        "ccxt>=4.0.0"
        "scikit-learn>=1.3.0"
        "schedule>=1.2.0"
    )
    
    log "Installing core trading packages..."
    for package in "${core_packages[@]}"; do
        pip install "$package"
        log "Installed: $package"
    done
    
    # Web dashboard dependencies
    web_packages=(
        "flask-cors>=4.0.0"
        "flask-socketio>=5.3.0"
        "gunicorn>=21.0.0"
    )
    
    log "Installing web dashboard packages..."
    for package in "${web_packages[@]}"; do
        pip install "$package"
        log "Installed: $package"
    done
    
    # Generate requirements.txt
    pip freeze > requirements.txt
    log_success "Generated requirements.txt"
    
    log_success "All dependencies installed successfully"
    echo ""
}

# ==================== CONFIGURATION FILES ====================
create_configuration_files() {
    log_header "⚙️  CREATING CONFIGURATION FILES"
    
    # Main configuration file
    cat > config/config_live.json << 'EOF'
{
    "trading_mode": "LIVE_ONLY",
    "constitutional_pin": "841921",
    "system_name": "WOLFPACK-LITE",
    "version": "2.0.0",
    "deployment_timestamp": "2025-08-06",
    
    "trading_parameters": {
        "risk_per_trade": 1.0,
        "max_concurrent_trades": 3,
        "max_trades_per_day": 15,
        "min_risk_reward": 2.5,
        "target_risk_reward": 3.0,
        "min_confluence_score": 7.0,
        "scan_interval": 2,
        "cooldown_seconds": 300
    },
    
    "oanda_config": {
        "environment": "live",
        "base_url": "https://api-fxtrade.oanda.com",
        "stream_url": "https://stream-fxtrade.oanda.com",
        "pairs": [
            "EUR_USD", "GBP_USD", "USD_JPY", "AUD_USD",
            "USD_CAD", "USD_CHF", "NZD_USD", "EUR_GBP",
            "EUR_JPY", "GBP_JPY", "AUD_JPY", "CHF_JPY"
        ]
    },
    
    "coinbase_config": {
        "environment": "live",
        "base_url": "https://api.coinbase.com",
        "cdp_url": "https://api.cdp.coinbase.com",
        "algorithm": "ed25519",
        "jwt_expiry": 120,
        "pairs": [
            "BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD",
            "XRP-USD", "DOGE-USD", "AVAX-USD", "DOT-USD",
            "MATIC-USD", "LINK-USD", "ATOM-USD", "ALGO-USD"
        ]
    },
    
    "dashboard_config": {
        "host": "0.0.0.0",
        "port": 8000,
        "debug": false,
        "threaded": true,
        "auto_reload": true,
        "update_interval": 5
    },
    
    "security_config": {
        "live_trading_only": true,
        "oco_mandatory": true,
        "emergency_stop_enabled": true,
        "audit_logging": true,
        "credential_encryption": true
    },
    
    "timezone_config": {
        "system_timezone": "America/New_York",
        "trading_sessions": {
            "london_open": "03:00",
            "london_close": "12:00",
            "ny_open": "08:00",
            "ny_close": "17:00",
            "asian_open": "18:00",
            "asian_close": "03:00"
        }
    },
    
    "logging_config": {
        "log_level": "INFO",
        "log_rotation": true,
        "max_log_files": 30,
        "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }
}
EOF
    log_success "Created config/config_live.json"
    
    # Environment configuration
    cat > .env << 'EOF'
# WOLFPACK-LITE ENVIRONMENT CONFIGURATION
# Constitutional PIN: 841921
# LIVE TRADING ONLY - NO DEMO/PRACTICE/SIMULATION

# System Configuration
CONSTITUTIONAL_PIN=841921
TRADING_MODE=LIVE_ONLY
SYSTEM_NAME=WOLFPACK-LITE
FLASK_ENV=production
FLASK_DEBUG=false

# Dashboard Configuration
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=8000

# Security Configuration
LIVE_TRADING_ONLY=true
OCO_MANDATORY=true
AUDIT_LOGGING=true

# Timezone Configuration
TZ=America/New_York

# Logging Configuration
LOG_LEVEL=INFO
LOG_ROTATION=true
EOF
    log_success "Created .env file"
    
    log_success "Configuration files created"
    echo ""
}

# ==================== CORE SYSTEM FILES ====================
validate_core_system_files() {
    log_header "🔍 VALIDATING CORE SYSTEM FILES"
    
    # Core files that must exist
    core_files=(
        "credentials.py"
        "main.py"
        "go_live.py"
        "coinbase_ed25519_auth.py"
        "logger.py"
        "dashboard/app.py"
        "executor.py"
        "guardian_fresh.py"
    )
    
    missing_files=()
    
    for file in "${core_files[@]}"; do
        if [[ -f "$file" ]]; then
            log_success "Found: $file"
        else
            log_error "Missing: $file"
            missing_files+=("$file")
        fi
    done
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        log_error "Missing core files detected. Please ensure all files are present."
        log_error "Missing files: ${missing_files[*]}"
        exit 1
    fi
    
    log_success "All core system files validated"
    echo ""
}

# ==================== DATABASE SETUP ====================
setup_database() {
    log_header "🗄️  DATABASE SETUP"
    
    # Create SQLite database for trade logging
    cat > scripts/setup_database.py << 'EOF'
#!/usr/bin/env python3
"""
Database setup for Wolfpack-Lite trading system
"""
import sqlite3
import os
from datetime import datetime

def create_database():
    """Create and initialize the trading database"""
    db_path = "data/wolfpack_trading.db"
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Create database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create trades table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            constitutional_pin TEXT NOT NULL,
            trade_id TEXT UNIQUE NOT NULL,
            pair TEXT NOT NULL,
            direction TEXT NOT NULL,
            entry_price REAL NOT NULL,
            exit_price REAL,
            quantity REAL NOT NULL,
            stop_loss REAL,
            take_profit REAL,
            pnl REAL DEFAULT 0.0,
            status TEXT DEFAULT 'OPEN',
            broker TEXT NOT NULL,
            strategy TEXT,
            confidence REAL,
            entry_time TIMESTAMP NOT NULL,
            exit_time TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create system_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            constitutional_pin TEXT NOT NULL,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            component TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create performance_metrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            constitutional_pin TEXT NOT NULL,
            date DATE NOT NULL,
            total_trades INTEGER DEFAULT 0,
            winning_trades INTEGER DEFAULT 0,
            losing_trades INTEGER DEFAULT 0,
            total_pnl REAL DEFAULT 0.0,
            win_rate REAL DEFAULT 0.0,
            average_pnl REAL DEFAULT 0.0,
            max_drawdown REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(constitutional_pin, date)
        )
    ''')
    
    # Create configuration_audit table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuration_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            constitutional_pin TEXT NOT NULL,
            config_section TEXT NOT NULL,
            old_value TEXT,
            new_value TEXT NOT NULL,
            changed_by TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"✅ Database created successfully at: {db_path}")

if __name__ == "__main__":
    create_database()
EOF
    
    # Run database setup
    python3 scripts/setup_database.py
    log_success "Database setup completed"
    echo ""
}

# ==================== SYSTEMD SERVICE ====================
create_systemd_service() {
    log_header "🔧 CREATING SYSTEMD SERVICE"
    
    SERVICE_NAME="wolfpack-lite"
    SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
    
    cat > "scripts/${SERVICE_NAME}.service" << EOF
[Unit]
Description=Wolfpack-Lite Live Trading System
After=network.target
Wants=network.target

[Service]
Type=liveple
User=$(whoami)
Group=$(id -gn)
WorkingDirectory=${SCRIPT_DIR}
ExecStart=${SCRIPT_DIR}/wolfpack_live_env/bin/python3 ${SCRIPT_DIR}/main.py --constitutional-pin 841921 --secure
Restart=always
RestartSec=10
KillMode=mixed
TimeoutStopSec=30

# Environment variables
Environment=PYTHONPATH=${SCRIPT_DIR}
Environment=PYTHONUNBUFFERED=1
Environment=CONSTITUTIONAL_PIN=841921
Environment=TRADING_MODE=LIVE_ONLY

# Logging
StandardOutput=append:${SCRIPT_DIR}/logs/systemd.log
StandardError=append:${SCRIPT_DIR}/logs/systemd_error.log

# Security
NoNewPrivileges=true
PrivateTmp=true

# Resource limits
LimitNOFILE=65536
LimitNPROC=4096

[Install]
WantedBy=multi-user.target
EOF
    
    log "Created systemd service file: scripts/${SERVICE_NAME}.service"
    
    # Install systemd service (requires sudo)
    if command -v systemctl &> /dev/null; then
        log "To install the systemd service, run:"
        log "  sudo cp scripts/${SERVICE_NAME}.service /etc/systemd/system/"
        log "  sudo systemctl daemon-reload"
        log "  sudo systemctl enable ${SERVICE_NAME}"
        log "  sudo systemctl start ${SERVICE_NAME}"
    else
        log_warning "systemctl not found - systemd service created but not installed"
    fi
    
    log_success "Systemd service configuration created"
    echo ""
}

# ==================== STARTUP SCRIPTS ====================
create_startup_scripts() {
    log_header "🚀 CREATING STARTUP SCRIPTS"
    
    # Main startup script
    cat > start_wolfpack_live.sh << 'EOF'
#!/bin/bash
# WOLFPACK-LITE LIVE TRADING STARTUP SCRIPT
# Constitutional PIN: 841921

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 STARTING WOLFPACK-LITE LIVE TRADING SYSTEM"
echo "=============================================="
echo "📊 Constitutional PIN: 841921"
echo "💰 Live Trading: OANDA Forex + Coinbase Crypto"
echo "🛡️  Live Only - No Demo/Practice/Simulation"
echo "=============================================="

# Validate environment
if [[ ! -f "credentials.py" ]]; then
    echo "❌ credentials.py not found - please configure credentials"
    exit 1
fi

if [[ ! -f "config/config_live.json" ]]; then
    echo "❌ config/config_live.json not found"
    exit 1
fi

# Activate virtual environment
if [[ -d "wolfpack_live_env" ]]; then
    source wolfpack_live_env/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found - run deployment script first"
    exit 1
fi

# Check credentials
echo "🔐 Validating credentials..."
python3 -c "
from credentials import WolfpackCredentials
creds = WolfpackCredentials()
issues = creds.validate_credentials()
if issues:
    print('❌ Credential issues found:')
    for issue in issues:
        print(f'   - {issue}')
    exit(1)
else:
    print('✅ Credentials validated')
"

# Start Flask dashboard in background
echo "📊 Starting Flask dashboard..."
python3 dashboard/app.py &
DASHBOARD_PID=$!
echo "✅ Dashboard started (PID: $DASHBOARD_PID) at http://localhost:8000"

# Wait for dashboard to start
sleep 3

# Start main trading system
echo "🎯 Starting main trading system..."
python3 main.py --constitutional-pin 841921 --secure

# Cleanup on exit
cleanup() {
    echo "🛑 Shutting down Wolfpack-Lite..."
    kill $DASHBOARD_PID 2>/dev/null || true
    echo "✅ Shutdown complete"
}

trap cleanup EXIT INT TERM
EOF
    
    chmod +x start_wolfpack_live.sh
    log_success "Created start_wolfpack_live.sh"
    
    # Dashboard startup script
    cat > scripts/start_dashboard.sh << 'EOF'
#!/bin/bash
# WOLFPACK-LITE DASHBOARD STARTUP

cd "$(dirname "$0")/.."
source wolfpack_live_env/bin/activate

echo "📊 Starting Wolfpack-Lite Dashboard..."
echo "🌐 Dashboard will be available at: http://localhost:8000"

python3 dashboard/app.py
EOF
    
    chmod +x scripts/start_dashboard.sh
    log_success "Created scripts/start_dashboard.sh"
    
    # Health check script
    cat > scripts/health_check.sh << 'EOF'
#!/bin/bash
# WOLFPACK-LITE HEALTH CHECK

cd "$(dirname "$0")/.."

echo "🏥 WOLFPACK-LITE HEALTH CHECK"
echo "=============================="

# Check if virtual environment exists
if [[ -d "wolfpack_live_env" ]]; then
    echo "✅ Virtual environment: OK"
else
    echo "❌ Virtual environment: MISSING"
fi

# Check core files
core_files=("credentials.py" "main.py" "go_live.py" "dashboard/app.py")
for file in "${core_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ Core file $file: OK"
    else
        echo "❌ Core file $file: MISSING"
    fi
done

# Check configuration
if [[ -f "config/config_live.json" ]]; then
    echo "✅ Configuration: OK"
else
    echo "❌ Configuration: MISSING"
fi

# Check database
if [[ -f "data/wolfpack_trading.db" ]]; then
    echo "✅ Database: OK"
else
    echo "❌ Database: MISSING"
fi

# Check dashboard endpoint
if curl -s -f http://localhost:8000 > /dev/null 2>&1; then
    echo "✅ Dashboard: ACCESSIBLE at http://localhost:8000"
else
    echo "⚠️  Dashboard: NOT ACCESSIBLE (may be stopped)"
fi

# Check system resources
echo ""
echo "📊 SYSTEM RESOURCES:"
echo "Memory usage: $(free -h | grep '^Mem:' | awk '{print $3 "/" $2}')"
echo "Disk usage: $(df -h . | tail -1 | awk '{print $3 "/" $2 " (" $5 " used)"}')"
echo "Load average: $(uptime | awk -F'load average:' '{ print $2 }')"

echo ""
echo "🏁 Health check complete"
EOF
    
    chmod +x scripts/health_check.sh
    log_success "Created scripts/health_check.sh"
    
    log_success "Startup scripts created"
    echo ""
}

# ==================== LOG MANAGEMENT ====================
setup_log_management() {
    log_header "📝 SETTING UP LOG MANAGEMENT"
    
    # Create log rotation script
    cat > scripts/rotate_logs.sh << 'EOF'
#!/bin/bash
# WOLFPACK-LITE LOG ROTATION

LOG_DIR="logs"
MAX_LOG_SIZE="50M"
MAX_LOG_FILES=30

echo "🔄 Rotating Wolfpack-Lite logs..."

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Rotate log files
for log_file in "$LOG_DIR"/*.log; do
    if [[ -f "$log_file" ]]; then
        # Check file size
        file_size=$(stat -f%z "$log_file" 2>/dev/null || stat -c%s "$log_file" 2>/dev/null || echo 0)
        max_size=$((50*1024*1024))  # 50MB in bytes
        
        if [[ $file_size -gt $max_size ]]; then
            # Rotate the file
            timestamp=$(date +%Y%m%d_%H%M%S)
            mv "$log_file" "${log_file%.log}_${timestamp}.log"
            echo "📦 Rotated: $log_file"
        fi
    fi
done

find "$LOG_DIR" -name "*.log" -type f -printf '%T@ %p\n' | sort -rn | tail -n +$((MAX_LOG_FILES+1)) | cut -d' ' -f2- | xargs rm -f

echo "✅ Log rotation complete"
EOF
    
    chmod +x scripts/rotate_logs.sh
    log_success "Created scripts/rotate_logs.sh"
    
    # Create cron job for log rotation
    cat > scripts/setup_cron.sh << 'EOF'
#!/bin/bash
# SETUP CRON JOBS FOR WOLFPACK-LITE

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "⏰ Setting up cron jobs for Wolfpack-Lite..."

# Create cron job for log rotation (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * $SCRIPT_DIR/scripts/rotate_logs.sh") | crontab -

# Create cron job for health check (every 15 minutes)
(crontab -l 2>/dev/null; echo "*/15 * * * * $SCRIPT_DIR/scripts/health_check.sh >> $SCRIPT_DIR/logs/health_check.log 2>&1") | crontab -

echo "✅ Cron jobs configured:"
echo "  - Log rotation: Daily at 2:00 AM"
echo "  - Health check: Every 15 minutes"
EOF
    
    chmod +x scripts/setup_cron.sh
    log_success "Created scripts/setup_cron.sh"
    
    log_success "Log management setup completed"
    echo ""
}

# ==================== BACKUP SYSTEM ====================
setup_backup_system() {
    log_header "💾 SETTING UP BACKUP SYSTEM"
    
    cat > scripts/backup_system.sh << 'EOF'
#!/bin/bash
# WOLFPACK-LITE BACKUP SYSTEM

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="$SCRIPT_DIR/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="wolfpack_backup_$TIMESTAMP"

echo "💾 Creating Wolfpack-Lite backup..."

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create backup archive
tar -czf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" \
    --exclude='wolfpack_live_env' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='logs/*.log' \
    --exclude='backups' \
    -C "$SCRIPT_DIR" \
    credentials.py \
    main.py \
    go_live.py \
    dashboard \
    config \
    scripts \
    data/wolfpack_trading.db \
    requirements.txt

echo "✅ Backup created: $BACKUP_DIR/$BACKUP_NAME.tar.gz"

ls -t "$BACKUP_DIR"/*.tar.gz | tail -n +11 | xargs rm -f 2>/dev/null || true

echo "💾 Backup system complete"
EOF
    
    chmod +x scripts/backup_system.sh
    log_success "Created scripts/backup_system.sh"
    
    log_success "Backup system setup completed"
    echo ""
}

# ==================== FINAL VALIDATION ====================
final_system_validation() {
    log_header "🔍 FINAL SYSTEM VALIDATION"
    
    # Test Python imports
    log "Testing Python imports..."
    python3 -c "
import sys
required_modules = [
    'requests', 'flask', 'numpy', 'pandas', 
    'cryptography', 'PyJWT', 'sqlite3'
]

missing_modules = []
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        missing_modules.append(module)

if missing_modules:
    print(f'❌ Missing modules: {missing_modules}')
    sys.exit(1)
else:
    print('✅ All required modules available')
"
    
    # Test database connection
    log "Testing database connection..."
    python3 -c "
import sqlite3
import os

if os.path.exists('data/wolfpack_trading.db'):
    try:
        conn = sqlite3.connect('data/wolfpack_trading.db')
        conn.close()
        print('✅ Database connection successful')
    except Exception as e:
        print(f'❌ Database connection failed: {e}')
        exit(1)
else:
    print('❌ Database file not found')
    exit(1)
"
    
    # Verify file permissions
    log "Verifying file permissions..."
    chmod +x start_wolfpack_live.sh
    chmod +x scripts/*.sh
    log_success "File permissions set"
    
    # Generate deployment summary
    cat > DEPLOYMENT_SUMMARY.md << EOF
# 🚀 WOLFPACK-LITE DEPLOYMENT SUMMARY
**Deployment Date**: $(date)
**Constitutional PIN**: 841921
**System Status**: READY FOR LIVE TRADING

## 📊 Deployment Statistics
- **Python Version**: $(python3 --version)
- **Virtual Environment**: wolfpack_live_env
- **Dependencies**: $(pip freeze | wc -l) packages installed
- **Database**: SQLite database created
- **Configuration**: Live-only configuration active
- **Dashboard**: Ready at http://localhost:8000

## 🎯 Quick Start Commands
\`\`\`bash
# Start complete system
./start_wolfpack_live.sh

# Start dashboard only
./scripts/start_dashboard.sh

# Health check
./scripts/health_check.sh

# System backup
./scripts/backup_system.sh
\`\`\`

## 🔧 System Management
\`\`\`bash
# Install systemd service
sudo cp scripts/wolfpack-lite.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable wolfpack-lite
sudo systemctl start wolfpack-lite

# Setup cron jobs
./scripts/setup_cron.sh
\`\`\`

## 📂 Directory Structure
\`\`\`
wolfpack-lite/
├── credentials.py              # API credentials (Constitutional PIN: 841921)
├── main.py                     # Primary trading controller
├── go_live.py                  # Live trading launcher
├── start_wolfpack_live.sh      # System startup script
├── requirements.txt            # Python dependencies
├── config/
│   └── config_live.json        # Live trading configuration
├── dashboard/
│   ├── app.py                  # Flask web dashboard
│   └── templates/              # Dashboard templates
├── data/
│   └── wolfpack_trading.db     # SQLite database
├── logs/                       # System logs
├── scripts/                    # Management scripts
├── backups/                    # System backups
└── wolfpack_live_env/          # Python virtual environment
\`\`\`

## 🛡️ Security Features
- Constitutional PIN authorization (841921)
- Live-only trading (no live/liveulation)
- Encrypted credential storage
- Comprehensive audit logging
- Emergency stop protocols
- Automatic backup system

## 📈 Performance Targets
- **Risk per Trade**: 1% of capital
- **Maximum Concurrent Trades**: 3
- **Target Win Rate**: 68-72%
- **Risk/Reward Ratio**: 1:2.5 to 1:3.0
- **Daily Trade Limit**: 15 trades

## 🎮 Dashboard Features
- Real-time trading status
- Live P&L tracking
- Position monitoring
- System health metrics
- Emergency controls
- Performance analytics

---
**Generated**: $(date)
**Status**: DEPLOYMENT COMPLETE ✅
**Next Step**: Configure credentials.py with live API keys
EOF
    
    log_success "Final system validation completed"
    echo ""
}

# ==================== MAIN DEPLOYMENT ====================
main_deployment() {
    display_banner
    
    # Execute deployment steps
    validate_system_requirements
    create_directory_structure
    setup_virtual_environment
    install_dependencies
    create_configuration_files
    validate_core_system_files
    setup_database
    create_systemd_service
    create_startup_scripts
    setup_log_management
    setup_backup_system
    final_system_validation
    
    # Final deployment summary
    log_header "🎉 DEPLOYMENT COMPLETE"
    log_success "Wolfpack-Lite Live Trading System deployed successfully!"
    log ""
    log_header "📋 NEXT STEPS:"
    log "1. Configure credentials.py with your live API keys"
    log "2. Verify Constitutional PIN: 841921"
    log "3. Test system: ./start_wolfpack_live.sh"
    log "4. Access dashboard: http://localhost:8000"
    log "5. Monitor logs: tail -f logs/trading.log"
    log ""
    log_header "🛡️ SECURITY REMINDER:"
    log "• Live trading only - real money at risk"
    log "• Constitutional PIN required for all operations"
    log "• Never commit credentials to version control"
    log "• Monitor system health regularly"
    log ""
    log_header "📊 SYSTEM STATUS:"
    log "✅ Virtual environment configured"
    log "✅ Dependencies installed"
    log "✅ Configuration files created"
    log "✅ Database initialized"
    log "✅ Scripts and services ready"
    log "✅ Backup system configured"
    log ""
    log_success "Wolfpack-Lite ready for live trading deployment!"
    log "Constitutional PIN: 841921 | Live Trading Only"
    
    # Display final banner
    echo ""
    echo -e "${BOLD}${GREEN}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║             🎉 DEPLOYMENT SUCCESSFUL 🎉                      ║
║                                                              ║
║                WOLFPACK-LITE LIVE TRADING                    ║
║                  Constitutional PIN: 841921                  ║
║                                                              ║
║              Ready for Live Trading Operations               ║
║                                                              ║
║     📊 Dashboard: http://localhost:8000                      ║
║     🚀 Start: ./start_wolfpack_live.sh                       ║
║     🔍 Health: ./scripts/health_check.sh                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# ==================== SCRIPT EXECUTION ====================
# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main_deployment "$@"
fi

# EOF - WOLFPACK-LITE DEPLOYMENT SCRIPT
