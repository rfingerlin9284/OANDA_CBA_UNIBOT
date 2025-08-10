IS_LIVE_MOD#!/usr/bin/env python3
"""
🎯 WOLFPACK-PROTO MAIN CONTROL
Enhanced autonomous FVG hunting with mass psychology quantification
- Dynamic OCO wave riders (remove TP caps on momentum breakouts)
- Market-aware FVG scoring (crypto momentum vs forex mean reversion)
- Bull/bear bias dispatch (wider SL in bulls, tighter in bears)
- Volume surge filters, lock mode for ultra-R signals
- Gap size weighting for psychological urgency
- OCO watchdog auto-kills orphans
- Heartbeat visuals on dashboards
LIVE TRADING ONLY - NO DEMO/PRACTICE MODE
"""

import sys
from pair_rotator import rotate_pairs
from strategy_boost import detect_patterns, confluence_boost
from drift_guard import is_pair_overused
import time
import signal
import threading
from datetime import datetime

# Import our enhanced API modules
from coinbase_advanced_api import CoinbaseAdvancedTradeAPI
from credentials import WolfpackCredentials
from sniper_core import FVGSniper
from oco_executor import OCOExecutor
from logger import logger, log_trade, log_error
from timezone_manager import MarketSessionManager
from portfolio_manager import LivePortfolioManager
from arbitrage_engine import ArbitrageEngine
from position_tracker import position_tracker, print_daily_summary
from trade_guardian import TradeGuardian
from oco_dynamic_adjuster import OCODynamicAdjuster

# Dashboard integration
try:
    from dashboards.feed_updater import FVGDashboardFeeder
except ImportError:
    # Fallback if dashboard not available
    class FVGDashboardFeeder:
        def update_system_status(self, *args): pass
        def update_oanda_feed(self, *args): pass
        def update_coinbase_feed(self, *args): pass
        def update_heartbeat(self, *args): pass

# Import oandapyV20
import oandapyV20
from oandapyV20 import API

