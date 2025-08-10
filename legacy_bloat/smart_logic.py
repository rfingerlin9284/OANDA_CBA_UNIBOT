#!/usr/bin/env python3
# Labeled: Smart Logic - Aggression & Enforcement
# Instructions: Class for leverage/scaling/compounding/reallocation/OCO/trailing/logging (JSON/txt). Used by main.py for trade decisions.
import os
import pandas as pd
import time
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
OCO_MANDATORY = os.getenv('OCO_MANDATORY', 'true') == 'true'
ML_CONF_MIN = float(os.getenv('ML_CONFIDENCE_MIN', 0.80))
MAX_RISK = float(os.getenv('MAX_RISK_PER_TRADE', 0.02))
MAX_DURATION = int(os.getenv('MAX_TRADE_DURATION_HOURS', 6)) * 3600

logging.basicConfig(filename='logs/smart.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class SmartLogic:
    def __init__(self, platform_path):
        self.platform_path = platform_path
        self.trades = []
        self.pnl_history = []
        
    def oco_enforce(self, price, sl_distance, side):
        """Calculate OCO stop loss and take profit"""
        if not OCO_MANDATORY:
            raise ValueError("❌ OCO is MANDATORY - Constitutional violation")
        
        if side.lower() == 'buy':
            sl = price - sl_distance
            tp = price + (sl_distance * 2)  # 2:1 RR
        else:
            sl = price + sl_distance  
            tp = price - (sl_distance * 2)
        
        return sl, tp
    
    def ml_confidence_filter(self, confidence):
        """Filter trades by ML confidence threshold"""
        return confidence >= ML_CONF_MIN
    
    def risk_size_calculator(self, account_balance, price, sl_price):
        """Calculate position size based on risk"""
        risk_amount = account_balance * MAX_RISK
        price_diff = abs(price - sl_price)
        units = risk_amount / price_diff
        return int(units)
    
    def log_trade_record(self, trade_data, reason):
        """Log trade with JSON and text format"""
        trade_record = {
            'timestamp': datetime.now().isoformat(),
            'platform': os.path.basename(self.platform_path),
            'data': trade_data,
            'reason': reason,
            'ml_confidence': trade_data.get('confidence', 0),
            'risk_used': trade_data.get('risk_pct', MAX_RISK)
        }
        
        # JSON log
        json_log = os.path.join(self.platform_path, 'logs', f"trade_json_{datetime.now().strftime('%Y%m%d')}.json")
        with open(json_log, 'a') as f:
            f.write(json.dumps(trade_record) + '\n')
        
        # Text log
        text_log = os.path.join(self.platform_path, 'logs', f"trade_text_{datetime.now().strftime('%Y%m%d')}.log")
        with open(text_log, 'a') as f:
            f.write(f"{datetime.now()} - {reason}\n")
        
        logging.info(f"Trade logged: {reason}")

