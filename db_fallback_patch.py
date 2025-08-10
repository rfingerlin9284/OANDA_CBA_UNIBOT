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
