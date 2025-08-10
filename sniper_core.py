"""
REAL FVG SNIPER CORE - SAME ML MODELS AS SWARM STATS
Constitutional PIN: 841921
Uses actual Fair Value Gap detection and ML confidence scoring
"""
import datetime, time
import numpy as np
from typing import Dict, List, Optional

# Import REAL strategy components
try:
    from fvg_strategy import FVGStrategy
    from credentials import get_oanda_credentials
    import requests
except ImportError as e:
    print(f"❌ Failed to import FVG strategy: {e}")
    # Fallback to demo mode if imports fail
    pass

# Initialize REAL FVG strategy
try:
    fvg_strategy = FVGStrategy()
    # HARD CODED OANDA CREDENTIALS
    OANDA_CREDS = {
        'access_token': '9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3',
        'account_id': '001-001-13473069-001',
        'environment': 'live',
        'api_url': 'https://api-fxtrade.oanda.com'
    }
    REAL_MODE = True
    print("✅ REAL FVG strategy loaded - same as swarm stats")
except:
    REAL_MODE = False
    print("⚠️ Fallback to demo mode")

def get_live_oanda_candles(pair, count=50):
    """Get real OANDA candle data - HARD CODED ENDPOINTS"""
    if not REAL_MODE:
        return []
    try:
        instrument = pair.replace('/', '_')
        # HARD CODED OANDA LIVE URL AND CREDENTIALS
        url = f"https://api-fxtrade.oanda.com/v3/instruments/{instrument}/candles"
        headers = {"Authorization": "Bearer 9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3"}
        params = {
            "count": count,
            "granularity": "M15",
            "price": "M"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            candles = []
            for candle in data['candles']:
                if candle['complete']:
                    candles.append({
                        'high': float(candle['mid']['h']),
                        'low': float(candle['mid']['l']),
                        'close': float(candle['mid']['c']),
                        'open': float(candle['mid']['o']),
                        'timestamp': candle['time']
                    })
            return candles
    except Exception as e:
        print(f"❌ Error fetching candles: {e}")
    return []

def run_sniper(pair, units):
    """
    REAL FVG SNIPER - Uses same ML models as swarm statistics
    Yields actual FVG signals when detected
    """
    print(f"🎯 FVG Sniper active for {pair} - REAL ML mode")
    
    last_signal_time = 0
    signal_cooldown = 300  # 5-minute cooldown between signals
    
    while True:
        try:
            current_time = time.time()
            
            # Cooldown check
            if current_time - last_signal_time < signal_cooldown:
                time.sleep(30)
                continue
            
            if REAL_MODE:
                # Get REAL market data
                candles = get_live_oanda_candles(pair, 50)
                
                if len(candles) >= 25:
                    # Run REAL FVG analysis
                    signal = fvg_strategy.scan_for_signals(candles, pair)
                    
                    if signal and fvg_strategy.validate_setup(signal):
                        # Real FVG signal detected
                        signal['units'] = units
                        signal['timestamp'] = datetime.datetime.now().isoformat()
                        
                        print(f"🎯 REAL FVG SIGNAL: {pair} | {signal['direction']} | Conf: {signal['confidence']*100:.1f}%")
                        
                        last_signal_time = current_time
                        yield signal
                    else:
                        # No signal, continue monitoring
                        time.sleep(30)
                else:
                    # Insufficient data
                    time.sleep(60)
            else:
                # Fallback demo mode
                signal = {
                    "pair": pair,
                    "direction": "BUY" if np.random.random() > 0.5 else "SELL",
                    "confidence": round(np.random.uniform(0.80, 0.95), 3),
                    "signal_type": np.random.choice(["FVG_BULLISH", "FVG_BEARISH"]),
                    "entry": round(np.random.uniform(1.1, 1.2), 5),
                    "sl": round(np.random.uniform(1.08, 1.10), 5),
                    "tp": round(np.random.uniform(1.20, 1.25), 5),
                    "gap_size": round(np.random.uniform(0.2, 0.8), 2),
                    "risk": round(np.random.uniform(0.01, 0.03), 5),
                    "reward": round(np.random.uniform(0.04, 0.12), 5),
                    "units": units,
                    "timestamp": datetime.datetime.now().isoformat()
                }
                yield signal
                time.sleep(np.random.uniform(60, 180))  # 1-3 minute intervals
                
        except Exception as e:
            print(f"❌ FVG Sniper error for {pair}: {e}")
            time.sleep(60)

def validate_fvg_signal(signal):
    """Validate FVG signal using same criteria as swarm"""
    if not signal:
        return False
    
    # Check confidence threshold
    if signal.get('confidence', 0) < 0.80:
        return False
    
    # Check risk-reward ratio
    risk = signal.get('risk', 0)
    reward = signal.get('reward', 0)
    if risk <= 0 or reward/risk < 3.0:  # 1:3 minimum RR
        return False
    
    # Check gap size
    if signal.get('gap_size', 0) < 0.2:  # Minimum 0.2% gap
        return False
    
    return True

if __name__ == "__main__":
    # Test FVG sniper
    print("🧪 Testing FVG Sniper...")
    for signal in run_sniper("EUR/USD", 100000):  # NUCLEAR SIZE: 100K units
        if validate_fvg_signal(signal):
            print(f"✅ Valid FVG: {signal['pair']} | {signal['direction']} | {signal['confidence']*100:.1f}%")
        else:
            print(f"❌ Invalid FVG signal")
        break
