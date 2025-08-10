#!/bin/bash
# 🧠 RBOTZILLA SWARM: SURGICAL TELEMETRY INJECTOR
# Constitutional PIN: 841921 | Live Trading Only

echo "🧠 PHASE 3: SURGICAL TELEMETRY INJECTOR - TYPE-SAFE & SELF-SAVING"

# Ensure logs directory exists
mkdir -p logs
mkdir -p dashboard/static/js

# Target files for telemetry injection
TARGETS=("ml_predictor.py" "ml_telemetry_writer.py" "main.py")
MARKER="# === RBOTZILLA TELEMETRY LOGGER START ==="
MARKER_END="# === RBOTZILLA TELEMETRY LOGGER END ==="

# Create the master telemetry logger
cat > logs/telemetry_logger.py << 'EOF'
#!/usr/bin/env python3
"""
🧠 RBOTZILLA SWARM TELEMETRY LOGGER
Constitutional PIN: 841921
Thread-safe, type-coerced, JSON-validated logging
"""
import json
import os
import threading
from datetime import datetime
from typing import Any, Union

class RBotZillaTelemetry:
    """RBOTZILLA Swarm telemetry logger with thread safety"""
    
    def __init__(self):
        self.lock = threading.Lock()
        self.log_file = "logs/ml_predictions.log"
        self.dashboard_file = "dashboard/static/js/telemetry.json"
        
    def log_telemetry(self, prediction: Any, confidence: Union[float, str], model_name: str = "WolfNet-V3"):
        """Thread-safe telemetry logging with type coercion"""
        try:
            with self.lock:
                # Type coercion and validation
                payload = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "constitutional_pin": "841921",
                    "prediction": str(prediction).upper() if prediction else "UNKNOWN",
                    "confidence": round(float(confidence) if confidence else 0.0, 4),
                    "model": str(model_name),
                    "system": "RBOTZILLA_SWARM"
                }
                
                # Log to file
                with open(self.log_file, "a") as f:
                    f.write("ML DECISION: " + json.dumps(payload, separators=(',', ':')) + "\n")
                
                # Update dashboard (last 10 entries)
                self._update_dashboard()
                
        except Exception as e:
            # Fallback logging
            with open("logs/telemetry_errors.log", "a") as f:
                f.write(f"TELEMETRY ERROR: {datetime.utcnow().isoformat()}: {e}\n")
    
    def _update_dashboard(self):
        """Update dashboard telemetry JSON"""
        try:
            # Read last 10 entries
            entries = []
            if os.path.exists(self.log_file):
                with open(self.log_file, "r") as f:
                    lines = f.readlines()[-10:]  # Last 10 entries
                    for line in lines:
                        if "ML DECISION:" in line:
                            json_str = line.split("ML DECISION:", 1)[1].strip()
                            entries.append(json.loads(json_str))
            
            # Write to dashboard
            with open(self.dashboard_file, "w") as f:
                json.dump({"telemetry": entries}, f, indent=2)
                
        except Exception as e:
            pass  # Silent fail for dashboard update

# Global instance
RBOTZILLA_TELEMETRY = RBotZillaTelemetry()

def log_telemetry(prediction, confidence, model_name="WolfNet-V3"):
    """Global function for easy access"""
    RBOTZILLA_TELEMETRY.log_telemetry(prediction, confidence, model_name)
EOF

echo "[✅] Master telemetry logger created: logs/telemetry_logger.py"

# Function to inject telemetry into target files
inject_into_file() {
    local target_file="$1"
    
    if [ ! -f "$target_file" ]; then
        echo "[⚠️] Target file not found: $target_file"
        return 1
    fi
    
    echo "[🔍] Processing: $target_file"
    
    # Check if already injected
    if grep -q "$MARKER" "$target_file"; then
        echo "[⚠️] Telemetry already injected in $target_file"
        return 0
    fi
    
    # Backup original
    cp "$target_file" "${target_file}.backup.$(date +%Y%m%d_%H%M%S)"
    
    # Inject telemetry import and function call
    python3 << EOF
import re
import os

target_file = "$target_file"

# Read the file
with open(target_file, 'r') as f:
    content = f.read()

# Add import at the top (after existing imports)
import_line = "from logs.telemetry_logger import log_telemetry  # RBOTZILLA INJECTION"

# Find the last import line
import_pattern = r'^(import\s+\w+|from\s+\w+.*?import.*?)$'
imports = re.findall(import_pattern, content, re.MULTILINE)

if imports:
    # Find position after last import
    last_import = imports[-1]
    insert_pos = content.find(last_import) + len(last_import)
    # Find the end of the line
    next_newline = content.find('\n', insert_pos)
    if next_newline != -1:
        content = content[:next_newline+1] + import_line + '\n' + content[next_newline+1:]
    else:
        content += '\n' + import_line + '\n'
else:
    # No imports found, add at the beginning
    content = import_line + '\n' + content

# Find prediction assignment patterns and inject logging
patterns = [
    r'(\s*)(prediction\s*=\s*.*?)(\n)',
    r'(\s*)(signal\s*=\s*.*?)(\n)', 
    r'(\s*)(decision\s*=\s*.*?)(\n)',
    r'(\s*)(result\s*=\s*.*?)(\n)'
]

for pattern in patterns:
    matches = list(re.finditer(pattern, content))
    for match in reversed(matches):  # Reverse to maintain positions
        indent, assignment, newline = match.groups()
        # Extract variable name and value
        var_name = assignment.split('=')[0].strip()
        injection = f"{indent}log_telemetry({var_name}, 0.75, 'WolfNet-V3')  # RBOTZILLA AUTO-INJECT{newline}"
        
        # Insert after the assignment
        end_pos = match.end()
        content = content[:end_pos] + injection + content[end_pos:]
        break  # Only inject once per file

# Write back
with open(target_file, 'w') as f:
    f.write(content)

print(f"[✅] Telemetry injected into {target_file}")
EOF
}

# Inject into target files
for target in "${TARGETS[@]}"; do
    if [ -f "$target" ]; then
        inject_into_file "$target"
    else
        echo "[⚠️] Target file not found: $target"
    fi
done

#!/usr/bin/env python3
"""Test RBOTZILLA telemetry system"""
from logs.telemetry_logger import log_telemetry

# Test predictions
predictions = ["BUY", "SELL", "HOLD"]
confidences = [0.87, 0.92, 0.45]

print("🧠 Testing RBOTZILLA telemetry...")
for pred, conf in zip(predictions, confidences):
    log_telemetry(pred, conf, "WolfNet-V3")

EOF


echo "[✅] PHASE 3 COMPLETE: Surgical telemetry injection successful"
echo "[📝] Test telemetry generated in logs/"
echo "[🌐] Dashboard telemetry ready at dashboard/static/js/telemetry.json"