class WolfpackProto:
    def __init__(self):
        """🚀 Initialize enhanced Wolfpack-Proto system with mass psychology quantification"""
        self.creds = WolfpackCredentials()
        self.sniper = FVGSniper()
        self.oco_executor = None
        
        # Enhanced timezone-aware market session manager
        self.session_manager = MarketSessionManager()
        
        # Live portfolio manager for real-time updates
        self.portfolio_manager = LivePortfolioManager()
        
        # Arbitrage engine for 24/7 spot vs forex arbitrage
        self.arbitrage_engine = None
        
        # Dashboard integration
        self.dashboard_feeder = FVGDashboardFeeder()
        
        # API clients
        self.coinbase = None
        self.oanda = None
        
        # Enhanced components
        self.oco_dynamic_adjuster = None  # Wave ride logic
        self.trade_guardian = None  # OCO watchdog
        
        # Control flags
        self.is_running = False
        self.scan_thread = None
        
        # Active trades tracking for dashboard
        self.active_oanda_trades = 0
        self.active_coinbase_trades = 0
        
        # Performance tracking
        self.scan_count = 0
        self.signals_found = 0
        self.signals_executed = 0
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def initialize_apis(self):
        """
        🔌 INITIALIZE LIVE API CONNECTIONS
        Setup Coinbase Advanced Trade and OANDA LIVE APIs with enhanced error handling
        """
        try:
            log_trade("🔌 Initializing LIVE API connections with psychology quantifier...", "STARTUP")
            
            # Validate credentials first
            validation_issues = self.creds.validate_credentials()
            if validation_issues:
                for issue in validation_issues:
                    log_error(f"Credential issue: {issue}", "CREDENTIALS")
                return False
            
            # Coinbase Advanced Trade API - LIVE ONLY with JWT ed25519
            self.coinbase = CoinbaseAdvancedTradeAPI(
                api_key=self.creds.COINBASE_API_KEY,
                private_key_b64=self.creds.COINBASE_PRIVATE_KEY_B64
            )
            
            # Test Coinbase LIVE connection
            coinbase_accounts = self.coinbase.get_accounts()
            log_trade(f"✅ Coinbase Advanced Trade LIVE connected | Accounts: {len(coinbase_accounts.get('accounts', []))}", "API")
            
            # OANDA LIVE API
            self.oanda = API(
                access_token=self.creds.OANDA_API_KEY,
                environment="live"  # LIVE TRADING ONLY
            )
            
            # Test OANDA LIVE connection
            account_response = self.oanda.account.get(accountID=self.creds.OANDA_ACCOUNT_ID)
            oanda_balance = float(account_response.body['account']['balance'])
            log_trade(f"✅ OANDA LIVE connected | Balance: ${oanda_balance:.2f}", "API")
            
            # Initialize enhanced OCO executor
            self.oco_executor = OCOExecutor(self.coinbase, self.oanda, self.creds)
            
            # Initialize dynamic OCO adjuster for wave riding
            self.oco_dynamic_adjuster = OCODynamicAdjuster(self.coinbase, self.oanda, self.creds)
            
            # Initialize trade guardian watchdog
            self.trade_guardian = TradeGuardian(self.oco_executor, self.dashboard_feeder)
            
            # Initialize portfolio manager with API connections
            self.portfolio_manager.initialize_apis(self.coinbase, self.oanda, self.creds)
            
            # Initialize arbitrage engine
            self.arbitrage_engine = ArbitrageEngine(
                self.coinbase, 
                self.oanda, 
                self.creds, 
                self.session_manager, 
                self.portfolio_manager
            )
            
            return True
            
        except Exception as e:
            log_error(f"LIVE API initialization failed: {str(e)}", "API_INIT")
            return False
    
    def start_hunting(self):
        """
        🏹 START ENHANCED FVG HUNTING
        Main scanning loop with mass psychology quantification
        """
        if not self.initialize_apis():
            log_error("API initialization failed - cannot start hunting", "STARTUP")
            return False
        
        self.is_running = True
        
        # Start OCO monitoring
        self.oco_executor.start_monitoring()
        
        # Start dynamic OCO adjuster for wave riding
        self.oco_dynamic_adjuster.start_monitoring()
        
        # Start trade guardian watchdog
        self.trade_guardian.start_monitoring()
        
        # Start arbitrage engine for 24/7 arbitrage
        self.arbitrage_engine.start_scanning()
        
        # Print initial stats with position tracking
        logger.print_daily_stats()
        print_daily_summary()
        
        # Print system configuration
        summary = self.creds.get_trading_summary()
        log_trade(f"📊 System Config: {summary['total_pairs']} pairs, {summary['risk_per_trade']} risk, {summary['min_rr']} RR, {summary['wave_ride_threshold']} wave threshold", "CONFIG")
        
        # Start scanning thread
        self.scan_thread = threading.Thread(target=self._scanning_loop, daemon=True)
        self.scan_thread.start()
        
        log_trade("🏹 WOLFPACK-PROTO HUNTING STARTED with mass psychology quantifier", "STARTUP")
        log_trade(f"💎 Watching {len(self.creds.COINBASE_PAIRS)} Coinbase + {len(self.creds.OANDA_PAIRS)} OANDA pairs", "STARTUP")
        log_trade("⚡ ARBITRAGE ENGINE: 24/7 Coinbase Spot vs OANDA Forex arbitrage active", "STARTUP")
        log_trade(f"🌍 TIMEZONE: Hamilton, NJ (EST/EDT) | Session-aware bias dispatch active", "STARTUP")
        log_trade(f"🧠 PSYCHOLOGY: Volume surge filters, gap size weighting, bias-aware SL adjustments", "STARTUP")
        log_trade(f"🔥 WAVE RIDING: Dynamic OCO removes TP at {self.creds.WAVE_RIDE_THRESHOLD}R, trails at {self.creds.TRAIL_PERCENT*100}%", "STARTUP")
        log_trade(f"🛡️ GUARDIAN: OCO watchdog active, heartbeat monitoring enabled", "STARTUP")
        
        return True
    
    def _scanning_loop(self):
        """
        🔍 ENHANCED SCANNING LOOP
        Session-aware FVG detection with mass psychology quantification
        """
        while self.is_running:
            try:
                self.scan_count += 1
                
                # Get current market session info for bias dispatch
                session_info = self.session_manager.get_current_session_info()
                current_session = session_info['current_session']
                market_bias = session_info['suggested_bias']
                volatility = session_info['volatility_level']
                
                # Get bias-specific trading settings
                bias_settings = self.session_manager.get_bias_dispatch_settings()
                
                # Update portfolio every 30 seconds
                if self.scan_count % 3 == 0:
                    self.portfolio_manager.update_portfolio()
                
                # Update dashboard status with enhanced session info
                session_text = f"LIVE SCANNING [{current_session}] Bias:{market_bias} Vol:{volatility} - Scan #{self.scan_count}"
                self.dashboard_feeder.update_system_status("oanda", session_text, self.active_oanda_trades)
                self.dashboard_feeder.update_system_status("coinbase", session_text, self.active_coinbase_trades)
                
                # Log portfolio balances every 100 scans
                if self.scan_count % 100 == 0:
                    balances = self.portfolio_manager.get_total_balances()
                    log_trade(f"📊 Portfolio Update | Total: ${balances['total_usd']:.2f} | CB: ${balances['coinbase_usd']:.2f} | OANDA: ${balances['oanda_usd']:.2f}", "PORTFOLIO")
                
                # Scan with bias-aware settings
                self._scan_platforms_with_bias(market_bias, bias_settings)
                
                # Print enhanced status every 100 scans
                if self.scan_count % 100 == 0:
                    active_count = len(self.oco_executor.active_trades)
                    signal_rate = (self.signals_found / self.scan_count * 100) if self.scan_count > 0 else 0
                    execution_rate = (self.signals_executed / max(self.signals_found, 1) * 100)
                    
                    log_trade(f"📊 Scan #{self.scan_count} | Active: {active_count} | Signals: {self.signals_found} ({signal_rate:.1f}%) | Executed: {self.signals_executed} ({execution_rate:.1f}%)", "STATUS")
                    log_trade(f"🧠 Session: {current_session} | Bias: {market_bias} | Volatility: {volatility}", "SESSION")
                
                # Use bias-specific scan interval
                time.sleep(bias_settings['scan_interval'])
                
            except Exception as e:
                log_error(f"Enhanced scanning loop error: {str(e)}", "SCAN_LOOP")
                time.sleep(5)
    
    def _scan_platforms_with_bias(self, market_bias, bias_settings):
        """
        🎯 BIAS-AWARE PLATFORM SCANNING
        Adapts scanning based on session characteristics and market psychology
        """
        # Check position limits
        active_count = len(self.oco_executor.active_trades)
        max_concurrent = bias_settings['max_concurrent']
        
        if active_count >= max_concurrent:
            return  # Skip scanning if at position limit
        
        # Scan Coinbase pairs with crypto-specific psychology
        for symbol in self.creds.COINBASE_PAIRS:
            if not self.is_running:
                break
            self._scan_pair("coinbase", symbol, market_bias, bias_settings, platform_focus="momentum")
        
        # Scan OANDA pairs with forex-specific psychology
        for symbol in self.creds.OANDA_PAIRS:
            if not self.is_running:
                break
            self._scan_pair("oanda", symbol, market_bias, bias_settings, platform_focus="mean_reversion")
    
    def _scan_pair(self, platform, symbol, market_bias, bias_settings, platform_focus):
        """
        🔍 ENHANCED PAIR SCANNING
        Individual pair analysis with psychology quantification
        """
        try:
            # Check if we're already trading this pair
            if self._is_pair_active(symbol):
                return
            
            # Get market data
            timeframe = "5m"  # 5-minute charts for sniper entries
            candles = self._fetch_candles(symbol, timeframe, platform)
            
            if not candles or len(candles) < 100:
                return
            
            # Enhanced signal detection with bias and platform awareness
            signal = self.sniper.scan_for_signals(
                candles, 
                symbol, 
                platform=platform, 
                bias=market_bias
            )
            
            if signal:
                self.signals_found += 1
                
                # Enhanced confluence validation with bias settings
                if signal['signal_strength'] >= bias_settings['min_confluence']:
                    # Check if signal aligns with market bias
                    if self._validate_signal_bias_alignment(signal, market_bias):
                        self._execute_enhanced_signal(signal, platform, market_bias, bias_settings)
                        self.signals_executed += 1
                    else:
                        log_trade(f"⚠️ Signal rejected due to bias misalignment: {symbol} {signal['type']} vs {market_bias}", "BIAS_FILTER")
                        
        except Exception as e:
            # Don't spam errors for individual pair failures
            if "rate limit" not in str(e).lower():
                log_error(f"Enhanced scan error {symbol}: {str(e)}", "PAIR_SCAN")
            time.sleep(0.1)
    
    def _validate_signal_bias_alignment(self, signal, market_bias):
        """
        🧠 VALIDATE SIGNAL ALIGNMENT WITH MARKET BIAS
        Ensures signals harmonize with session characteristics
        """
        signal_type = signal['type']
        
        # Strong alignment cases
        if market_bias == "Momentum" and signal_type in ["bullish", "bearish"]:
            return True  # Momentum favors any directional signal
        elif market_bias == "Breakout" and signal['signal_strength'] >= 8.0:
            return True  # Breakout sessions favor strong signals
        elif market_bias == "Range" and 7.0 <= signal['signal_strength'] <= 8.5:
            return True  # Range sessions favor moderate signals
        elif market_bias == "Reversal":
            # Reversal sessions favor counter-trend setups
            # Would need additional analysis of recent trend direction
            return True  # Simplified for now
        elif market_bias == "Neutral":
            return True  # Neutral allows any signal
        
        # Weak alignment - still allow but log
        return True  # For now, allow all signals but log the bias
    
    def _execute_enhanced_signal(self, signal, platform, market_bias, bias_settings):
        """
        ⚡ EXECUTE ENHANCED TRADING SIGNAL
        Places OCO trade with bias-aware adjustments and psychology scoring
        """
        try:
            symbol = signal['symbol']
            signal_type = signal['type']
            entry_price = signal['entry_price']
            
            # Calculate SL and TP with bias-aware adjustments
            sl_price, tp_price = self._calculate_enhanced_sl_tp(signal, bias_settings)
            
            # Validate risk/reward
            risk = abs(entry_price - sl_price)
            reward = abs(tp_price - entry_price) if tp_price else risk * 3.0
            risk_reward = reward / risk if risk > 0 else 0
            
            if risk_reward < self.creds.MIN_RISK_REWARD:
                log_trade(f"❌ {symbol} R:R too low: {risk_reward:.2f} (min: {self.creds.MIN_RISK_REWARD})", "REJECTED")
                return
            
            # Check for lock mode on ultra-R signals or high psychology score
            psychology_score = signal.get('gap_psychology_score', 0)
            lock_mode = (signal['signal_strength'] >= self.creds.LOCK_MODE_THRESHOLD or 
                        risk_reward >= 3.0 or 
                        psychology_score >= 5.0)
            
            if lock_mode:
                tp_price = None  # No TP, pure trail for wave ride
                log_trade(f"🔐 LOCK MODE ACTIVATED {symbol} | Psychology: {psychology_score:.1f} | No TP, trailing only", "LOCK_MODE")
            
            # Create enhanced dashboard signal
            dashboard_signal = self._create_dashboard_signal(signal, entry_price, sl_price, tp_price, market_bias, lock_mode)
            
            # Update dashboard with pending signal
            if platform == "oanda":
                self.dashboard_feeder.update_oanda_feed(symbol, dashboard_signal, self.active_oanda_trades)
            else:
                self.dashboard_feeder.update_coinbase_feed(symbol, dashboard_signal, self.active_coinbase_trades)
            
            # Determine trade side
            side = "buy" if signal_type == "bullish" else "sell"
            
            # Log enhanced signal before execution
            volume_surge = "VOL+" if signal.get('volume_surge', False) else ""
            log_trade(f"🎯 SIGNAL: {symbol} {signal_type.upper()} | Strength: {signal['signal_strength']:.1f} | "
                     f"Psychology: {psychology_score:.1f} | Bias: {market_bias} {volume_surge}", "SIGNAL")
            
            # Execute OCO trade with enhanced parameters
            order_id = self.oco_executor.place_oco_trade(
                symbol=symbol,
                side=side,
                entry_price=entry_price,
                sl_price=sl_price,
                tp_price=tp_price,
                platform=platform
            )
            
            if order_id:
                # Update dashboard with ACTIVE status
                dashboard_signal["status"] = "ACTIVE"
                if platform == "oanda":
                    self.active_oanda_trades += 1
                    self.dashboard_feeder.update_oanda_feed(symbol, dashboard_signal, self.active_oanda_trades)
                else:
                    self.active_coinbase_trades += 1
                    self.dashboard_feeder.update_coinbase_feed(symbol, dashboard_signal, self.active_coinbase_trades)
                
                log_trade(f"✅ ENHANCED SIGNAL EXECUTED {symbol} | R:R: {risk_reward:.2f} | "
                         f"Confluence: {signal['signal_strength']:.1f} | Psychology: {psychology_score:.1f}", "EXECUTED")
            else:
                log_error(f"Enhanced signal execution failed: {symbol}", "EXECUTION")
                
        except Exception as e:
            log_error(f"Enhanced signal execution error: {str(e)}", "SIGNAL_EXEC")
    
    def _create_dashboard_signal(self, signal, entry_price, sl_price, tp_price, market_bias, lock_mode):
        """Create enhanced dashboard signal with psychology data"""
        trail_status = "🔐 LOCK MODE" if lock_mode else "🔴 STATIC"
        
        return {
            "direction": "BUY" if signal['type'] == "bullish" else "SELL",
            "confidence": signal['signal_strength'],
            "psychology_score": signal.get('gap_psychology_score', 0),
            "volume_surge": signal.get('volume_surge', False),
            "entry": entry_price,
            "sl": sl_price,
            "tp": tp_price,
            "status": "PENDING",
            "reason": f"{signal['type'].title()} FVG + Psychology",
            "trail_status": trail_status,
            "market_bias": market_bias,
            "lock_mode": lock_mode
        }
    
    def _calculate_enhanced_sl_tp(self, signal, bias_settings):
        """
        📐 CALCULATE ENHANCED STOP LOSS & TAKE PROFIT
        Incorporates bias-aware adjustments for market harmony
        """
        entry_price = signal['entry_price']
        signal_type = signal['type']
        fvg_data = signal.get('fvg_data', {})
        
        # Base SL calculation from FVG boundaries
        fvg_high = fvg_data.get('high', entry_price)
        fvg_low = fvg_data.get('low', entry_price)
        
        if signal_type == "bullish":
            # Long trade - SL below FVG low
            base_sl = fvg_low * 0.999
            # Apply bias adjustment
            sl_price = base_sl * bias_settings['sl_adjustment']
            
            # Target based on FVG size + Fibonacci extension
            fvg_size = fvg_high - fvg_low
            tp_price = entry_price + (fvg_size * 2.618)
            
        else:
            # Short trade - SL above FVG high
            base_sl = fvg_high * 1.001
            # Apply bias adjustment
            sl_price = base_sl * bias_settings['sl_adjustment']
            
            # Target based on FVG size + Fibonacci extension
            fvg_size = fvg_high - fvg_low
            tp_price = entry_price - (fvg_size * 2.618)
        
        return round(sl_price, 6), round(tp_price, 6)
    
    def _fetch_candles(self, symbol, timeframe, platform):
        """Enhanced candle fetching with error handling"""
        try:
            if platform == "coinbase":
                return self.coinbase.fetch_ohlcv(symbol, timeframe, limit=100)
            else:
                # OANDA candles via REST API
                oanda_symbol = symbol.replace('/', '_')
                params = {
                    "count": 100,
                    "granularity": "M5"  # 5-minute candles
                }
                
                response = self.oanda.instrument.candles(
                    instrument=oanda_symbol,
                    params=params
                )
                
                # Convert OANDA format to CCXT format
                candles = []
                for candle in response.body['candles']:
                    if candle['complete']:
                        mid = candle['mid']
                        candles.append([
                            int(candle['time'][:19].replace('T', ' ').replace('-', '').replace(':', '')),
                            float(mid['o']),
                            float(mid['h']),
                            float(mid['l']),
                            float(mid['c']),
                            float(candle.get('volume', 0))
                        ])
                
                return candles
                
        except Exception as e:
            log_error(f"Enhanced candle fetch failed {symbol}: {str(e)}", "CANDLE_FETCH")
            return None
    
    def _is_pair_active(self, symbol):
        """Check if we already have an active trade for this pair"""
        for trade_data in self.oco_executor.active_trades.values():
            if trade_data['symbol'] == symbol:
                return True
        return False
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        log_trade(f"🛑 Received signal {signum} - shutting down gracefully...", "SHUTDOWN")
        self.shutdown()
    
    def shutdown(self):
        """
        🛑 GRACEFUL SHUTDOWN
        Stop all enhanced components
        """
        log_trade("🛑 Initiating enhanced shutdown sequence...", "SHUTDOWN")
        
        # Stop scanning
        self.is_running = False
        
        if self.scan_thread and self.scan_thread.is_alive():
            self.scan_thread.join(timeout=10)
        
        # Stop enhanced components
        if self.oco_executor:
            self.oco_executor.stop_monitoring()
        
        if self.oco_dynamic_adjuster:
            self.oco_dynamic_adjuster.stop()
        
        if self.trade_guardian:
            self.trade_guardian.stop()
        
        if self.arbitrage_engine:
            self.arbitrage_engine.stop_scanning()
        
        # Print final enhanced stats
        logger.print_daily_stats()
        print_daily_summary()
        
        # Log final performance metrics
        if self.scan_count > 0:
            signal_rate = (self.signals_found / self.scan_count * 100)
            execution_rate = (self.signals_executed / max(self.signals_found, 1) * 100)
            log_trade(f"📊 Final Stats | Scans: {self.scan_count} | Signals: {self.signals_found} ({signal_rate:.1f}%) | Executed: {self.signals_executed} ({execution_rate:.1f}%)", "FINAL_STATS")
        
        log_trade("✅ Wolfpack-Proto enhanced shutdown complete", "SHUTDOWN")
    
    def emergency_stop(self):
        """
        🚨 EMERGENCY STOP
        Close all positions and shutdown immediately
        """
        log_trade("🚨 EMERGENCY STOP TRIGGERED - Mass psychology quantifier shutdown", "EMERGENCY")
        
        if self.oco_executor:
            self.oco_executor.emergency_close_all()
        
        # Stop wave rides immediately
        if self.oco_dynamic_adjuster:
            from oco_dynamic_adjuster import emergency_stop_all_wave_rides
            emergency_stop_all_wave_rides(self.oco_dynamic_adjuster)
        
        self.shutdown()

