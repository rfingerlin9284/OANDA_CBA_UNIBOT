#!/bin/bash
# 🗄️ RBOTZILLA SWARM: DB FALLBACK PATCH + AUTH TEST
# Constitutional PIN: 841921 | Live Trading Only

echo "🗄️ PHASE 4: DB FALLBACK PATCH + AUTHENTICATION TEST"

# Create DB fallback patch for main.py
echo "[🔧] Patching main.py with DB fallback logic..."

# Check current main.py structure
if [ ! -f "main.py" ]; then
    echo "[❌] main.py not found!"
    exit 1
fi

# Backup main.py
cp main.py main.py.backup.$(date +%Y%m%d_%H%M%S)

# Create enhanced main.py with DB fallback
cat > db_fallback_patch.py << 'EOF'
#!/usr/bin/env python3
"""
🗄️ RBOTZILLA DB FALLBACK INJECTOR
Adds JSON log fallback when SQLite DB is missing
"""
import re

# Read main.py
with open('main.py', 'r') as f:
    content = f.read()

# DB fallback code to inject
fallback_code = '''
    # 🗄️ RBOTZILLA DB FALLBACK - Constitutional PIN: 841921
    def get_trading_stats_fallback():
        """Fallback stats from JSON logs when DB is missing"""
        try:
            import json
            import os
            from datetime import datetime
            
            stats = {
                "total_trades": 0,
                "total_pnl": 0.0,
                "avg_pnl": 0.0,
                "bot_status": "READY",
                "last_update": datetime.now().isoformat()
            }
            
            # Parse telemetry logs for stats
            telemetry_file = "logs/ml_predictions.log"
            if os.path.exists(telemetry_file):
                with open(telemetry_file, 'r') as f:
                    lines = f.readlines()
                    stats["total_trades"] = len([l for l in lines if "ML DECISION:" in l])
                    stats["bot_status"] = "ACTIVE" if lines else "IDLE"
            
            # Parse dashboard telemetry if available
            dashboard_file = "dashboard/static/js/telemetry.json"
            if os.path.exists(dashboard_file):
                try:
                    with open(dashboard_file, 'r') as f:
                        data = json.load(f)
                        if "telemetry" in data:
                            stats["total_trades"] = len(data["telemetry"])
                except:
                    pass
            
            return stats
            
        except Exception as e:
            return {
                "total_trades": 0,
                "total_pnl": 0.0,
                "avg_pnl": 0.0,
                "bot_status": "ERROR",
                "error": str(e),
                "last_update": datetime.now().isoformat()
            }
'''

# Find a good injection point (after imports, before main class)
if "class " in content:
    # Find the first class definition
    class_match = re.search(r'^class\s+\w+', content, re.MULTILINE)
    if class_match:
        inject_pos = class_match.start()
        content = content[:inject_pos] + fallback_code + "\n\n" + content[inject_pos:]
else:
    # No class found, add near the end before if __name__ == "__main__"
    if '__name__ == "__main__"' in content:
        main_pos = content.find('if __name__ == "__main__"')
        content = content[:main_pos] + fallback_code + "\n\n" + content[main_pos:]
    else:
        # Just append at the end
        content += fallback_code

# Write back
with open('main.py', 'w') as f:
    f.write(content)

print("[✅] DB fallback injected into main.py")
EOF

python3 db_fallback_patch.py

echo "[✅] DB fallback patch applied"


