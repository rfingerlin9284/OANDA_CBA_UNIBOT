"""
💰 LIVE PORTFOLIO & TRADE MANAGER
Direct API portfolio updates and arbitrage monitoring
Hamilton, NJ timezone-aware trading
"""
import time
import json
from datetime import datetime
from threading import Thread, Lock
import ccxt
import oandapyV20
from oandapyV20.endpoints.accounts import AccountDetails, AccountSummary
from oandapyV20.endpoints.positions import OpenPositions
from oandapyV20.endpoints.orders import OrderList

class LivePortfolioManager:
    def __init__(self, credentials):
        self.creds = credentials
        self.portfolio_lock = Lock()
        
        # Initialize APIs
        self.coinbase = None
        self.oanda = None
        
        # Portfolio data
        self.portfolio_data = {
            'coinbase': {
                'balances': {},
                'positions': {},
                'orders': {},
                'last_update': None
            },
            'oanda': {
                'balance': 0.0,
                'positions': {},
                'orders': {},
                'last_update': None
            }
        }
        
        # Arbitrage opportunities
        self.arbitrage_opportunities = []
        
    def initialize_apis(self):
        """Initialize live trading APIs"""
        print("🔌 Initializing LIVE APIs for portfolio management...")
        
        # Coinbase Advanced Trade
        self.coinbase = ccxt.coinbase({
            'apiKey': self.creds.COINBASE_API_KEY,
            'secret': self.creds.COINBASE_SECRET,
            'passphrase': self.creds.COINBASE_PASSPHRASE,
            'live_mode': False,  # LIVE TRADING
            'urls': {'api': self.creds.COINBASE_LIVE_URL},
            'enableRateLimit': True,
        })
        
        # OANDA Live API
        self.oanda = oandapyV20.API(
            access_token=self.creds.OANDA_API_KEY,
            environment="live"
        )
        
        print("✅ Live APIs initialized for Hamilton, NJ trader")
        return True
    
    def update_coinbase_portfolio(self):
        """Get live Coinbase portfolio data"""
        try:
            with self.portfolio_lock:
                # Get account balances
                balance = self.coinbase.fetch_balance()
                
                # Get open orders
                orders = {}
                for symbol in self.creds.COINBASE_PAIRS:
                    try:
                        symbol_orders = self.coinbase.fetch_open_orders(symbol)
                        if symbol_orders:
                            orders[symbol] = symbol_orders
                    except:
                        continue
                
                # Update portfolio data
                self.portfolio_data['coinbase'] = {
                    'balances': balance,
                    'orders': orders,
                    'last_update': datetime.now().isoformat()
                }
                
                return True
                
        except Exception as e:
            print(f"❌ Coinbase portfolio update error: {e}")
            return False
    
    def update_oanda_portfolio(self):
        """Get live OANDA portfolio data"""
        try:
            with self.portfolio_lock:
                # Get account summary
                account_summary = AccountSummary(self.creds.OANDA_ACCOUNT_ID)
                response = self.oanda.request(account_summary)
                account_data = response['account']
                
                # Get open positions
                positions_req = OpenPositions(self.creds.OANDA_ACCOUNT_ID)
                positions_response = self.oanda.request(positions_req)
                positions = positions_response.get('positions', [])
                
                # Get open orders
                orders_req = OrderList(self.creds.OANDA_ACCOUNT_ID)
                orders_response = self.oanda.request(orders_req)
                orders = orders_response.get('orders', [])
                
                # Update portfolio data
                self.portfolio_data['oanda'] = {
                    'balance': float(account_data['balance']),
                    'nav': float(account_data['NAV']),
                    'unrealized_pl': float(account_data['unrealizedPL']),
                    'margin_used': float(account_data['marginUsed']),
                    'margin_available': float(account_data['marginAvailable']),
                    'positions': {pos['instrument']: pos for pos in positions if float(pos['long']['units']) != 0 or float(pos['short']['units']) != 0},
                    'orders': {order['id']: order for order in orders},
                    'last_update': datetime.now().isoformat()
                }
                
                return True
                
        except Exception as e:
            print(f"❌ OANDA portfolio update error: {e}")
            return False
    
    def find_arbitrage_opportunities(self):
        """Find price differences between Coinbase and OANDA for overlapping pairs"""
        opportunities = []
        
        try:
            # Common pairs that exist on both platforms
            common_pairs = ['BTC/USD', 'ETH/USD']  # Can expand this
            
            for pair in common_pairs:
                try:
                    # Get Coinbase price
                    coinbase_ticker = self.coinbase.fetch_ticker(pair)
                    coinbase_price = coinbase_ticker['last']
                    
                    # For OANDA, we don't have crypto directly, so skip for now
                    # This would be for forex pairs if both platforms supported them
                    
                except Exception as e:
                    continue
            
            # Look for forex arbitrage opportunities (different brokers, spreads, etc.)
            # This is more theoretical since we're using one forex broker (OANDA)
            
        except Exception as e:
            print(f"❌ Arbitrage scan error: {e}")
        
        self.arbitrage_opportunities = opportunities
        return opportunities
    
    def get_portfolio_summary(self):
        """Get comprehensive portfolio summary"""
        with self.portfolio_lock:
            summary = {
                'timestamp': datetime.now().isoformat(),
                'total_usd_value': 0.0,
                'platforms': {}
            }
            
            # Coinbase summary
            coinbase_data = self.portfolio_data['coinbase']
            if coinbase_data['balances']:
                usd_balance = coinbase_data['balances'].get('USD', {}).get('free', 0)
                btc_balance = coinbase_data['balances'].get('BTC', {}).get('free', 0)
                eth_balance = coinbase_data['balances'].get('ETH', {}).get('free', 0)
                
                # Estimate USD value (liveplified)
                total_coinbase_usd = float(usd_balance)
                
                summary['platforms']['coinbase'] = {
                    'usd_balance': float(usd_balance),
                    'btc_balance': float(btc_balance),
                    'eth_balance': float(eth_balance),
                    'estimated_usd_total': total_coinbase_usd,
                    'active_orders': len(coinbase_data['orders']),
                    'last_update': coinbase_data['last_update']
                }
                
                summary['total_usd_value'] += total_coinbase_usd
            
            # OANDA summary
            oanda_data = self.portfolio_data['oanda']
            if oanda_data.get('balance', 0) > 0:
                summary['platforms']['oanda'] = {
                    'balance': oanda_data['balance'],
                    'nav': oanda_data.get('nav', 0),
                    'unrealized_pl': oanda_data.get('unrealized_pl', 0),
                    'margin_used': oanda_data.get('margin_used', 0),
                    'margin_available': oanda_data.get('margin_available', 0),
                    'active_positions': len(oanda_data.get('positions', {})),
                    'active_orders': len(oanda_data.get('orders', {})),
                    'last_update': oanda_data['last_update']
                }
                
                summary['total_usd_value'] += oanda_data['balance']
            
            return summary
    
    def start_portfolio_monitoring(self, update_interval=30):
        """Start continuous portfolio monitoring"""
        print(f"🔄 Starting portfolio monitoring (every {update_interval}s)")
        
        def monitor_loop():
            while True:
                try:
                    # Update both portfolios
                    self.update_coinbase_portfolio()
                    self.update_oanda_portfolio()
                    
                    # Check for arbitrage opportunities
                    self.find_arbitrage_opportunities()
                    
                    # Print summary every 5 minutes
                    if int(time.time()) % 300 == 0:
                        self.print_portfolio_summary()
                    
                except Exception as e:
                    print(f"❌ Portfolio monitoring error: {e}")
                
                time.sleep(update_interval)
        
        # Start monitoring thread
        monitor_thread = Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        
        return monitor_thread
    
    def print_portfolio_summary(self):
        """Print formatted portfolio summary"""
        summary = self.get_portfolio_summary()
        
        print("\n" + "="*60)
        print("💰 LIVE PORTFOLIO SUMMARY - HAMILTON, NJ")
        print(f"🕐 {summary['timestamp']}")
        print("="*60)
        
        print(f"💵 Total Portfolio Value: ${summary['total_usd_value']:,.2f}")
        
        for platform, data in summary['platforms'].items():
            print(f"\n📊 {platform.upper()}:")
            
            if platform == 'coinbase':
                print(f"   💵 USD: ${data['usd_balance']:,.2f}")
                print(f"   ₿ BTC: {data['btc_balance']:.8f}")
                print(f"   ⟠ ETH: {data['eth_balance']:.6f}")
                print(f"   📋 Active Orders: {data['active_orders']}")
            
            elif platform == 'oanda':
                print(f"   💰 Balance: ${data['balance']:,.2f}")
                print(f"   📈 NAV: ${data['nav']:,.2f}")
                print(f"   📊 Unrealized P&L: ${data['unrealized_pl']:,.2f}")
                print(f"   💳 Margin Used: ${data['margin_used']:,.2f}")
                print(f"   💰 Margin Available: ${data['margin_available']:,.2f}")
                print(f"   📍 Active Positions: {data['active_positions']}")
                print(f"   📋 Active Orders: {data['active_orders']}")
            
            print(f"   🕐 Last Update: {data['last_update']}")
        
        print("="*60)

    """Test live portfolio management"""
    from credentials import WolfpackCredentials
    
    creds = WolfpackCredentials()
    portfolio = LivePortfolioManager(creds)
    
    if portfolio.initialize_apis():
        print("✅ Testing live portfolio updates...")
        
        # Test updates
        coinbase_ok = portfolio.update_coinbase_portfolio()
        oanda_ok = portfolio.update_oanda_portfolio()
        
        if coinbase_ok and oanda_ok:
            portfolio.print_portfolio_summary()
            return True
        else:
            print("❌ Portfolio update failed")
            return False
    else:
        print("❌ API initialization failed")
        return False

if __name__ == "__main__":