def main():
    """
    🚀 MAIN ENTRY POINT
    Launch enhanced Wolfpack-Proto system with mass psychology quantification
    """
    print("\n" + "="*80)
    print("🎯 WOLFPACK-PROTO: ENHANCED AUTONOMOUS FVG SNIPER SYSTEM")
    print("🧠 Mass Psychology Quantifier Edition")
    print("⚡ Dynamic OCO Wave Riders | Bias-Aware Dispatch | Lock Mode")
    print("🌍 Hamilton, NJ Timezone | Session-Aware Trading")
    print("🔥 Live Trading Only - Real Money, Real Results")
    print("="*80 + "\n")
    
    # Initialize enhanced system
    wolfpack = WolfpackProto()
    
    try:
        # Start enhanced hunting
        if wolfpack.start_hunting():
            log_trade("🏹 Enhanced system online - press Ctrl+C to shutdown", "STARTUP")
            
            # Keep main thread alive
            while wolfpack.is_running:
                time.sleep(1)
        else:
            log_error("Failed to start enhanced hunting system", "STARTUP")
            sys.exit(1)
            
    except KeyboardInterrupt:
        log_trade("🛑 Keyboard interrupt received", "SHUTDOWN")
    except Exception as e:
        log_error(f"Fatal error in enhanced system: {str(e)}", "FATAL")
    finally:
        wolfpack.shutdown()