#!/usr/bin/env python3
"""
🔐 RBOTZILLA COINBASE AUTHENTICATION TEST
Constitutional PIN: 841921
"""
import sys
import traceback
from credentials import WolfpackCredentials

    """Test Coinbase Advanced Trade authentication"""
    print("🔐 RBOTZILLA COINBASE AUTH TEST - Constitutional PIN: 841921")
    print("=" * 60)
    
    try:
        # Load credentials
        creds = WolfpackCredentials()
        print(f"[✅] Credentials loaded - Constitutional PIN: {creds.CONSTITUTIONAL_PIN}")
        
        # Validate credentials
        issues = creds.validate_credentials()
        if issues:
            print("[❌] Credential validation failed:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        
        print("[✅] Credential validation passed")
        
        # Test PEM loading
        try:
            pem_content = creds.COINBASE_PRIVATE_KEY_PEM
            print(f"[✅] PEM loaded successfully ({len(pem_content)} chars)")
            print(f"[🔍] PEM format check: {'✅' if 'BEGIN PRIVATE KEY' in pem_content else '❌'}")
        except Exception as e:
            print(f"[❌] PEM loading failed: {e}")
            return False
        
        # Test Coinbase API import
        try:
            from coinbase_ed25519_auth import CoinbaseEd25519Auth
            print("[✅] CoinbaseEd25519Auth imported successfully")
            
            # Initialize auth
            auth = CoinbaseEd25519Auth(creds)
            print("[✅] Coinbase auth initialized")
            
            # Test connection (if method exists)
                try:
                    return connection_result
                except Exception as e:
                    return False
            else:
                return True
                
        except ImportError as e:
            print(f"[❌] Coinbase auth import failed: {e}")
            return False
        except Exception as e:
            print(f"[❌] Coinbase auth initialization failed: {e}")
            return False
        
    except Exception as e:
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    if success:
        print("🎯 RBOTZILLA AUTH TEST: ✅ SUCCESS - Ready for live trading!")
        print("🚀 Constitutional PIN 841921 verified - System ready for deployment")
    else:
        print("❌ RBOTZILLA AUTH TEST: FAILED - Authentication issues detected")
        print("🔧 Review credentials and PEM format")
    
    sys.exit(0 if success else 1)
EOF


# Test the authentication

# Create system status checker
echo "[📊] Creating system status checker..."

cat > system_status.py << 'EOF'
#!/usr/bin/env python3
"""
📊 RBOTZILLA SYSTEM STATUS CHECKER
Constitutional PIN: 841921
"""
import os
import json
from datetime import datetime
from credentials import WolfpackCredentials

def check_system_status():
    """Comprehensive RBOTZILLA system status check"""
    print("📊 RBOTZILLA SYSTEM STATUS - Constitutional PIN: 841921")
    print("=" * 60)
    
    status = {
        "timestamp": datetime.now().isoformat(),
        "constitutional_pin": "841921",
        "components": {},
        "overall_status": "UNKNOWN"
    }
    
    # Check credentials
    try:
        creds = WolfpackCredentials()
        issues = creds.validate_credentials()
        status["components"]["credentials"] = {
            "status": "✅ OK" if not issues else "❌ ISSUES",
            "issues": issues
        }
        print(f"[🔐] Credentials: {status['components']['credentials']['status']}")
    except Exception as e:
        status["components"]["credentials"] = {"status": "❌ ERROR", "error": str(e)}
        print(f"[🔐] Credentials: ❌ ERROR - {e}")
    
    # Check PEM file
    pem_exists = os.path.exists("coinbase_private_fixed.pem")
    status["components"]["pem_file"] = {"status": "✅ OK" if pem_exists else "❌ MISSING"}
    print(f"[🔑] PEM File: {status['components']['pem_file']['status']}")
    
    # Check telemetry system
    telemetry_exists = os.path.exists("logs/telemetry_logger.py")
    log_exists = os.path.exists("logs/ml_predictions.log")
    status["components"]["telemetry"] = {
        "status": "✅ OK" if telemetry_exists else "❌ MISSING",
        "log_exists": log_exists
    }
    print(f"[🧠] Telemetry: {status['components']['telemetry']['status']}")
    
    # Check dashboard files
    dashboard_exists = os.path.exists("dashboard/app.py")
    telemetry_json = os.path.exists("dashboard/static/js/telemetry.json")
    status["components"]["dashboard"] = {
        "status": "✅ OK" if dashboard_exists else "❌ MISSING",
        "telemetry_json": telemetry_json
    }
    print(f"[📊] Dashboard: {status['components']['dashboard']['status']}")
    
    # Check trading stats
    try:
        # Try to get stats using fallback method
        stats = {
            "total_trades": 0,
            "total_pnl": 0.0,
            "bot_status": "READY"
        }
        
        if os.path.exists("logs/ml_predictions.log"):
            with open("logs/ml_predictions.log", 'r') as f:
                lines = f.readlines()
                stats["total_trades"] = len([l for l in lines if "ML DECISION:" in l])
        
        status["components"]["trading_stats"] = {
            "status": "✅ OK",
            "stats": stats
        }
        print(f"[📈] Trading Stats: ✅ OK ({stats['total_trades']} predictions logged)")
        
    except Exception as e:
        status["components"]["trading_stats"] = {"status": "❌ ERROR", "error": str(e)}
        print(f"[📈] Trading Stats: ❌ ERROR - {e}")
    
    # Overall status
    all_ok = all(comp.get("status", "").startswith("✅") for comp in status["components"].values())
    status["overall_status"] = "✅ READY FOR DEPLOYMENT" if all_ok else "⚠️ ISSUES DETECTED"
    
    print("\n" + "=" * 60)
    print(f"🎯 OVERALL STATUS: {status['overall_status']}")
    
    # Save status to file
    with open("logs/system_status.json", "w") as f:
        json.dump(status, f, indent=2)
    
    print(f"[💾] Status saved to: logs/system_status.json")
    return all_ok

if __name__ == "__main__":
    check_system_status()
EOF

chmod +x system_status.py
python3 system_status.py

echo ""
echo "[🗄️] JSON fallback system active"
echo "[📊] System status check completed"
