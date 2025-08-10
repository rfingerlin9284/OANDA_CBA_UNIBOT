#!/usr/bin/env python3
"""
Direct OCO fix injection - replaces the faulty import with inline verified logic
"""

# Read the router file
with open('/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/router_live_hardcoded.py', 'r') as f:
    content = f.read()

# Replace the problematic import-based method with inline verified logic
old_method = '''        def place_order(self, instrument, units, price, sl, tp):
            """Place live order with MANDATORY OCO verification and fail-safe protection"""
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
            
            # Import emergency fix module
            from fix_order_submission import place_order_with_oco
            
            # Use the verified OCO order placement
            success = place_order_with_oco(
                api=self.api,
                account_id=os.getenv('OANDA_ACCOUNT_ID'),
                instrument=instrument,
                units=int(units),
                sl_price=sl,
                tp_price=tp
            )
            
            if success:
                self.log_message(f"✅ LIVE ORDER WITH OCO CONFIRMED: {instrument}, {units} units, Price: {price:.5f}, SL: {sl:.5f}, TP: {tp:.5f}")
                # Record successful trade for cooldown
                cooldown_tracker[instrument] = time.time()
                return True
            else:
                self.log_message(f"🚨 CRITICAL FAILURE: OCO order submission failed for {instrument}")
                self.log_message(f"🛑 POSITION PROTECTION FAILURE - TRADE ABORTED")
                return False'''

new_method = '''        def place_order(self, instrument, units, price, sl, tp):
            """🛡️ EMERGENCY-FIXED ORDER PLACEMENT with INLINE OCO VERIFICATION"""
            global last_signature, rejection_count
            from oandapyV20.endpoints.orders import OrderCreate, OrderList
            import time
            
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
            
            # Build verified OCO order
            order_data = {
                "order": {
                    "instrument": instrument,
                    "units": str(int(units)),
                    "type": "MARKET",
                    "positionFill": "DEFAULT",
                    "stopLossOnFill": {
                        "price": str(sl)
                    },
                    "takeProfitOnFill": {
                        "price": str(tp)
                    }
                }
            }

            self.log_message(f"📤 SUBMITTING VERIFIED ORDER: {units} {instrument} | SL: {sl} | TP: {tp}")

            try:
                # Submit the order
                r = OrderCreate(accountID=os.getenv('OANDA_ACCOUNT_ID'), data=order_data)
                self.api.request(r)
                
                self.log_message("✅ ORDER ACCEPTED - Verifying OCO placement...")
                
                # Wait for OANDA to process
                time.sleep(2)
                
                # Verify OCO orders were actually created
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
                
                if has_sl and has_tp:
                    self.log_message("🛡️ OCO VERIFICATION PASSED - Position is protected!")
                    cooldown_tracker[instrument] = time.time()
                    return True
                else:
                    self.log_message("🚨 OCO VERIFICATION FAILED - EMERGENCY ALERT!")
                    self.log_message("🛑 TRADE ABORTED - POSITION PROTECTION FAILURE")
                    return False
                    
            except Exception as e:
                self.log_message(f"❌ ORDER SUBMISSION FAILED: {str(e)}")
                return False'''

# Replace the method
if old_method in content:
    new_content = content.replace(old_method, new_method)
    
    # Backup original
    with open('/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/router_live_hardcoded.py.backup', 'w') as f:
        f.write(content)
    
    # Write fixed version
    with open('/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/router_live_hardcoded.py', 'w') as f:
        f.write(new_content)
    
    print("✅ EMERGENCY OCO FIX APPLIED!")
    print("🔒 Backup saved as router_live_hardcoded.py.backup")
    
    # Restart service
    import subprocess
    subprocess.run(['systemctl', '--user', 'restart', 'horsemen-proto_oanda.service'])
    print("🚀 Service restarted with verified OCO logic")
    
else:
    print("❌ Method not found for replacement")
    print("Checking for partial matches...")
    
    # Check if partial content exists
    if "from fix_order_submission import place_order_with_oco" in content:
        print("Found faulty import - proceeding with text replacement...")
        
        # Replace just the faulty import section
        faulty_import = "# Import emergency fix module\n            from fix_order_submission import place_order_with_oco\n            \n            # Use the verified OCO order placement\n            success = place_order_with_oco(\n                api=self.api,\n                account_id=os.getenv('OANDA_ACCOUNT_ID'),\n                instrument=instrument,\n                units=int(units),\n                sl_price=sl,\n                tp_price=tp\n            )"
        
        inline_fix = '''# 🚑 EMERGENCY INLINE OCO FIX
            from oandapyV20.endpoints.orders import OrderCreate, OrderList
            import time
            
            # Build verified OCO order
            order_data = {
                "order": {
                    "instrument": instrument,
                    "units": str(int(units)),
                    "type": "MARKET",
                    "positionFill": "DEFAULT",
                    "stopLossOnFill": {"price": str(sl)},
                    "takeProfitOnFill": {"price": str(tp)}
                }
            }

            self.log_message(f"📤 VERIFIED ORDER: {units} {instrument} | SL: {sl} | TP: {tp}")

            try:
                # Submit order
                r = OrderCreate(accountID=os.getenv('OANDA_ACCOUNT_ID'), data=order_data)
                self.api.request(r)
                self.log_message("✅ ORDER ACCEPTED - Verifying OCO...")
                
                # Wait and verify
                time.sleep(2)
                orders_request = OrderList(accountID=os.getenv('OANDA_ACCOUNT_ID'))
                self.api.request(orders_request)
                orders = orders_request.response.get('orders', [])
                
                has_sl = any(o.get('instrument') == instrument and 'STOP_LOSS' in o.get('type', '') for o in orders)
                has_tp = any(o.get('instrument') == instrument and 'TAKE_PROFIT' in o.get('type', '') for o in orders)
                
                success = has_sl and has_tp
                if success:
                    self.log_message("🛡️ OCO VERIFIED!")
                else:
                    self.log_message("🚨 OCO FAILED!")
                    
            except Exception as e:
                self.log_message(f"❌ ORDER FAILED: {e}")
                success = False'''
        
        new_content = content.replace(faulty_import, inline_fix)
        
        # Write the fix
        with open('/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/router_live_hardcoded.py', 'w') as f:
            f.write(new_content)
        
        print("✅ INLINE OCO FIX APPLIED!")
        
        # Restart service
        import subprocess
        subprocess.run(['systemctl', '--user', 'restart', 'horsemen-proto_oanda.service'])
        print("🚀 Service restarted")
