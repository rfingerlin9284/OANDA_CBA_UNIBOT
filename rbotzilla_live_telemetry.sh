#!/bin/bash
# 🔁 RBOTzilla Telemetry Viewer (Live Scroll + Color)

LOG_FILE="logs/ml_predictions.log"

# Wait if the log file doesn't exist yet
while [[ ! -f "$LOG_FILE" ]]; do
    echo "⏳ Waiting for $LOG_FILE..."
    sleep 2
done

tail -n 0 -F "$LOG_FILE" | while read -r line; do
    prediction=$(echo "$line" | grep -oP '"prediction":"\K[^"]+')
    confidence=$(echo "$line" | grep -oP '"confidence":\K[0-9.]+')
    model=$(echo "$line" | grep -oP '"model":"\K[^"]+')
    time_utc=$(echo "$line" | grep -oP '"timestamp":"\K[^"]+')
    system=$(echo "$line" | grep -oP '"system":"\K[^"]+')

    # Set color
    if [[ $prediction == "BUY" ]]; then
        color="\e[1;32m"  # Green
    elif [[ $prediction == "SELL" ]]; then
        color="\e[1;31m"  # Red
    else
        color="\e[1;33m"  # Yellow
    fi

    # Output formatted line
    echo -e "${color}[${system}] ${time_utc} | Prediction: $prediction | Confidence: ${confidence} | Model: $model\e[0m"
done