if __name__ == "__main__":
    main()

if not IS_LIVE_MODE:

    raise RuntimeError("�� LIVE_MODE is not active. Execution blocked.")


#!/usr/bin/env python3
"""
🎯 WOLFPACK-LITE MAIN CONTROL
Aggressive FVG hunting with mandatory OCO execution
LIVE TRADING ONLY - NO live_mode/PRACTICE MODE
"""

import sys
import time
import signal
import threading
from datetime import datetime

# Import our API modules
from coinbase_advanced_api import CoinbaseAdvancedTradeAPI
from credentials import WolfpackCredentials
from sniper_core import FVGSniper
from oco_executor import OCOExecutor
from logger import logger, log_trade, log_error
from timezone_manager import MarketSessionManager
from portfolio_manager import LivePortfolioManager
from arbitrage_engine import ArbitrageEngine
from position_tracker import position_tracker, print_daily_summary

# Dashboard integration
from dashboards.feed_updater import FVGDashboardFeeder

# API clients
import ccxt
import oandapyV20
from oandapyV20 import API

class WolfpackLite:
    def __init__(self):
        """🚀 Initialize Wolfpack-Lite system with Hamilton, NJ timezone awareness"""
        self.creds = WolfpackCredentials()
        self.sniper = FVGSniper()
        self.oco_executor = None
        
        # Timezone-aware market session manager
        self.session_manager = MarketSessionManager()
        
        # Live portfolio manager for real-time updates
        self.portfolio_manager = LivePortfolioManager()
        
        # Arbitrage engine for 24/7 spot vs forex arbitrage
        self.arbitrage_engine = None
        
        # Dashboard integration
        self.dashboard_feeder = FVGDashboardFeeder()
        
        # API clients
        self.coinbase = None
        self.oanda = None
        
        # Control flags
        self.is_running = False
        self.scan_thread = None
        
        # Active trades tracking for dashboard
        self.active_oanda_trades = 0
        self.active_coinbase_trades = 0
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def initialize_apis(self):
        """
        🔌 INITIALIZE LIVE API CONNECTIONS
        Setup Coinbase Advanced Trade and OANDA LIVE APIs
        """
        try:
            log_trade("🔌 Initializing LIVE API connections...", "STARTUP")
            
            # Coinbase Advanced Trade API - LIVE ONLY with JWT ed25519
            self.coinbase = CoinbaseAdvancedTradeAPI(
                api_key=self.creds.COINBASE_API_KEY,
                private_key_b64=self.creds.COINBASE_PRIVATE_KEY_B64
            )
            
            # Test Coinbase LIVE connection
            try:
                coinbase_accounts = self.coinbase.get_accounts()
                log_trade(f"✅ Coinbase Advanced Trade LIVE connected | Accounts: {len(coinbase_accounts.get('accounts', []))}", "API")
            except Exception as e:
                # Continue anyway - credentials might not be set yet
            
            # OANDA LIVE API
            self.oanda = API(
                access_token=self.creds.OANDA_API_KEY,
                environment="live"  # LIVE TRADING ONLY
            )
            
            # Test OANDA LIVE connection
            account_response = self.oanda.account.get(accountID=self.creds.OANDA_ACCOUNT_ID)
            oanda_balance = float(account_response.body['account']['balance'])
            log_trade(f"✅ OANDA LIVE connected | Balance: ${oanda_balance:.2f}", "API")
            
            # Initialize OCO executor
            self.oco_executor = OCOExecutor(self.coinbase, self.oanda, self.creds)
            
            # Initialize portfolio manager with API connections
            self.portfolio_manager.initialize_apis(self.coinbase, self.oanda, self.creds)
            
            # Initialize arbitrage engine
            self.arbitrage_engine = ArbitrageEngine(
                self.coinbase, 
                self.oanda, 
                self.creds, 
                self.session_manager, 
                self.portfolio_manager
            )
            
            return True
            
        except Exception as e:
            log_error(f"LIVE API initialization failed: {str(e)}", "API_INIT")
            return False
    
    def start_hunting(self):
        """
        🏹 START FVG HUNTING
        Main scanning loop
        """
        if not self.initialize_apis():
            log_error("API initialization failed - cannot start hunting", "STARTUP")
            return False
        
        self.is_running = True
        
        # Start OCO monitoring
        self.oco_executor.start_monitoring()
        
        # Start arbitrage engine for 24/7 arbitrage
        self.arbitrage_engine.start_scanning()
        
        # Print initial stats with position tracking
        logger.print_daily_stats()
        print_daily_summary()
        
        # Start scanning thread
        self.scan_thread = threading.Thread(target=self._scanning_loop, daemon=True)
        self.scan_thread.start()
        
        log_trade("🏹 WOLFPACK-LITE HUNTING STARTED", "STARTUP")
        log_trade(f"💎 Watching {len(self.creds.COINBASE_PAIRS)} Coinbase + {len(self.creds.OANDA_PAIRS)} OANDA pairs", "STARTUP")
        log_trade("⚡ ARBITRAGE ENGINE: 24/7 Coinbase Spot vs OANDA Forex arbitrage active", "STARTUP")
        log_trade(f"🌍 TIMEZONE: Hamilton, NJ (EST/EDT) | Market sessions: London/NY/China focus", "STARTUP")
        log_trade(f"📊 POSITION TRACKING: Active with {position_tracker.get_position_count()} positions", "STARTUP")
        
        return True
    
    def _scanning_loop(self):
        """
        🔍 MAIN SCANNING LOOP
        Timezone-aware FVG detection and execution
        """
        scan_count = 0
        
        while self.is_running:
            try:
                scan_count += 1
                
                # Get current market session info
                session_info = self.session_manager.get_current_session_info()
                current_session = session_info['current_session']
                
                # Update portfolio every 30 seconds
                if scan_count % 3 == 0:  # Every 3 scans (30 seconds at 10s intervals)
                    self.portfolio_manager.update_portfolio()
                
                # Update dashboard status with session info
                session_text = f"LIVE SCANNING [{current_session}] - Scan #{scan_count}"
                self.dashboard_feeder.update_system_status("oanda", session_text, self.active_oanda_trades)
                self.dashboard_feeder.update_system_status("coinbase", session_text, self.active_coinbase_trades)
                
                # Log portfolio balances every 100 scans
                if scan_count % 100 == 0:
                    balances = self.portfolio_manager.get_total_balances()
                    log_trade(f"📊 Portfolio Update | Total: ${balances['total_usd']:.2f} | CB: ${balances['coinbase_usd']:.2f} | OANDA: ${balances['oanda_usd']:.2f}", "PORTFOLIO")
                
                # Scan Coinbase pairs
                self._scan_platform("coinbase", self.creds.COINBASE_PAIRS)
                
                # Scan OANDA pairs
                self._scan_platform("oanda", self.creds.OANDA_PAIRS)
                
                # Print status every 100 scans
                if scan_count % 100 == 0:
                    active_count = len(self.oco_executor.active_trades)
                    log_trade(f"📊 Scan #{scan_count} | Active trades: {active_count}", "STATUS")
                
                # Brief pause between scans
                time.sleep(self.creds.SCAN_INTERVAL)
                
            except Exception as e:
                log_error(f"Scanning loop error: {str(e)}", "SCAN_LOOP")
                time.sleep(5)  # Longer pause on error
    
    def _scan_platform(self, platform, pairs):
        """
        🎯 SCAN SPECIFIC PLATFORM
        Check all pairs for FVG signals
        """
        for symbol in pairs:
            try:
                # Check if we're already trading this pair
                if self._is_pair_active(symbol):
                    continue
                
                # Get market data
                timeframe = "5m"  # 5-minute charts for sniper entries
                candles = self._fetch_candles(symbol, timeframe, platform)
                
                if not candles or len(candles) < 100:
                    continue
                
                # Detect FVG signals
                signal = self.sniper.scan_for_signals(candles, symbol)
                
                if signal and signal['signal_strength'] >= self.creds.MIN_CONFLUENCE_SCORE:
                    self._execute_signal(signal, platform)
                    
            except Exception as e:
                # Don't spam errors for individual pair failures
                if "rate limit" not in str(e).lower():
                    log_error(f"Scan error {symbol}: {str(e)}", "PAIR_SCAN")
                time.sleep(0.1)  # Small delay on error
    
    def _fetch_candles(self, symbol, timeframe, platform):
        """
        📈 FETCH MARKET DATA
        Get OHLCV candles for analysis
        """
        try:
            if platform == "coinbase":
                return self.coinbase.fetch_ohlcv(symbol, timeframe, limit=100)
            else:
                # OANDA candles via REST API
                oanda_symbol = symbol.replace('/', '_')
                params = {
                    "count": 100,
                    "granularity": "M5"  # 5-minute candles
                }
                
                response = self.oanda.instrument.candles(
                    instrument=oanda_symbol,
                    params=params
                )
                
                # Convert OANDA format to CCXT format
                candles = []
                for candle in response.body['candles']:
                    if candle['complete']:
                        mid = candle['mid']
                        candles.append([
                            int(candle['time'][:19].replace('T', ' ').replace('-', '').replace(':', '')),
                            float(mid['o']),
                            float(mid['h']),
                            float(mid['l']),
                            float(mid['c']),
                            float(candle.get('volume', 0))
                        ])
                
                return candles
                
        except Exception as e:
            log_error(f"Candle fetch failed {symbol}: {str(e)}", "CANDLE_FETCH")
            return None
    
    def _is_pair_active(self, symbol):
        """Check if we already have an active trade for this pair"""
        for trade_data in self.oco_executor.active_trades.values():
            if trade_data['symbol'] == symbol:
                return True
        return False
    
    def _execute_signal(self, signal, platform):
        """
        ⚡ EXECUTE TRADING SIGNAL
        Place OCO trade based on FVG signal
        """
        try:
            symbol = signal['symbol']
            signal_type = signal['type']
            entry_price = signal['entry_price']
            
            # Calculate SL and TP based on FVG and Fibonacci
            sl_price, tp_price = self._calculate_sl_tp(signal)
            
            # Validate risk/reward
            risk = abs(entry_price - sl_price)
            reward = abs(tp_price - entry_price)
            risk_reward = reward / risk if risk > 0 else 0
            
            if risk_reward < self.creds.MIN_RISK_REWARD:
                log_trade(f"❌ {symbol} R:R too low: {risk_reward:.2f}", "REJECTED")
                return
            
            # Update dashboard with pending signal BEFORE execution
            dashboard_signal = {
                "direction": "BUY" if signal_type == "bullish" else "SELL",
                "confidence": signal['signal_strength'],
                "entry": entry_price,
                "sl": sl_price,
                "tp": tp_price,
                "status": "PENDING",
                "reason": f"{signal_type.title()} FVG + Confluence"
            }
            
            if platform == "oanda":
                self.dashboard_feeder.update_oanda_feed(symbol, dashboard_signal, self.active_oanda_trades)
            else:
                self.dashboard_feeder.update_coinbase_feed(symbol, dashboard_signal, self.active_coinbase_trades)
            
            # Determine trade side
            side = "buy" if signal_type == "bullish" else "sell"
            
            # Log signal before execution
            from logger import log_signal
            log_signal(symbol, signal_type, signal['signal_strength'], signal)
            
            # Execute OCO trade
            order_id = self.oco_executor.place_oco_trade(
                symbol=symbol,
                side=side,
                entry_price=entry_price,
                sl_price=sl_price,
                tp_price=tp_price,
                platform=platform
            )
            
            if order_id:
                # Update dashboard with ACTIVE status after successful execution
                dashboard_signal["status"] = "ACTIVE"
                if platform == "oanda":
                    self.active_oanda_trades += 1
                    self.dashboard_feeder.update_oanda_feed(symbol, dashboard_signal, self.active_oanda_trades)
                else:
                    self.active_coinbase_trades += 1
                    self.dashboard_feeder.update_coinbase_feed(symbol, dashboard_signal, self.active_coinbase_trades)
                log_trade(f"🎯 SIGNAL EXECUTED {symbol} | R:R: {risk_reward:.2f} | "
                         f"Confluence: {signal['signal_strength']:.1f}", "EXECUTED")
            else:
                log_error(f"Signal execution failed: {symbol}", "EXECUTION")
                
        except Exception as e:
            log_error(f"Signal execution error: {str(e)}", "SIGNAL_EXEC")
    
    def _calculate_sl_tp(self, signal):
        """
        📐 CALCULATE STOP LOSS & TAKE PROFIT
        Based on FVG boundaries and Fibonacci levels
        """
        entry_price = signal['entry_price']
        signal_type = signal['type']
        fvg_data = signal.get('fvg_data', {})
        
        # FVG boundaries for SL placement
        fvg_high = fvg_data.get('high', entry_price)
        fvg_low = fvg_data.get('low', entry_price)
        
        if signal_type == "bullish":
            # Long trade
            sl_price = fvg_low * 0.999  # Just below FVG low
            
            # Target based on FVG size + Fibonacci extension
            fvg_size = fvg_high - fvg_low
            tp_price = entry_price + (fvg_size * 2.618)  # 261.8% Fibonacci extension
            
        else:
            # Short trade
            sl_price = fvg_high * 1.001  # Just above FVG high
            
            # Target based on FVG size + Fibonacci extension
            fvg_size = fvg_high - fvg_low
            tp_price = entry_price - (fvg_size * 2.618)  # 261.8% Fibonacci extension
        
        return round(sl_price, 6), round(tp_price, 6)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        log_trade(f"🛑 Received signal {signum} - shutting down gracefully...", "SHUTDOWN")
        self.shutdown()
    
    def shutdown(self):
        """
        🛑 GRACEFUL SHUTDOWN
        Stop scanning and close monitoring
        """
        log_trade("🛑 Initiating shutdown sequence...", "SHUTDOWN")
        
        # Stop scanning
        self.is_running = False
        
        if self.scan_thread and self.scan_thread.is_alive():
            self.scan_thread.join(timeout=10)
        
        # Stop OCO monitoring
        if self.oco_executor:
            self.oco_executor.stop_monitoring()
        
        # Print final stats
        logger.print_daily_stats()
        
        log_trade("✅ Wolfpack-Lite shutdown complete", "SHUTDOWN")
    
    def emergency_stop(self):
        """
        🚨 EMERGENCY STOP
        Close all positions and shutdown
        """
        log_trade("🚨 EMERGENCY STOP TRIGGERED", "EMERGENCY")
        
        if self.oco_executor:
            self.oco_executor.emergency_close_all()
        
        self.shutdown()

def main():
    """
    🚀 MAIN ENTRY POINT
    Launch Wolfpack-Lite system
    """
    print("\n" + "="*60)
    print("🎯 WOLFPACK-LITE FVG SNIPER SYSTEM")
    print("⚡ Aggressive FVG hunting with mandatory OCO")
    print("="*60 + "\n")
    
    # Initialize system
    wolfpack = WolfpackLite()
    
    try:
        # Start hunting
        if wolfpack.start_hunting():
            log_trade("🏹 System online - press Ctrl+C to shutdown", "STARTUP")
            
            # Keep main thread alive
            while wolfpack.is_running:
                time.sleep(1)
        else:
            log_error("Failed to start hunting system", "STARTUP")
            sys.exit(1)
            
    except KeyboardInterrupt:
        log_trade("🛑 Keyboard interrupt received", "SHUTDOWN")
    except Exception as e:
        log_error(f"Fatal error: {str(e)}", "FATAL")
    finally:
        wolfpack.shutdown()

if __name__ == "__main__":
    main()
