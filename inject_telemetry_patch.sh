#!/bin/bash

echo "📡 [1/4] Injecting real-time ML telemetry route into dashboard/app.py..."

cat >> dashboard/app.py << 'EOF'

@app.route('/api/telemetry')
def telemetry():
    try:
        telemetry_path = "dashboard/static/js/telemetry.json"
        if not os.path.exists(telemetry_path):
            return jsonify({
                "model_name": "Not Detected",
                "confidence": 0,
                "decision": "Unknown",
                "status": "IDLE",
                "comment": "No telemetry file found"
            })

        with open(telemetry_path, "r") as f:
            data = f.read()

        import json
        telemetry_data = json.loads(data)

        return jsonify({
            "model_name": telemetry_data.get("model_name", "Unknown"),
            "confidence": telemetry_data.get("confidence", 0),
            "decision": telemetry_data.get("decision", "Unknown"),
            "status": telemetry_data.get("status", "IDLE"),
            "comment": telemetry_data.get("comment", "No comment")
        })
    except Exception as e:
        return jsonify({"error": str(e)})
EOF

echo "📝 [2/4] Creating empty live telemetry cache..."
mkdir -p dashboard/static/js
cat > dashboard/static/js/telemetry.json << 'JSON'
{
    "model_name": "OANDA_ML_Alpha",
    "confidence": 0,
    "decision": "Booting...",
    "status": "LOADING",
    "comment": "Awaiting first prediction..."
}
JSON

echo "🧹 [3/4] Killing any stale dashboard instances..."
pkill -f "dashboard/app.py"

echo "🚀 [4/4] Restarting dashboard headless with telemetry API..."
nohup python3 dashboard/app.py > logs/dashboard_stdout.log 2>&1 &

echo "✅ Telemetry endpoint live at: http://localhost:8000/api/telemetry"
#!/bin/bash

echo "📡 [1/4] Injecting real-time ML telemetry route into dashboard/app.py..."

cat >> dashboard/app.py << 'EOF'

@app.route('/api/telemetry')
def telemetry():
    try:
        telemetry_path = "dashboard/static/js/telemetry.json"
        if not os.path.exists(telemetry_path):
            return jsonify({
                "model_name": "Not Detected",
                "confidence": 0,
                "decision": "Unknown",
                "status": "IDLE",
                "comment": "No telemetry file found"
            })

        with open(telemetry_path, "r") as f:
            data = f.read()

        import json
        telemetry_data = json.loads(data)

        return jsonify({
            "model_name": telemetry_data.get("model_name", "Unknown"),
            "confidence": telemetry_data.get("confidence", 0),
            "decision": telemetry_data.get("decision", "Unknown"),
            "status": telemetry_data.get("status", "IDLE"),
            "comment": telemetry_data.get("comment", "No comment")
        })
    except Exception as e:
        return jsonify({"error": str(e)})
EOF

echo "📝 [2/4] Creating empty live telemetry cache..."
mkdir -p dashboard/static/js
cat > dashboard/static/js/telemetry.json << 'JSON'
{
    "model_name": "OANDA_ML_Alpha",
    "confidence": 0,
    "decision": "Booting...",
    "status": "LOADING",
    "comment": "Awaiting first prediction..."
}
JSON

echo "🧹 [3/4] Killing any stale dashboard instances..."
pkill -f "dashboard/app.py"

echo "🚀 [4/4] Restarting dashboard headless with telemetry API..."
nohup python3 dashboard/app.py > logs/dashboard_stdout.log 2>&1 &

echo "✅ Telemetry endpoint live at: http://localhost:8000/api/telemetry"
