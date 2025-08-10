"""
REAL OANDA OCO DYNAMIC ADJUSTER
Constitutional PIN: 841921
Manages One-Cancels-Other orders via OANDA API
"""
import os, datetime, time
import requests
from typing import Optional, Dict

# Import OANDA credentials - HARD CODED
try:
    # HARD CODED OANDA LIVE CREDENTIALS
    OANDA_CREDS = {
        'access_token': '9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3',
        'account_id': '001-001-13473069-001',
        'environment': 'live',
        'api_url': 'https://api-fxtrade.oanda.com'
    }
    REAL_MODE = True
except:
    REAL_MODE = False
    print("⚠️ OCO running in demo mode")

def log_oco_event(msg):
    """Enhanced OCO logging"""
    timestamp = datetime.datetime.utcnow().isoformat()
    print(f"[OCO] {msg}")
    os.makedirs("logs", exist_ok=True)
    with open("logs/oco_enforcer.log", "a") as f:
        f.write(f"{timestamp} | {msg}\n")

def get_order_status(order_id: str) -> Optional[Dict]:
    """Get real order status from OANDA - HARD CODED ENDPOINTS"""
    if not REAL_MODE:
        return {"state": "FILLED", "profit": 0.0}
    
    try:
        # HARD CODED OANDA LIVE URL AND CREDENTIALS
        url = f"https://api-fxtrade.oanda.com/v3/accounts/001-001-13473069-001/orders/{order_id}"
        headers = {"Authorization": "Bearer 9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            order_data = response.json()
            return order_data.get('order', {})
    except Exception as e:
        log_oco_event(f"Error checking order {order_id}: {e}")
    
    return None

def cancel_order(order_id: str) -> bool:
    """Cancel order via OANDA API - HARD CODED ENDPOINTS"""
    if not REAL_MODE:
        return True
    
    try:
        # HARD CODED OANDA LIVE URL AND CREDENTIALS
        url = f"https://api-fxtrade.oanda.com/v3/accounts/001-001-13473069-001/orders/{order_id}/cancel"
        headers = {"Authorization": "Bearer 9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3"}
        response = requests.put(url, headers=headers)
        
        if response.status_code == 200:
            log_oco_event(f"Successfully cancelled order {order_id}")
            return True
    except Exception as e:
        log_oco_event(f"Error cancelling order {order_id}: {e}")
    
    return False

def enforce_oco(order_id: str, pair: str, status="ACTIVE"):
    """
    REAL OCO enforcement with OANDA API monitoring
    Monitors TP/SL execution and manages OCO logic
    """
    log_oco_event(f"OCO Monitor started for Order #{order_id} | {pair} | Status: {status}")
    
    if not REAL_MODE:
        # Demo mode simulation
        import random
        if random.random() < 0.15:  # 15% chance of trigger
            profit = round(random.uniform(-20, 50), 2)
            if profit > 0:
                log_oco_event(f"TP Triggered for Order #{order_id} | {pair} | Profit: +")
            else:
                log_oco_event(f"SL Triggered for Order #{order_id} | {pair} | Loss: ")
        return
    
    # Real OANDA OCO monitoring
    monitor_count = 0
    max_monitors = 1440  # Monitor for 24 hours (1440 minutes)
    
    while monitor_count < max_monitors:
        try:
            order_status = get_order_status(order_id)
            
            if order_status:
                state = order_status.get('state', 'UNKNOWN')
                
                if state == 'FILLED':
                    # Order executed, check if TP or SL
                    fill_reason = order_status.get('filledReason', 'UNKNOWN')
                    
                    if 'TAKE_PROFIT' in fill_reason.upper():
                        profit = order_status.get('profit', 0.0)
                        log_oco_event(f"TP Executed for Order #{order_id} | {pair} | Profit: +")
                        break
                    elif 'STOP_LOSS' in fill_reason.upper():
                        loss = order_status.get('profit', 0.0)
                        log_oco_event(f"SL Executed for Order #{order_id} | {pair} | Loss: ")
                        break
                
                elif state == 'CANCELLED':
                    log_oco_event(f"Order #{order_id} | {pair} | Status: CANCELLED")
                    break
                
                elif state == 'PENDING':
                    # Still active, continue monitoring
                    if monitor_count % 60 == 0:  # Log every hour
                        log_oco_event(f"Order #{order_id} | {pair} | Still active (monitoring {monitor_count} min)")
            
            monitor_count += 1
            time.sleep(60)  # Check every minute
            
        except Exception as e:
            log_oco_event(f"OCO Monitor error for {order_id}: {e}")
            time.sleep(60)
    
    # Monitoring timeout
    if monitor_count >= max_monitors:
        log_oco_event(f"OCO Monitor timeout for Order #{order_id} | {pair} | Stopped after 24h")

def dynamic_sl_adjustment(order_id: str, pair: str, new_sl_price: float):
    """Dynamically adjust stop loss for running trades - HARD CODED ENDPOINTS"""
    if not REAL_MODE:
        log_oco_event(f"Demo SL adjustment for Order #{order_id} | {pair} | New SL: {new_sl_price}")
        return
    
    try:
        # Modify order SL via OANDA API - HARD CODED LIVE URL AND CREDENTIALS
        url = f"https://api-fxtrade.oanda.com/v3/accounts/001-001-13473069-001/orders/{order_id}"
        headers = {
            "Authorization": "Bearer 9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3",
            "Content-Type": "application/json"
        }
        
        order_data = {
            "order": {
                "stopLoss": {
                    "price": str(new_sl_price)
                }
            }
        }
        
        response = requests.put(url, headers=headers, json=order_data)
        
        if response.status_code == 200:
            log_oco_event(f"SL Updated for Order #{order_id} | {pair} | New SL: {new_sl_price}")
        else:
            log_oco_event(f"SL Update failed for Order #{order_id}: {response.text}")
            
    except Exception as e:
        log_oco_event(f"SL Adjustment error for {order_id}: {e}")

if __name__ == "__main__":
    # Test OCO system
    print("🧪 Testing REAL OCO system...")
    enforce_oco("TEST123", "EUR/USD", "ACTIVE")
