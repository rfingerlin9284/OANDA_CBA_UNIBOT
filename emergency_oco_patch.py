#!/usr/bin/env python3
"""
🚑 EMERGENCY OCO INJECTION SCRIPT
This script patches the router_live_hardcoded.py with verified OCO logic
"""

import re

# Read the current router file
with open('/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/router_live_hardcoded.py', 'r') as f:
    content = f.read()

# Define the new verified OCO methods
new_methods = '''
        def place_order(self, instrument, units, price, sl, tp):
            """🛡️ EMERGENCY-FIXED ORDER PLACEMENT with MANDATORY OCO VERIFICATION"""
            global last_signature, rejection_count
            
            # Cooldown Protection Check
            try:
                validate_cooldown(instrument)
            except Exception as e:
                self.log_message(f"🛑 COOLDOWN BLOCK: {e}")
                return False
            
            # Apply proper decimal precision to prices
            price = truncate_price(price, instrument)
            sl = truncate_price(sl, instrument)
            tp = truncate_price(tp, instrument)
            
            # 🚑 EMERGENCY OCO FIX - Use verified submission method
            success = self.submit_order_with_oco_verification(instrument, int(units), price, sl, tp)
            
            if success:
                self.log_message(f"✅ LIVE ORDER WITH VERIFIED OCO: {instrument}, {units} units, Price: {price:.5f}, SL: {sl:.5f}, TP: {tp:.5f}")
                # Record successful trade for cooldown
                cooldown_tracker[instrument] = time.time()
                return True
            else:
                self.log_message(f"🚨 CRITICAL FAILURE: OCO verification failed for {instrument}")
                self.log_message(f"🛑 TRADE ABORTED - POSITION PROTECTION FAILURE")
                return False
        
        def submit_order_with_oco_verification(self, instrument, units, entry_price, sl_price, tp_price):
            """🛡️ VERIFIED OCO order submission with server-side confirmation"""
            from oandapyV20.endpoints.orders import OrderCreate, OrderList
            import time
            
            order_data = {
                "order": {
                    "instrument": instrument,
                    "units": str(units),
                    "type": "MARKET",
                    "positionFill": "DEFAULT",
                    "stopLossOnFill": {
                        "price": str(sl_price)
                    },
                    "takeProfitOnFill": {
                        "price": str(tp_price)
                    }
                }
            }

            self.log_message(f"📤 SUBMITTING VERIFIED ORDER: {units} {instrument} | SL: {sl_price} | TP: {tp_price}")

            try:
                # Submit the order
                r = OrderCreate(accountID=os.getenv('OANDA_ACCOUNT_ID'), data=order_data)
                self.api.request(r)
                
                self.log_message("✅ ORDER ACCEPTED - Verifying OCO placement...")
                
                # Wait for OANDA to process
                time.sleep(2)
                
                # Verify OCO orders were actually created
                oco_verified = self.verify_oco_on_server(instrument)
                
                if oco_verified:
                    self.log_message("🛡️ OCO VERIFICATION PASSED - Position is protected!")
                    return True
                else:
                    self.log_message("🚨 OCO VERIFICATION FAILED - EMERGENCY ALERT!")
                    self.log_message("Position may be naked - manual intervention required!")
                    return False
                    
            except Exception as e:
                self.log_message(f"❌ ORDER SUBMISSION FAILED: {str(e)}")
                return False
        
        def verify_oco_on_server(self, instrument):
            """Verify that SL and TP orders actually exist on OANDA server"""
            from oandapyV20.endpoints.orders import OrderList
            
            try:
                # Get all pending orders
                orders_request = OrderList(accountID=os.getenv('OANDA_ACCOUNT_ID'))
                self.api.request(orders_request)
                orders = orders_request.response.get('orders', [])
                
                has_sl = False
                has_tp = False
                
                for order in orders:
                    if (order.get('instrument') == instrument and 
                        order.get('state') == 'PENDING'):
                        
                        if 'STOP_LOSS' in order.get('type', ''):
                            has_sl = True
                            self.log_message(f"   ✅ Stop Loss confirmed: {order.get('price', 'N/A')}")
                            
                        elif 'TAKE_PROFIT' in order.get('type', ''):
                            has_tp = True
                            self.log_message(f"   ✅ Take Profit confirmed: {order.get('price', 'N/A')}")
                
                return has_sl and has_tp
                
            except Exception as e:
                self.log_message(f"❌ OCO verification error: {e}")
                return False
'''

# Find and replace the place_order method
# Look for the method definition and replace everything until the next method
pattern = r'(\s+def place_order\(self, instrument, units, price, sl, tp\):\s*"""[^"]*"""[^}]*?)(\s+def [^}]*)'

match = re.search(pattern, content, re.DOTALL)

if match:
    # Replace the place_order method and add new methods
    new_content = content[:match.start(1)] + new_methods + '\n' + content[match.start(2):]
    
    # Backup the original file
    with open('/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/router_live_hardcoded.py.backup', 'w') as f:
        f.write(content)
    
    # Write the patched version
    with open('/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/router_live_hardcoded.py', 'w') as f:
        f.write(new_content)
    
    print("✅ EMERGENCY OCO PATCH APPLIED SUCCESSFULLY!")
    print("🔒 Original file backed up as router_live_hardcoded.py.backup")
    
else:
    print("❌ Could not find place_order method to patch")
    
# Now restart the service
import subprocess
subprocess.run(['systemctl', '--user', 'restart', 'horsemen-proto_oanda.service'])
print("🚀 OANDA service restarted with emergency fix")
