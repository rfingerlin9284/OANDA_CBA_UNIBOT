#!/usr/bin/env python3
"""
NUCLEAR ORDER EXECUTION TRACER
Traces every single step of order execution to find the failure point
"""
import json
import requests
import datetime

# HARD CODED OANDA CREDENTIALS
TOKEN = "9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3"
ACCOUNT_ID = "001-001-13473069-001"
BASE_URL = "https://api-fxtrade.oanda.com"

def trace_log(msg):
    """Enhanced tracing with timestamps"""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] 🔍 {msg}")

def test_connectivity():
    """Test basic OANDA connectivity"""
    trace_log("Testing OANDA API connectivity...")
    try:
        url = f"{BASE_URL}/v3/accounts/{ACCOUNT_ID}"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        
        trace_log(f"GET {url}")
        response = requests.get(url, headers=headers)
        
        trace_log(f"Response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            balance = data['account']['balance']
            trace_log(f"✅ Connected! Account balance: ${balance}")
            return True
        else:
            trace_log(f"❌ Connection failed: {response.text}")
            return False
    except Exception as e:
        trace_log(f"❌ Connection error: {e}")
        return False

def test_market_order():
    """Test a minimal market order (1 unit EUR/USD)"""
    trace_log("Testing MINIMAL market order execution...")
    
    order_payload = {
        "order": {
            "type": "MARKET",
            "instrument": "EUR_USD", 
            "units": "1"  # Smallest possible order
        }
    }
    
    trace_log(f"Order payload: {json.dumps(order_payload, indent=2)}")
    
    try:
        url = f"{BASE_URL}/v3/accounts/{ACCOUNT_ID}/orders"
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        
        trace_log(f"POST {url}")
        trace_log(f"Headers: {headers}")
        
        response = requests.post(url, headers=headers, json=order_payload)
        
        trace_log(f"Response status: {response.status_code}")
        trace_log(f"Response headers: {dict(response.headers)}")
        trace_log(f"Response body: {response.text}")
        
        if response.status_code == 201:
            order_data = response.json()
            if 'orderFillTransaction' in order_data:
                order_id = order_data['orderFillTransaction']['id']
                trace_log(f"🎯 ORDER EXECUTED! ID: {order_id}")
                return order_id
            else:
                trace_log(f"⚠️ Order created but no fill transaction: {order_data}")
                return None
        else:
            trace_log(f"❌ Order FAILED: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        trace_log(f"❌ Order execution EXCEPTION: {e}")
        return None

def test_order_with_stops():
    """Test order with TP/SL (like your bot does)"""
    trace_log("Testing order with TP/SL stops...")
    
    # Get current price first
    try:
        url = f"{BASE_URL}/v3/pricing"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        params = {"instruments": "EUR_USD"}
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            price_data = response.json()
            current_price = float(price_data['prices'][0]['asks'][0]['price'])
            trace_log(f"Current EUR/USD price: {current_price}")
            
            # Calculate TP/SL levels
            tp_price = round(current_price + 0.0050, 5)  # 50 pips profit
            sl_price = round(current_price - 0.0025, 5)  # 25 pips loss
            
            order_payload = {
                "order": {
                    "type": "MARKET",
                    "instrument": "EUR_USD",
                    "units": "1000",  # 1000 units
                    "takeProfitOnFill": {"price": str(tp_price)},
                    "stopLossOnFill": {"price": str(sl_price)}
                }
            }
            
            trace_log(f"TP/SL Order payload: {json.dumps(order_payload, indent=2)}")
            
            url = f"{BASE_URL}/v3/accounts/{ACCOUNT_ID}/orders"
            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, headers=headers, json=order_payload)
            
            trace_log(f"TP/SL Response: {response.status_code}")
            trace_log(f"TP/SL Body: {response.text}")
            
            if response.status_code == 201:
                order_data = response.json()
                if 'orderFillTransaction' in order_data:
                    order_id = order_data['orderFillTransaction']['id']
                    trace_log(f"🎯 TP/SL ORDER EXECUTED! ID: {order_id}")
                    return order_id
                else:
                    trace_log(f"⚠️ TP/SL Order created but no fill: {order_data}")
            else:
                trace_log(f"❌ TP/SL Order FAILED: {response.text}")
                
    except Exception as e:
        trace_log(f"❌ TP/SL Order EXCEPTION: {e}")
    
    return None

def check_account_status():
    """Check if account has any restrictions"""
    trace_log("Checking account status and restrictions...")
    
    try:
        url = f"{BASE_URL}/v3/accounts/{ACCOUNT_ID}"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            account = response.json()['account']
            
            trace_log(f"Account ID: {account['id']}")
            trace_log(f"Balance: ${account['balance']}")
            trace_log(f"NAV: ${account['NAV']}")
            trace_log(f"Margin Used: ${account['marginUsed']}")
            trace_log(f"Margin Available: ${account['marginAvailable']}")
            trace_log(f"Open Trade Count: {account['openTradeCount']}")
            trace_log(f"Open Position Count: {account['openPositionCount']}")
            trace_log(f"Pending Order Count: {account['pendingOrderCount']}")
            
            if float(account['marginAvailable']) < 100:
                trace_log("⚠️ WARNING: Low margin available!")
            
            return True
    except Exception as e:
        trace_log(f"❌ Account status error: {e}")
    
    return False

def list_current_positions():
    """List any current positions"""
    trace_log("Checking current positions...")
    
    try:
        url = f"{BASE_URL}/v3/accounts/{ACCOUNT_ID}/positions"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            positions = response.json()['positions']
            
            if positions:
                for pos in positions:
                    if float(pos['long']['units']) != 0 or float(pos['short']['units']) != 0:
                        trace_log(f"Position: {pos['instrument']} | Long: {pos['long']['units']} | Short: {pos['short']['units']}")
            else:
                trace_log("No open positions found")
            
            return positions
    except Exception as e:
        trace_log(f"❌ Position check error: {e}")
    
    return []

def list_pending_orders():
    """List any pending orders"""
    trace_log("Checking pending orders...")
    
    try:
        url = f"{BASE_URL}/v3/accounts/{ACCOUNT_ID}/orders"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            orders = response.json()['orders']
            
            if orders:
                for order in orders:
                    trace_log(f"Pending Order: {order['id']} | {order['instrument']} | {order['units']} | {order['type']}")
            else:
                trace_log("No pending orders found")
            
            return orders
    except Exception as e:
        trace_log(f"❌ Order check error: {e}")
    
    return []

def main():
    """Run complete order execution diagnostics"""
    print("🚀 NUCLEAR ORDER EXECUTION TRACER STARTING")
    print("=" * 60)
    
    # Step 1: Test connectivity
    if not test_connectivity():
        print("❌ FAILED: Cannot connect to OANDA API")
        return
    
    # Step 2: Check account status
    check_account_status()
    
    # Step 3: List current state
    list_current_positions()
    list_pending_orders()
    
    print("\n" + "=" * 60)
    print("🧪 TESTING ORDER EXECUTION")
    print("=" * 60)
    
    # Step 4: Test minimal order
    order_id = test_market_order()
    if order_id:
        print(f"✅ SUCCESS: Minimal order executed with ID {order_id}")
    else:
        print("❌ FAILED: Cannot execute minimal order")
        return
    
    # Step 5: Test order with stops
    order_id_2 = test_order_with_stops()
    if order_id_2:
        print(f"✅ SUCCESS: TP/SL order executed with ID {order_id_2}")
    else:
        print("⚠️ WARNING: TP/SL order failed (but basic orders work)")
    
    print("\n" + "=" * 60)
    print("✅ DIAGNOSIS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
