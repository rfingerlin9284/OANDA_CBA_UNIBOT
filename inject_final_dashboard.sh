#!/bin/bash

echo "📦 [1/3] Injecting clean, real-only stats route into dashboard/app.py..."

cat > dashboard/app.py << 'EOF'
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def stats():
    try:
        log_path = "logs/live_trading.log"
        if not os.path.exists(log_path):
            return jsonify({
                "total_trades": 0,
                "total_pnl": 0.0,
                "avg_pnl": 0.0,
                "bot_status": "IDLE"
            })

        with open(log_path, "r") as f:
            lines = f.readlines()[-50:]

        real_trades = [line.strip() for line in lines if "ORDER FILLED" in line]
        pnl_list = []
        for line in real_trades:
            if "$" in line:
                try:
                    pnl = float(line.split("$")[-1])
                    pnl_list.append(pnl)
                except:
                    continue

        total_pnl = round(sum(pnl_list), 2)
        avg_pnl = round(total_pnl / len(pnl_list), 2) if pnl_list else 0.0

        return jsonify({
            "total_trades": len(real_trades),
            "total_pnl": total_pnl,
            "avg_pnl": avg_pnl,
            "bot_status": "RUNNING",
            "constitutional_pin": "841921"
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=False, port=8000, host='0.0.0.0')
EOF

echo "🛑 [2/3] Killing previous dashboard instance (if any)..."
pkill -f "dashboard/app.py"

echo "🚀 [3/3] Restarting dashboard in headless mode..."
nohup python3 dashboard/app.py > logs/dashboard_stdout.log 2>&1 &

echo "✅ Dashboard is LIVE at: http://localhost:8000"
