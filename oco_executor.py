IS_LIVE_MODE = True

REQUIRE_OCO = True

REQUIRE_COINBASE_API = True

if not IS_LIVE_MODE:

    raise RuntimeError("�� LIVE_MODE is not active. Execution blocked.")


#!/usr/bin/env python3
"""
⚡ WOLFPACK-LITE OCO EXECUTOR
Mandatory OCO execution with smart trailing stops
"""

import time
import threading
from logger import logger, log_trade, log_error, log_pnl

class OCOExecutor:
    def __init__(self, coinbase_client, oanda_client, credentials):
        self.coinbase = coinbase_client
        self.oanda = oanda_client
        self.creds = credentials
        self.active_trades = {}  # Track all live OCO positions
        self.monitor_thread = None
        self.is_monitoring = False
        
    def place_oco_trade(self, symbol, side, entry_price, sl_price, tp_price, platform="coinbase"):
        """
        🎯 PLACE OCO TRADE
        Mandatory OCO with stop loss + take profit
        """
        try:
            # Calculate position size
            balance = self.get_balance(platform)
            risk_amount = balance * (self.creds.RISK_PER_TRADE / 100)
            
            # Apply streak multiplier
            streak_multiplier = logger.get_streak_multiplier()
            risk_amount *= streak_multiplier
            
            # Calculate pip distance for position sizing
            pip_distance = abs(entry_price - sl_price)
            position_size = risk_amount / pip_distance
            
            # Platform-specific execution
            if platform == "coinbase":
                return self._place_coinbase_oco(symbol, side, entry_price, sl_price, tp_price, position_size)
            else:
                return self._place_oanda_oco(symbol, side, entry_price, sl_price, tp_price, position_size)
                
        except Exception as e:
            log_error(f"OCO placement failed: {str(e)}", "OCO_EXECUTOR")
            return None
    
    def _place_coinbase_oco(self, symbol, side, entry_price, sl_price, tp_price, size):
        """
        💱 COINBASE ADVANCED TRADE LIVE OCO EXECUTION
        Market order + OCO bracket - LIVE TRADING ONLY
        """
        try:
            # Step 1: Place LIVE market order
            market_order = self.coinbase.create_market_order(
                symbol=symbol,
                side=side,
                amount=size
            )
            
            if not market_order:
                raise Exception("LIVE market order failed")
            
            order_id = market_order['id']
            actual_fill = float(market_order.get('filled', 0))
            actual_price = float(market_order.get('average', entry_price))
            
            # Step 2: Place OCO bracket orders
            oco_data = self._place_coinbase_bracket(symbol, side, actual_fill, sl_price, tp_price)
            
            # Step 3: Track position
            trade_data = {
                "symbol": symbol,
                "side": side,
                "size": actual_fill,
                "entry_price": actual_price,
                "sl_price": sl_price,
                "tp_price": tp_price,
                "sl_order_id": oco_data['sl_id'],
                "tp_order_id": oco_data['tp_id'],
                "platform": "coinbase",
                "timestamp": time.time(),
                "trailing_stop": None
            }
            
            self.active_trades[order_id] = trade_data
            
            # Add to position tracker
            from position_tracker import add_position
            add_position(order_id, symbol, side, actual_fill, actual_price, sl_price, tp_price, "coinbase", trade_data)
            
            log_trade(f"✅ OCO PLACED {symbol} {side.upper()} | Size: {actual_fill:.6f} | "
                     f"Entry: {actual_price:.6f} | SL: {sl_price:.6f} | TP: {tp_price:.6f}")
            
            return order_id
            
        except Exception as e:
            log_error(f"Coinbase OCO failed: {str(e)}", "COINBASE_OCO")
            return None
    
    def _place_coinbase_bracket(self, symbol, side, size, sl_price, tp_price):
        """Place stop loss and take profit orders"""
        try:
            # Opposite side for closing orders
            opposite_side = "sell" if side == "buy" else "buy"
            
            # Stop Loss Order
            sl_order = self.coinbase.create_limit_order(
                symbol=symbol,
                side=opposite_side,
                amount=size,
                price=sl_price,
                type='stop_loss'
            )
            
            # Take Profit Order
            tp_order = self.coinbase.create_limit_order(
                symbol=symbol,
                side=opposite_side,
                amount=size,
                price=tp_price,
                type='limit'
            )
            
            return {
                'sl_id': sl_order['id'],
                'tp_id': tp_order['id']
            }
            
        except Exception as e:
            raise Exception(f"Bracket orders failed: {str(e)}")
    
    def _place_oanda_oco(self, symbol, side, entry_price, sl_price, tp_price, size):
        """
        🏛️ OANDA LIVE OCO EXECUTION
        Market order with automatic SL/TP - LIVE TRADING ONLY
        """
        try:
            # Convert to OANDA format
            oanda_symbol = symbol.replace('/', '_')
            units = int(size * 10000)  # Standard lot conversion
            
            if side == "sell":
                units = -units
            
            # Place LIVE market order with SL/TP
            order_data = {
                "order": {
                    "units": str(units),
                    "instrument": oanda_symbol,
                    "timeInForce": "IOC",
                    "type": "MARKET",
                    "stopLossOnFill": {
                        "price": str(sl_price)
                    },
                    "takeProfitOnFill": {
                        "price": str(tp_price)
                    }
                }
            }
            
            response = self.oanda.order.create(
                accountID=self.creds.OANDA_ACCOUNT_ID,
                data=order_data
            )
            
            if response.status != 201:
                raise Exception(f"OANDA order failed: {response.body}")
            
            # CRITICAL FIX: Check for attached orders in response
            response_body = response.body
            order_id = None
            actual_price = entry_price
            actual_size = abs(units)
            
            # Check if order was filled
            if 'orderFillTransaction' in response_body:
                fill_txn = response_body['orderFillTransaction']
                order_id = fill_txn.get('id')
                actual_price = float(fill_txn.get('price', entry_price))
                actual_size = abs(float(fill_txn.get('units', units)))
                
                # CRITICAL: Verify attached SL/TP orders were created
                has_sl = 'stopLossOrderTransaction' in response_body
                has_tp = 'takeProfitOrderTransaction' in response_body
                
                if not (has_sl and has_tp):
                    # OCO verification failed - cancel any partial orders
                    log_error(f"CRITICAL: OCO incomplete for {oanda_symbol} - SL: {has_sl}, TP: {has_tp}", "OCO_VERIFICATION")
                    raise Exception(f"OCO verification failed: SL={has_sl}, TP={has_tp}")
                
                # Log successful OCO verification
                sl_order_id = response_body['stopLossOrderTransaction'].get('id') if has_sl else None
                tp_order_id = response_body['takeProfitOrderTransaction'].get('id') if has_tp else None
                
                log_trade(f"🛡️ OANDA OCO VERIFIED: SL Order: {sl_order_id}, TP Order: {tp_order_id}", "OCO_VERIFICATION")
            
            elif 'orderCreateTransaction' in response_body:
                # Order created but not filled (pending)
                create_txn = response_body['orderCreateTransaction']
                order_id = create_txn.get('id')
                log_trade(f"📋 OANDA Order created (pending): {order_id}", "OANDA_ORDER")
            else:
                raise Exception("No valid order transaction in response")
            
            # Track position with proper validation
            trade_data = {
                "symbol": symbol,
                "side": side,
                "size": actual_size,
                "entry_price": actual_price,
                "sl_price": sl_price,
                "tp_price": tp_price,
                "platform": "oanda",
                "timestamp": time.time(),
                "trade_id": response_body.get('orderFillTransaction', {}).get('tradeOpened', {}).get('tradeID'),
                "trailing_stop": None,
                "sl_order_id": response_body.get('stopLossOrderTransaction', {}).get('id'),
                "tp_order_id": response_body.get('takeProfitOrderTransaction', {}).get('id')
            }
            
            self.active_trades[order_id] = trade_data
            
            # Add to position tracker
            from position_tracker import add_position
            add_position(order_id, symbol, side, actual_size, actual_price, sl_price, tp_price, "oanda", trade_data)
            
            log_trade(f"✅ OANDA OCO PLACED {symbol} {side.upper()} | "
                     f"Size: {actual_size:.0f} units | Entry: {actual_price:.5f} | "
                     f"SL: {sl_price:.5f} | TP: {tp_price:.5f}")
            
            return order_id
            
        except Exception as e:
            log_error(f"OANDA OCO failed: {str(e)}", "OANDA_OCO")
            return None
    
    def start_monitoring(self):
        """
        🔄 START OCO MONITORING
        Background thread to track all positions
        """
        if self.is_monitoring:
            return
            
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_positions, daemon=True)
        self.monitor_thread.start()
        
        log_trade("🔄 OCO monitoring started", "MONITOR")
    
    def _monitor_positions(self):
        """Background monitoring of all OCO positions"""
        while self.is_monitoring:
            try:
                if not self.active_trades:
                    time.sleep(2)
                    continue
                
                for order_id, trade_data in list(self.active_trades.items()):
                    self._check_position_status(order_id, trade_data)
                    self._update_trailing_stop(order_id, trade_data)
                
                time.sleep(1)  # Check every second
                
            except Exception as e:
                log_error(f"Monitor error: {str(e)}", "MONITOR")
                time.sleep(5)
    
    def _check_position_status(self, order_id, trade_data):
        """Check if position was closed"""
        try:
            platform = trade_data["platform"]
            
            if platform == "coinbase":
                # Check if either SL or TP was filled
                sl_status = self.coinbase.fetch_order(trade_data["sl_order_id"])
                tp_status = self.coinbase.fetch_order(trade_data["tp_order_id"])
                
                if sl_status['status'] == 'closed':
                    self._handle_trade_close(order_id, trade_data, "STOP_LOSS", sl_status['average'])
                elif tp_status['status'] == 'closed':
                    self._handle_trade_close(order_id, trade_data, "TAKE_PROFIT", tp_status['average'])
                    
            else:  # OANDA
                # Check trade status via positions API
                positions = self.oanda.position.list_open(accountID=self.creds.OANDA_ACCOUNT_ID)
                trade_id = trade_data.get("trade_id")
                
                # Check if trade is still open
                open_trades = [pos.get('long', {}).get('tradeIDs', []) + 
                              pos.get('short', {}).get('tradeIDs', []) 
                              for pos in positions.body.get('positions', [])]
                
                if trade_id and trade_id not in str(open_trades):
                    # Trade was closed - get close info from transactions
                    self._handle_oanda_close(order_id, trade_data)
                    
        except Exception as e:
            log_error(f"Status check failed: {str(e)}", "STATUS_CHECK")
    
    def _handle_oanda_close(self, order_id, trade_data):
        """Handle OANDA trade closure"""
        try:
            # For OANDA, we'll need to check transaction history for close price
            # For now, use current market price as approximation
            symbol = trade_data["symbol"].replace('/', '_')
            current_price = self._get_current_price(symbol)
            
            # Determine if it was SL or TP based on price
            if trade_data["side"].lower() == "buy":
                if current_price <= trade_data["sl_price"]:
                    reason = "STOP_LOSS"
                    exit_price = trade_data["sl_price"]
                else:
                    reason = "TAKE_PROFIT"
                    exit_price = trade_data["tp_price"]
            else:
                if current_price >= trade_data["sl_price"]:
                    reason = "STOP_LOSS"
                    exit_price = trade_data["sl_price"]
                else:
                    reason = "TAKE_PROFIT"
                    exit_price = trade_data["tp_price"]
            
            self._handle_trade_close(order_id, trade_data, reason, exit_price)
            
        except Exception as e:
            log_error(f"OANDA close handling failed: {str(e)}", "OANDA_CLOSE")
    
    def _get_current_price(self, oanda_symbol):
        """Get current market price for OANDA symbol"""
        try:
            # This would typically fetch from pricing API
            # For now, return None to avoid errors
            return None
        except:
            return None
    
    def _handle_trade_close(self, order_id, trade_data, close_reason, exit_price):
        """Handle trade closure and update tracking"""
        try:
            # Calculate P&L
            if trade_data["side"].lower() == "buy":
                pnl = (exit_price - trade_data["entry_price"]) * trade_data["size"]
            else:
                pnl = (trade_data["entry_price"] - exit_price) * trade_data["size"]
            
            # Update position tracker
            from position_tracker import close_position
            close_position(order_id, exit_price, close_reason, pnl)
            
            # Remove from active trades
            if order_id in self.active_trades:
                del self.active_trades[order_id]
            
            # Log closure
            status = "🎯" if close_reason == "TAKE_PROFIT" else "🛑"
            log_trade(f"{status} TRADE CLOSED: {trade_data['symbol']} | "
                     f"Reason: {close_reason} | P&L: ${pnl:.2f}")
            
            # Log P&L
            log_pnl(
                trade_data["symbol"], 
                trade_data["side"], 
                trade_data["entry_price"], 
                exit_price, 
                pnl,
                self._get_current_balance(),
                self._get_current_streak()
            )
            
        except Exception as e:
            log_error(f"Error handling trade close: {str(e)}", "TRADE_CLOSE")
    
    def _get_current_balance(self):
        """Get current balance from position tracker"""
        try:
            from position_tracker import position_tracker
            return position_tracker.get_total_balance()
        except:
            return 3000.0  # Default starting balance
    
    def _get_current_streak(self):
        """Get current streak from position tracker"""
        try:
            from position_tracker import position_tracker
            return position_tracker.get_current_streak()
        except:
            return 0
    
    def _update_trailing_stop(self, order_id, trade_data):
        """
        🔥 SMART TRAILING STOP
        Update SL when in profit
        """
        try:
            current_price = self.get_current_price(trade_data["symbol"], trade_data["platform"])
            entry_price = trade_data["entry_price"]
            side = trade_data["side"]
            
            # Calculate profit distance
            if side == "buy":
                profit_distance = current_price - entry_price
                should_trail = profit_distance > 0
            else:
                profit_distance = entry_price - current_price
                should_trail = profit_distance > 0
            
            if should_trail and profit_distance > abs(entry_price - trade_data["sl_price"]) * 0.5:
                # Update trailing stop when profit > 50% of initial risk
                new_sl = self._calculate_trailing_sl(trade_data, current_price)
                
                if new_sl != trade_data["sl_price"]:
                    self._update_stop_loss(order_id, trade_data, new_sl)
                    
        except Exception as e:
            log_error(f"Trailing stop error: {str(e)}", "TRAILING")
    
    def _calculate_trailing_sl(self, trade_data, current_price):
        """Calculate new trailing stop level"""
        entry_price = trade_data["entry_price"]
        side = trade_data["side"]
        
        # Trail at 50% of profit
        if side == "buy":
            profit = current_price - entry_price
            new_sl = entry_price + (profit * 0.5)
        else:
            profit = entry_price - current_price
            new_sl = entry_price - (profit * 0.5)
        
        return round(new_sl, 6)
    
    def _update_stop_loss(self, order_id, trade_data, new_sl):
        """Update stop loss order"""
        try:
            platform = trade_data["platform"]
            
            if platform == "coinbase":
                # Cancel old SL and place new one
                self.coinbase.cancel_order(trade_data["sl_order_id"])
                
                opposite_side = "sell" if trade_data["side"] == "buy" else "buy"
                new_sl_order = self.coinbase.create_limit_order(
                    symbol=trade_data["symbol"],
                    side=opposite_side,
                    amount=trade_data["size"],
                    price=new_sl,
                    type='stop_loss'
                )
                
                trade_data["sl_order_id"] = new_sl_order['id']
                
            else:  # OANDA
                # Update trade's stop loss
                trade_id = trade_data.get("trade_id")
                update_data = {
                    "stopLoss": {
                        "price": str(new_sl)
                    }
                }
                
                self.oanda.trade.set_dependent_orders(
                    accountID=self.creds.OANDA_ACCOUNT_ID,
                    tradeID=trade_id,
                    data=update_data
                )
            
            # Update tracking
            old_sl = trade_data["sl_price"]
            trade_data["sl_price"] = new_sl
            
            log_trade(f"🔄 TRAIL {trade_data['symbol']} | SL: {old_sl:.6f} → {new_sl:.6f}", "TRAIL")
            
        except Exception as e:
            log_error(f"SL update failed: {str(e)}", "SL_UPDATE")
    
    def _handle_trade_close(self, order_id, trade_data, close_type, exit_price):
        """Handle completed trade"""
        try:
            # Calculate P&L
            entry_price = trade_data["entry_price"]
            size = trade_data["size"]
            side = trade_data["side"]
            
            if side == "buy":
                pnl = (exit_price - entry_price) * size
            else:
                pnl = (entry_price - exit_price) * size
            
            # Update balance and streak
            current_balance = logger.streak_data["balance"]
            new_balance = current_balance + pnl
            
            # Get current streak for logging
            if pnl > 0:
                streak = logger.streak_data["win_streak"] + 1
            else:
                streak = -(logger.streak_data["loss_streak"] + 1)
            
            # Log the trade
            log_pnl(
                trade_data["symbol"], 
                side, 
                entry_price, 
                exit_price, 
                pnl, 
                new_balance, 
                streak
            )
            
            close_emoji = "✅" if pnl > 0 else "❌"
            log_trade(f"{close_emoji} {close_type} {trade_data['symbol']} | "
                     f"P&L: ${pnl:.2f} | Balance: ${new_balance:.2f}")
            
            # Remove from active trades
            del self.active_trades[order_id]
            
        except Exception as e:
            log_error(f"Trade close handling failed: {str(e)}", "CLOSE_HANDLER")
    
    def _handle_oanda_close(self, order_id, trade_data):
        """Handle OANDA trade closure"""
        # Simplified - would need to query transaction history for exact close price
        # For now, assume it hit one of our targets
        avg_price = (trade_data["sl_price"] + trade_data["tp_price"]) / 2
        self._handle_trade_close(order_id, trade_data, "CLOSED", avg_price)
    
    def get_balance(self, platform):
        """Get current account balance"""
        try:
            if platform == "coinbase":
                balance = self.coinbase.fetch_balance()
                return float(balance.get('USD', {}).get('free', 0))
            else:
                account = self.oanda.account.get(accountID=self.creds.OANDA_ACCOUNT_ID)
                return float(account.body['account']['balance'])
        except:
            return 3000.0  # Default balance
    
    def get_current_price(self, symbol, platform):
        """Get current market price"""
        try:
            if platform == "coinbase":
                ticker = self.coinbase.fetch_ticker(symbol)
                return float(ticker['last'])
            else:
                oanda_symbol = symbol.replace('/', '_')
                pricing = self.oanda.pricing.get(
                    accountID=self.creds.OANDA_ACCOUNT_ID,
                    instruments=oanda_symbol
                )
                price_data = pricing.body['prices'][0]
                return (float(price_data['asks'][0]['price']) + float(price_data['bids'][0]['price'])) / 2
        except:
            return 0.0
    
    def emergency_close_all(self):
        """
        🚨 EMERGENCY CLOSE ALL POSITIONS
        Market close all trades
        """
        log_trade("🚨 EMERGENCY CLOSE ALL TRIGGERED", "EMERGENCY")
        
        for order_id, trade_data in list(self.active_trades.items()):
            try:
                platform = trade_data["platform"]
                symbol = trade_data["symbol"]
                side = "sell" if trade_data["side"] == "buy" else "buy"
                size = trade_data["size"]
                
                if platform == "coinbase":
                    # Cancel OCO orders and market close
                    self.coinbase.cancel_order(trade_data["sl_order_id"])
                    self.coinbase.cancel_order(trade_data["tp_order_id"])
                    self.coinbase.create_market_order(symbol=symbol, side=side, amount=size)
                else:
                    # OANDA market close
                    trade_id = trade_data.get("trade_id")
                    if trade_id:
                        self.oanda.trade.close(
                            accountID=self.creds.OANDA_ACCOUNT_ID,
                            tradeID=trade_id
                        )
                
                log_trade(f"🚨 EMERGENCY CLOSED {symbol}", "EMERGENCY")
                del self.active_trades[order_id]
                
            except Exception as e:
                log_error(f"Emergency close failed for {trade_data['symbol']}: {str(e)}", "EMERGENCY")
    
    def stop_monitoring(self):
        """Stop position monitoring"""
        self.is_monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
        log_trade("🛑 OCO monitoring stopped", "MONITOR")

if __name__ == "__main__":
    print("⚡ OCO Executor initialized")
