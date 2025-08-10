#!/bin/bash

mkdir -p logs
touch logs/clean_ml_stream.log

echo "==============================="
echo "RBOTzilla Commander Terminal 🔥"
echo "Only commander-level events, no tick spam."
echo "Log: logs/clean_ml_stream.log"
echo "==============================="

tail -n 50 -f logs/clean_ml_stream.log
