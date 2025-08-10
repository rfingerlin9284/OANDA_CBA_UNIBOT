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
