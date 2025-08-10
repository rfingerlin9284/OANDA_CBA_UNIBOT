#!/usr/bin/env python3
"""
🔐 OCO Trade Engine for OANDA - Professional Risk Management
Enforces mandatory OCO orders with calculated SL/TP and proper position sizing
"""

import json
import requests
import time
from datetime import datetime

class OandaOCOTradeEngine:
    def __init__(self, config_path="small_cap_config_oanda.json"):
        self.config = self.load_config(config_path)
        self.account_id = self.config["account_id"]
        self.api_token = self.config["api_token"]
        self.base_url = "https://api-fxtrade.oanda.com" if self.config["live_mode"] else "https://api-fxtrade.oanda.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
    def load_config(self, path):
        """Load configuration from JSON file"""
        with open(path, 'r') as f:
            config = json.load(f)
        print(f"🧠 Config loaded: OCO={config['oco_required']}, SL={config['stop_loss_pct']*100}%, TP={config['take_profit_pct']*100}%")
        return config
    
    def get_account_balance(self):
        """Get current account balance"""
        try:
            response = requests.get(
                f"{self.base_url}/v3/accounts/{self.account_id}",
                headers=self.headers
            )
            if response.status_code == 200:
                data = response.json()
                balance = float(data['account']['balance'])
                equity = float(data['account']['NAV'])
                print(f"💰 Account Balance: ${balance:.2f} | Equity: ${equity:.2f}")
                return balance, equity
            else:
                print(f"❌ Failed to get account info: {response.status_code}")
                return None, None
        except Exception as e:
            print(f"❌ Error getting account balance: {e}")
            return None, None
    
    def get_current_price(self, pair):
        """Get current bid/ask prices for currency pair"""
        try:
            response = requests.get(
                f"{self.base_url}/v3/accounts/{self.account_id}/pricing",
                headers=self.headers,
                params={"instruments": pair}
            )
            if response.status_code == 200:
                data = response.json()
                price_data = data['prices'][0]
                bid = float(price_data['bids'][0]['price'])
                ask = float(price_data['asks'][0]['price'])
                spread = ask - bid
                print(f"📈 {pair}: Bid={bid} Ask={ask} Spread={spread:.5f}")
                return bid, ask, spread
            else:
                print(f"❌ Failed to get price for {pair}: {response.status_code}")
                return None, None, None
        except Exception as e:
            print(f"❌ Error getting price for {pair}: {e}")
            return None, None, None
    
    def calc_pip_value(self, pair, units):
        """Calculate pip value for position sizing"""
        # Simplified pip value calculation
        if "JPY" in pair:
            return 0.01 * units / 10000  # JPY pairs
        else:
            return 0.0001 * units / 10000  # Major pairs
    
    def calculate_position_size(self, pair, entry_price, sl_price, account_balance):
        """Calculate position size based on risk management rules"""
        if not self.config["oco_required"]:
            print("❌ OCO disabled. Trade blocked.")
            return 0
        
        # Calculate risk amount (2% of balance)
        risk_amount = account_balance * self.config["risk_per_trade"]
        
        # Calculate SL distance in pips
        pip_size = 0.01 if "JPY" in pair else 0.0001
        sl_pips = abs(entry_price - sl_price) / pip_size
        
        # Prevent trades with tiny SL distance
        if sl_pips < 5:
            print(f"❌ SL distance too small: {sl_pips:.1f} pips")
            return 0
        
        # Calculate units based on risk
        pip_value_per_unit = pip_size * (10 if "JPY" in pair else 1)
        units = int(risk_amount / (sl_pips * pip_value_per_unit))
        
        # Apply lot size cap
        
        print(f"🧮 Position Calc: Risk=${risk_amount:.2f}, SL={sl_pips:.1f}pips, Units={units}")
        return units
    
    def calculate_sl_tp_levels(self, pair, entry_price, direction):
        """Calculate SL and TP levels based on config percentages"""
        sl_pct = self.config["stop_loss_pct"]
        tp_pct = self.config["take_profit_pct"]
        
        if direction == "buy":
            sl_price = entry_price * (1 - sl_pct)
            tp_price = entry_price * (1 + tp_pct)
        else:  # sell
            sl_price = entry_price * (1 + sl_pct)
            tp_price = entry_price * (1 - tp_pct)
        
        # Apply decimal precision
        precision = self.config["decimal_precision"].get(pair, 5)
        sl_price = round(sl_price, precision)
        tp_price = round(tp_price, precision)
        
        # Calculate RR ratio
        if direction == "buy":
            risk_pips = (entry_price - sl_price) / (0.01 if "JPY" in pair else 0.0001)
            reward_pips = (tp_price - entry_price) / (0.01 if "JPY" in pair else 0.0001)
        else:
            risk_pips = (sl_price - entry_price) / (0.01 if "JPY" in pair else 0.0001)
            reward_pips = (entry_price - tp_price) / (0.01 if "JPY" in pair else 0.0001)
        
        rr_ratio = reward_pips / risk_pips if risk_pips > 0 else 0
        
        print(f"🎯 SL/TP Calc: Entry={entry_price}, SL={sl_price}, TP={tp_price}, RR={rr_ratio:.2f}:1")
        return sl_price, tp_price, rr_ratio
    
    def place_oco_trade(self, pair, direction, ml_confidence, units=None):
        """Place OCO trade with mandatory SL and TP"""
        print(f"\n🚀 PLACING OCO TRADE: {pair} {direction.upper()}")
        print(f"🧠 ML Confidence: {ml_confidence:.3f} (min: {self.config['ml_confidence_min']})")
        
        # Pre-flight checks
        if not self.config["oco_required"]:
            print("❌ OCO disabled. Trade blocked.")
            return False
        
        if ml_confidence < self.config["ml_confidence_min"]:
            print(f"❌ ML confidence too low: {ml_confidence:.3f}")
            return False
        
        # Get current prices and account info
        bid, ask, spread = self.get_current_price(pair)
        if bid is None:
            return False
        
        balance, equity = self.get_account_balance()
        if balance is None:
            return False
        
        # Determine entry price
        entry_price = ask if direction == "buy" else bid
        
        # Calculate SL and TP levels
        sl_price, tp_price, rr_ratio = self.calculate_sl_tp_levels(pair, entry_price, direction)
        
        # Check minimum RR ratio
        min_rr = self.config.get("min_reward_risk_ratio", 2.0)
        if rr_ratio < min_rr:
            print(f"❌ RR ratio too low: {rr_ratio:.2f} (min: {min_rr})")
            return False
        
        # Calculate position size
        if units is None:
            units = self.calculate_position_size(pair, entry_price, sl_price, balance)
        
        if units <= 0:
            print("❌ Invalid position size calculated")
            return False
        
        # Prepare OCO order payload
        order_payload = {
            "order": {
                "type": "MARKET",
                "instrument": pair,
                "units": str(units if direction == "buy" else -units),
                "timeInForce": "FOK",
                "stopLossOnFill": {
                    "price": str(sl_price),
                    "timeInForce": "GTC"
                },
                "takeProfitOnFill": {
                    "price": str(tp_price),
                    "timeInForce": "GTC"
                }
            }
        }
        
        print(f"🔐 OCO ORDER DETAILS:")
        print(f"   📊 Pair: {pair}")
        print(f"   📈 Direction: {direction.upper()}")
        print(f"   💰 Units: {units}")
        print(f"   🎯 Entry: {entry_price}")
        print(f"   🛑 Stop Loss: {sl_price}")
        print(f"   ✅ Take Profit: {tp_price}")
        print(f"   📊 RR Ratio: {rr_ratio:.2f}:1")
        print(f"   🧠 ML Confidence: {ml_confidence:.3f}")
        
        # Execute the trade
        try:
            response = requests.post(
                f"{self.base_url}/v3/accounts/{self.account_id}/orders",
                headers=self.headers,
                json=order_payload
            )
            
            if response.status_code == 201:
                data = response.json()
                order_id = data['orderFillTransaction']['id']
                trade_id = data['orderFillTransaction']['tradeOpened']['tradeID']
                
                print(f"✅ OCO TRADE EXECUTED!")
                print(f"   📋 Order ID: {order_id}")
                print(f"   🔄 Trade ID: {trade_id}")
                
                # Log trade to CSV
                self.log_trade_to_csv(pair, direction, entry_price, sl_price, tp_price, units, ml_confidence, order_id)
                
                return True
            else:
                print(f"❌ Order failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Exception placing order: {e}")
            return False
    
    def log_trade_to_csv(self, pair, direction, entry, sl, tp, units, confidence, order_id):
        """Log trade details to CSV file"""
        if not self.config.get("log_trades_to_csv", False):
            return
        
        import csv
        import os
        
        csv_file = self.config.get("csv_log_path", "trade_log.csv")
        file_exists = os.path.isfile(csv_file)
        
        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['timestamp', 'pair', 'direction', 'entry', 'sl', 'tp', 'units', 'confidence', 'order_id', 'strategy'])
            
            writer.writerow([
                datetime.now().isoformat(),
                pair, direction, entry, sl, tp, units, confidence, order_id,
                self.config.get("strategy_name", "Unknown")
            ])
        
        print(f"📝 Trade logged to {csv_file}")
    
    def validate_trade_conditions(self, pair, ml_confidence):
        """Validate all trade conditions before execution"""
        print(f"\n🔍 VALIDATING TRADE CONDITIONS for {pair}")
        
        checks = []
        
        # OCO requirement
        if self.config["oco_required"]:
            checks.append("✅ OCO required: ENABLED")
        else:
            checks.append("❌ OCO required: DISABLED")
            return False
        
        # ML confidence
        if ml_confidence >= self.config["ml_confidence_min"]:
            checks.append(f"✅ ML confidence: {ml_confidence:.3f} >= {self.config['ml_confidence_min']}")
        else:
            checks.append(f"❌ ML confidence: {ml_confidence:.3f} < {self.config['ml_confidence_min']}")
            return False
        
        # Bot enabled
        if self.config.get("bot_enabled", True):
            checks.append("✅ Bot enabled: TRUE")
        else:
            checks.append("❌ Bot enabled: FALSE")
            return False
        
        for check in checks:
            print(f"   {check}")
        
        return True

if __name__ == "__main__":
    print("🔐 OCO Trade Engine - OANDA")
    print("=" * 50)
    
    engine = OandaOCOTradeEngine()
    
    # Test validation
    
        # Uncomment to place actual trade:
    else:
