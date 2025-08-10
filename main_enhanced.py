#!/usr/bin/env python3
# Labeled: Main - Headless Trading Loop with Real-Time OCO Display

# 🔒 BOT_LOCK FAILSAFE - Ultimate veto power over autonomous trading
import os
import sys

# Failsafe: If lock file is present, halt immediately
lock_file = os.path.join(os.path.dirname(__file__), ".BOT_LOCK")
if os.path.exists(lock_file):
    print("⛔ BOT_LOCK present. Exiting for safety.")
    print("🔓 To unlock: rm /mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/.BOT_LOCK")
    sys.exit(1)

print("🟢 BOT_LOCK check passed - Autonomous trading authorized")

import platform
import subprocess

def try_dns_lock():
    if "WSL" in platform.uname().release:
        print("⚠️ WSL detected — skipping chattr DNS lock.")
        return
    try:
        try_dns_lock()
        print("✅ DNS lock applied.")
    except Exception as e:
        print(f"❌ DNS lock failed: {e}")

import time
import asyncio
import pandas as pd
import json
from datetime import datetime
from dotenv import load_dotenv

# Import our modules
from router_live_hardcoded import OandaRouter
from strategies import MODEL_A, MODEL_B, MODEL_C, MODEL_D, manual_rsi, manual_macd_hist
from smart_logic import SmartLogic
from model_wrapper import ModelWrapper
from guardian import verify_constitutional_pin
# Enhanced Risk Mitigation Imports
from enhanced_oco_validator import check_enhanced_oco_status
from cobra_strike_overlay import cobra_strike_consensus
from profit_gating_overlay import ProfitGatingManager


load_dotenv()

class HorsemenBot:
    def __init__(self):
        # ANSI color codes for real-time display
        self.WHITE = '\033[97m'
        self.BLUE = '\033[94m' 
        self.GREEN = '\033[92m'
        self.RED = '\033[91m'
        self.YELLOW = '\033[93m'
        self.RESET = '\033[0m'
        self.BOLD = '\033[1m'
        self.CYAN = '\033[96m'
        
        print(f"{self.CYAN}{self.BOLD}🤖 INITIALIZING OANDA HORSEMEN BOT...{self.RESET}")
        
        # Initialize components
        self.router = OandaRouter()  # This will verify PIN
        self.smart = SmartLogic(os.getcwd())
        
        # Load models
        self.models = {
            'A': {
                'light': ModelWrapper('models/wolfpack_A/light.json'),
                'heavy': ModelWrapper('models/wolfpack_A/heavy.json')
            },
            'B': {
                'light': ModelWrapper('models/wolfpack_B/light.json'), 
                'heavy': ModelWrapper('models/wolfpack_B/heavy.json')
            },
            'C': {
                'light': ModelWrapper('models/wolfpack_C/light.json'),
                'heavy': ModelWrapper('models/wolfpack_C/heavy.json')
            },
            'D': {
                'light': ModelWrapper('models/wolfpack_D/light.json'),
                'heavy': ModelWrapper('models/wolfpack_D/heavy.json')
            }
        }
        
        # Load strategies
        self.strategies = {
            'A': [cls() for cls in MODEL_A],
            'B': [cls() for cls in MODEL_B], 
            'C': [cls() for cls in MODEL_C],
            'D': [cls() for cls in MODEL_D]
        }
        
        # Get trading pairs
        self.instruments = os.getenv('TOP_PAIRS', 'EUR_USD,USD_JPY,GBP_USD').split(',')
        
        # Trading state
        self.is_running = True
        self.trade_count = 0
        self.oco_pairs = {}  # Track OCO order pairs
        
        print(f"{self.GREEN}✅ OANDA BOT INITIALIZED{self.RESET}")
        self.print_dashboard_header()
    
    def print_dashboard_header(self):
        """Print real-time trading dashboard with parameters"""
        print(f"\n{self.CYAN}{'═' * 80}{self.RESET}")
        print(f"{self.CYAN}{self.BOLD}                    OANDA LIVE TRADING DASHBOARD{self.RESET}")
        print(f"{self.CYAN}{'═' * 80}{self.RESET}")
        print(f"{self.YELLOW}TRADING PARAMETERS:{self.RESET}")
        print(f"  • ML Confidence Min: {self.GREEN}{os.getenv('ML_CONFIDENCE_MIN', '0.8')}{self.RESET}")
        print(f"  • Max Risk per Trade: {self.GREEN}{os.getenv('MAX_RISK_PER_TRADE', '0.02')}{self.RESET}")
        print(f"  • OCO Mandatory: {self.GREEN}{os.getenv('OCO_MANDATORY', 'true')}{self.RESET}")
        print(f"  • Max Trade Duration: {self.GREEN}{os.getenv('MAX_TRADE_DURATION_HOURS', '6')} hours{self.RESET}")
        print(f"  • Trading Pairs: {self.GREEN}{', '.join(self.instruments)}{self.RESET}")
        print(f"{self.CYAN}{'─' * 80}{self.RESET}")
        print(f"{self.WHITE}{self.BOLD}Main Orders: WHITE{self.RESET}  |  {self.BLUE}{self.BOLD}OCO Orders: BLUE{self.RESET}")
        print(f"{self.CYAN}{'═' * 80}{self.RESET}\n")
    
    def print_oco_order_display(self, signal, price, units, sl, tp, order_id=None):
        """Display OCO order with color coding - Main order WHITE, OCO in BLUE"""
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        
        # Main order display (WHITE)
        print(f"\n{self.BOLD}{self.GREEN}═══ LIVE ORDER EXECUTED ═══{self.RESET}")
        print(f"{self.YELLOW}[{timestamp}]{self.RESET}")
        print(f"{self.WHITE}{self.BOLD}MAIN ORDER: {signal['signal']} {signal['instrument']}{self.RESET}")
        print(f"{self.WHITE}├─ Units: {units:,}{self.RESET}")
        print(f"{self.WHITE}├─ Price: {price:.5f}{self.RESET}")
        print(f"{self.WHITE}├─ Strategy: {signal['strategy']} (Model {signal['model']}){self.RESET}")
        print(f"{self.WHITE}└─ ML Confidence: {signal['ml_confidence']:.1%}{self.RESET}")
        
        # OCO Orders display (BLUE) - positioned directly next to main order
        print(f"{self.BLUE}{self.BOLD}OCO PROTECTION:{self.RESET}")
        print(f"{self.BLUE}├─ Stop Loss:  {sl:.5f}{self.RESET}")
        print(f"{self.BLUE}├─ Take Profit: {tp:.5f}{self.RESET}")
        
        # Calculate risk/reward
        if signal['signal'] == 'BUY':
            risk = price - sl
            reward = tp - price
        else:
            risk = sl - price  
            reward = price - tp
            
        rr_ratio = reward / risk if risk > 0 else 0
        print(f"{self.BLUE}└─ Risk/Reward: {rr_ratio:.1f}:1{self.RESET}")
        
        if order_id:
            print(f"{self.YELLOW}Order ID: {order_id}{self.RESET}")
            # Store OCO pair for tracking
            self.oco_pairs[order_id] = {'sl': sl, 'tp': tp, 'main_price': price}
        
        print(f"{self.GREEN}{'─' * 50}{self.RESET}\n")
    
    async def get_ml_prediction(self, data, model_name):
        """Get ML prediction with confidence"""
        try:
            lalive = data.iloc[-1]
            features = pd.Series([
                lalive.get('rsi', 50),
                lalive.get('macd_hist', 0),
                lalive.get('ema_20', lalive['close']),
                lalive.get('price_change', 0),
                lalive.get('volume_ma', lalive['volume']),
                lalive.get('volatility', 0.01),
                lalive['close'],
                lalive['volume']
            ])
            
            # Get prediction from both light and heavy models
            light_conf, light_signal = self.models[model_name]['light'].predict(features)
            heavy_conf, heavy_signal = self.models[model_name]['heavy'].predict(features)
            
            # Combine predictions
            combined_conf = (light_conf * 0.3) + (heavy_conf * 0.7)
            final_signal = heavy_signal if heavy_conf > light_conf else light_signal
            
            return combined_conf, final_signal
            
        except Exception as e:
            print(f"{self.RED}❌ ML prediction error: {e}{self.RESET}")
            return 0.5, 'HOLD'
    
    async def execute_strategies(self, instrument, data):
        """Execute all strategies for given instrument"""
        signals = []
        
        for model_name, strategy_list in self.strategies.items():
            ml_conf, ml_signal = await self.get_ml_prediction(data, model_name)
            
            if not self.smart.ml_confidence_filter(ml_conf):
                continue
            
            for strategy in strategy_list:
                try:
                    strategy_signal = strategy.execute(data.copy(), ml_conf)
                    
                    if strategy_signal in ['BUY', 'SELL']:
                        signals.append({
                            'instrument': instrument,
                            'signal': strategy_signal,
                            'strategy': strategy.name,
                            'model': model_name,
                            'ml_confidence': ml_conf,
                            'ml_signal': ml_signal,
                            'price': data['close'].iloc[-1],
                            'timestamp': datetime.now().isoformat()
                        })
                        
                except Exception as e:
                    print(f"{self.RED}❌ Strategy {strategy.name} error: {e}{self.RESET}")
        
        return signals
    
    async def place_trade(self, signal):
        """Place trade with OCO protection and real-time display"""
        try:
            price = signal['price']
            
            # Calculate position size
            account_balance = 10000
            sl_distance = price * 0.001  # 0.1% stop loss
            units = self.smart.risk_size_calculator(account_balance, price, price - sl_distance)
            
            # Calculate OCO levels
            sl, tp = self.smart.oco_enforce(price, sl_distance, signal['signal'])
            
            # Display order with OCO visualization
            self.print_oco_order_display(signal, price, units, sl, tp)
            
            # Place order
            success = self.router.place_order(
                instrument=signal['instrument'],
                units=units if signal['signal'] == 'BUY' else -units,
                price=price,
                sl=sl,
                tp=tp
            )
            
            if success:
                trade_data = {
                    'confidence': signal['ml_confidence'],
                    'risk_pct': float(os.getenv('MAX_RISK_PER_TRADE', 0.02)),
                    'units': units,
                    'sl': sl,
                    'tp': tp,
                    **signal
                }
                
                reason = f"{signal['strategy']} {signal['signal']} on {signal['instrument']} - ML:{signal['ml_confidence']:.2f} Model:{signal['model']}"
                self.smart.log_trade_record(trade_data, reason)
                
                self.trade_count += 1
                print(f"{self.GREEN}🎯 TRADE #{self.trade_count} COMPLETED{self.RESET}")
                return True
            
        except Exception as e:
            print(f"{self.RED}❌ Trade placement error: {e}{self.RESET}")
            return False
    
    async def trading_loop(self):
        """Main trading loop with real-time display"""
        print(f"{self.GREEN}🚀 STARTING LIVE TRADING LOOP...{self.RESET}")
        
        while self.is_running:
            try:
                # 🔒 Periodic BOT_LOCK check during runtime
                lock_file = os.path.join(os.path.dirname(__file__), ".BOT_LOCK")
                if os.path.exists(lock_file):
                    print(f"{self.RED}⛔ BOT_LOCK detected during runtime. Shutting down...{self.RESET}")
                    print(f"{self.YELLOW}🔓 To unlock: rm {lock_file}{self.RESET}")
                    self.is_running = False
                    break
                
                print(f"\n{self.CYAN}📊 SCANNING {len(self.instruments)} INSTRUMENTS...{self.RESET}")
                
                for instrument in self.instruments:
                    try:
                        # Get market data
                        data = self.router.get_market_data(instrument)
                        
                        if data.empty:
                            print(f"{self.YELLOW}⚠️ No data for {instrument}{self.RESET}")
                            continue
                        
                        # Add technical indicators
                        data['rsi'] = manual_rsi(data['close'])
                        data['macd_hist'] = manual_macd_hist(data['close'])
                        data['ema_20'] = data['close'].ewm(span=20).mean()
                        data['price_change'] = data['close'].pct_change()
                        data['volume_ma'] = data['volume'].rolling(20).mean()
                        data['volatility'] = data['close'].rolling(20).std()
                        
                        # Execute strategies
                        signals = await self.execute_strategies(instrument, data)
                        
                        # Print scan results with current price
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        current_price = data['close'].iloc[-1]
                        rsi_val = data['rsi'].iloc[-1] if not data['rsi'].isna().iloc[-1] else 50
                        
                        print(f"{self.CYAN}[{timestamp}] {instrument}: Price {current_price:.5f} | RSI {rsi_val:.1f} | {len(signals)} signals{self.RESET}")
                        
                        # Process signals with enhanced display
                        for signal in signals:
                            print(f"{self.GREEN}🎯 SIGNAL DETECTED: {signal['strategy']} suggests {signal['signal']} on {instrument} (ML: {signal['ml_confidence']:.1%}){self.RESET}")
                            await self.place_trade(signal)
                        
                    except Exception as e:
                        print(f"{self.RED}❌ Error processing {instrument}: {e}{self.RESET}")
                
                # Sleep between cycles
                print(f"{self.CYAN}💤 Next scan in 15 seconds... (Trades today: {self.trade_count}){self.RESET}")
                await asyncio.sleep(15)
                
            except KeyboardInterrupt:
                print(f"\n{self.RED}🛑 SHUTDOWN REQUESTED...{self.RESET}")
                self.is_running = False
                break
            except Exception as e:
                print(f"{self.RED}❌ Trading loop error: {e}{self.RESET}")
                await asyncio.sleep(30)
    
    def run(self):
        """Run the bot"""
        try:
            asyncio.run(self.trading_loop())
        except Exception as e:
            print(f"{self.RED}❌ Bot crashed: {e}{self.RESET}")
        finally:
            print(f"{self.GREEN}🏁 OANDA HORSEMEN BOT SHUTDOWN COMPLETE{self.RESET}")


    def execute_trade_enhanced(self, signal):
        """🛡️ ENHANCED TRADE EXECUTION with Multi-Layer Protection"""
        try:
            # 1. Cobra Strike Consensus Check
            model_predictions = {
                'MODEL_A': signal['ml_confidence'],
                'MODEL_B': signal['ml_confidence'] * 0.95,  # Simulate other models
                'MODEL_C': signal['ml_confidence'] * 0.92,
                'RSI': 0.75,  # Placeholder
            }
            
            consensus_ok, avg_confidence = cobra_strike_consensus(model_predictions, 0.82)
            if not consensus_ok:
                print(f"🚫 COBRA STRIKE BLOCK: Insufficient model consensus")
                return False
            
            # 2. Enhanced Position Sizing (Win Streak Bonus)
            
            # Check recent performance (liveplified)
            recent_wins = 2  # This would come from your trade history
            confidence_multiplier = 1.0
            
            if recent_wins >= 2 and signal['ml_confidence'] > 0.90:
                confidence_multiplier = 2.5  # Perfect storm bonus
                print(f"🚀 PERFECT STORM BONUS: 2.5x position size")
            elif signal['ml_confidence'] > 0.90:
                confidence_multiplier = 2.0  # High confidence bonus
                print(f"🎯 HIGH CONFIDENCE BONUS: 2.0x position size")
            elif recent_wins >= 2:
                confidence_multiplier = 1.5  # Win streak bonus
                print(f"📈 WIN STREAK BONUS: 1.5x position size")
            
            enhanced_units = int(base_units * confidence_multiplier)
            enhanced_units = min(enhanced_units, base_units * 3)  # Cap at 3x
            
            # 3. Dynamic OCO Calculation
            price = signal['price']
            
            # Tighter stops for higher confidence
            if signal['ml_confidence'] > 0.90:
                sl_distance = price * 0.003  # 0.3% stop for high confidence
                tp_distance = price * 0.009  # 0.9% target (3:1 R/R)
            else:
                sl_distance = price * 0.005  # 0.5% stop for normal
                tp_distance = price * 0.010  # 1.0% target (2:1 R/R)
            
            if signal['signal'] == 'BUY':
                sl = price - sl_distance
                tp = price + tp_distance
            else:
                sl = price + sl_distance  
                tp = price - tp_distance
            
            print(f"💪 ENHANCED EXECUTION:")
            print(f"   Signal: {signal['signal']} {signal['instrument']}")
            print(f"   Units: {enhanced_units:,} (multiplier: {confidence_multiplier}x)")
            print(f"   ML Confidence: {signal['ml_confidence']:.1%}")
            print(f"   Entry: {price:.5f}")
            print(f"   Stop Loss: {sl:.5f} ({sl_distance/price:.1%})")
            print(f"   Take Profit: {tp:.5f} ({tp_distance/price:.1%})")
            
            # 4. Place Enhanced Order
            success = self.router.place_order(
                instrument=signal['instrument'],
                units=enhanced_units if signal['signal'] == 'BUY' else -enhanced_units,
                price=price,
                sl=sl,
                tp=tp
            )
            
            if success:
                # 5. Start Profit Gating Monitor for this trade
                trade_data = {
                    'id': f"{signal['instrument']}_{int(time.time())}",
                    'entry_price': price,
                    'entry_time': datetime.now(),
                    'confidence': signal['ml_confidence'],
                    'strategy': signal['strategy']
                }
                
                print(f"✅ ENHANCED TRADE EXECUTED - Monitoring activated")
                return True
            else:
                print(f"❌ Enhanced trade execution failed")
                return False
                
        except Exception as e:
            print(f"❌ Enhanced execution error: {e}")
            return False


if __name__ == "__main__":
    if '--backlive' in sys.argv:
        print("🔐 BACKlive MODE REQUIRES CONSTITUTIONAL PIN")
        pin = verify_constitutional_pin()
        print(f"✅ Backlive authorized with PIN: {pin[:2]}***")
        print("📈 BACKlive MODE - No live trades will be placed")
        sys.exit(0)
    
    # Start live trading with real-time OCO display
    bot = HorsemenBot()
    bot.run()

# === $400/DAY PROFIT SYSTEM INTEGRATION ===
import sys
sys.path.append('/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda')

try:
    from smart_scaling_module import dynamic_trade_size, profit_target_reached, daily_profit_tracker
    from position_rotation_guard import check_and_rotate
    print("✅ $400/DAY PROFIT MODULES LOADED")
except ImportError as e:
    print(f"⚠️ Profit modules not found: {e}")

# Override risk calculation with smart scaling
def enhanced_risk_calculator(self, account_balance, price, sl_price, ml_confidence):
    """Enhanced risk calculator with confidence-based scaling"""
    try:
        # Check daily profit target
        if profit_target_reached():
            print("🎯 DAILY TARGET REACHED: $400+ profit - Reducing risk")
            return 100  # Minimal size when target reached
            
        # Use smart scaling based on ML confidence
        optimal_units = dynamic_trade_size(ml_confidence, account_balance)
        
        # Apply position rotation check
        api = self.router.api
        account_id = os.getenv('OANDA_ACCOUNT_ID')
        check_and_rotate(api, account_id)
        
        return optimal_units
        
    except Exception as e:
        print(f"⚠️ Enhanced risk calc error: {e}")
        # Fallback to original calculation
        return self.smart.risk_size_calculator(account_balance, price, sl_price)

# Monkey patch the risk calculator
# This will be applied during trade execution
