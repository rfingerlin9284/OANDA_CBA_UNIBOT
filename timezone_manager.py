"""
🌍 TIMEZONE & MARKET SESSION MANAGER
Hamilton, NJ (EST/EDT) based trading with major market focus
"""
import pytz
from datetime import datetime, time
import schedule

class MarketSessionManager:
    def __init__(self):
        # User timezone: Eastern Time (Hamilton, NJ)
        self.user_tz = pytz.timezone('America/New_York')
        
        # Major market timezones
        self.london_tz = pytz.timezone('Europe/London')
        self.tokyo_tz = pytz.timezone('Asia/Tokyo')
        self.shanghai_tz = pytz.timezone('Asia/Shanghai')
        
        # OANDA market hours (24/7 except weekends)
        self.oanda_open = "Sunday 5:00 PM EST"
        self.oanda_close = "Friday 6:00 PM EST"
    
    def get_current_user_time(self):
        """Get current time in Hamilton, NJ timezone"""
        return datetime.now(self.user_tz)
    
    def get_market_times(self):
        """Get current time in all major markets"""
        now = datetime.now(pytz.UTC)
        return {
            'hamilton_nj': now.astimezone(self.user_tz),
            'london': now.astimezone(self.london_tz),
            'tokyo': now.astimezone(self.tokyo_tz),
            'shanghai': now.astimezone(self.shanghai_tz)
        }
    
    def is_oanda_open(self):
        """Check if OANDA market is open (Sunday 5PM - Friday 6PM EST)"""
        now = self.get_current_user_time()
        weekday = now.weekday()  # 0=Monday, 6=Sunday
        
        # Friday after 6 PM EST or Saturday - closed
        if weekday == 4 and now.hour >= 18:  # Friday 6 PM+
            return False
        if weekday == 5:  # Saturday - closed
            return False
        
        # Sunday before 5 PM EST - closed
        if weekday == 6 and now.hour < 17:  # Sunday before 5 PM
            return False
        
        return True
    
    def get_optimal_trading_sessions(self):
        """Get optimal trading periods for arbitrage"""
        market_times = self.get_market_times()
        
        sessions = {
            'london_open': {
                'local_time': '3:00 AM - 12:00 PM EST',
                'description': 'London session - High EUR/GBP volatility',
                'pairs': ['EUR/USD', 'GBP/USD', 'EUR/GBP', 'BTC/USD', 'ETH/USD']
            },
            'new_york_open': {
                'local_time': '8:00 AM - 5:00 PM EST',
                'description': 'NY session - USD pairs + crypto volume',
                'pairs': ['USD/JPY', 'USD/CAD', 'BTC/USD', 'ETH/USD', 'SOL/USD']
            },
            'asia_open': {
                'local_time': '7:00 PM - 4:00 AM EST',
                'description': 'Asian session - JPY pairs + crypto',
                'pairs': ['USD/JPY', 'AUD/USD', 'NZD/USD', 'BTC/USD', 'ETH/USD']
            },
            'overlap_london_ny': {
                'local_time': '8:00 AM - 12:00 PM EST',
                'description': 'London/NY overlap - MAXIMUM VOLATILITY',
                'pairs': ['EUR/USD', 'GBP/USD', 'USD/CHF', 'BTC/USD', 'ETH/USD']
            }
        }
        
        return sessions
    
    def get_current_session(self):
        """Determine current optimal trading session"""
        now = self.get_current_user_time()
        hour = now.hour
        
        if 8 <= hour < 12:
            return "overlap_london_ny"  # PEAK TRADING
        elif 3 <= hour < 12:
            return "london_open"
        elif 8 <= hour < 17:
            return "new_york_open"
        elif hour >= 19 or hour < 4:
            return "asia_open"
        else:
            return "transition"
    
    def schedule_session_optimization(self):
        """Schedule trading intensity based on market sessions"""
        # Peak trading during London/NY overlap
        schedule.every().day.at("08:00").do(self.increase_trading_intensity)
        schedule.every().day.at("12:00").do(self.normal_trading_intensity)
        
        # Reduce intensity during low volatility periods
        schedule.every().day.at("17:00").do(self.reduce_trading_intensity)
        schedule.every().day.at("03:00").do(self.normal_trading_intensity)
        
        return True
    
    def increase_trading_intensity(self):
        """Increase scan frequency during peak sessions"""
        return {
            'scan_interval': 1,  # 1 second scans
            'min_confluence': 6.5,  # Lower threshold for more trades
            'max_concurrent': 5  # More liveultaneous trades
        }
    
    def normal_trading_intensity(self):
        """Normal trading intensity"""
        return {
            'scan_interval': 2,  # 2 second scans
            'min_confluence': 7.0,  # Normal threshold
            'max_concurrent': 3  # Normal trade count
        }
    
    def reduce_trading_intensity(self):
        """Reduce intensity during low volatility"""
        return {
            'scan_interval': 5,  # 5 second scans
            'min_confluence': 7.5,  # Higher threshold
            'max_concurrent': 2  # Fewer trades
        }
    
    def get_current_session_info(self):
        """
        🧠 GET ENHANCED SESSION INFO FOR BIAS DISPATCH
        Returns comprehensive session data for psychology-aware trading
        """
        try:
            now = self.get_current_user_time()
            hour = now.hour
            weekday = now.weekday()
            
            # Determine active sessions and overlaps
            active_sessions = []
            if 3 <= hour < 12:
                active_sessions.append('London')
            if 8 <= hour < 17:
                active_sessions.append('New York')
            if hour >= 19 or hour < 4:
                active_sessions.append('Asia')
            
            # Determine overlap zones
            overlap_zone = None
            if 'London' in active_sessions and 'New York' in active_sessions:
                overlap_zone = 'London/NY Overlap'
            elif 19 <= hour <= 23 or 0 <= hour <= 2:
                overlap_zone = 'Asia/London Transition'
            
            # Assess volatility and bias
            volatility = self._assess_session_volatility(active_sessions, overlap_zone, hour)
            market_bias = self._determine_session_bias(active_sessions, overlap_zone, hour)
            
            return {
                'hamilton_time': now.strftime('%Y-%m-%d %H:%M:%S %Z'),
                'active_sessions': active_sessions,
                'current_session': self.get_current_session(),
                'overlap_zone': overlap_zone,
                'volatility_level': volatility,
                'suggested_bias': market_bias,
                'is_weekend': weekday >= 5,
                'is_oanda_open': self.is_oanda_open(),
                'hour': hour,
                'weekday': weekday
            }
            
        except Exception as e:
            print(f"Session info error: {e}")
            return self._get_default_session_info()
    
    def _assess_session_volatility(self, active_sessions, overlap_zone, hour):
        """Assess expected volatility based on session characteristics"""
        if overlap_zone == 'London/NY Overlap':
            return 'Very High'  # Peak volatility 8AM-12PM EST
        elif len(active_sessions) >= 2:
            return 'High'  # Multiple session overlap
        elif 8 <= hour <= 17:  # NY or London solo
            return 'Medium'
        elif hour >= 19 or hour <= 4:  # Asian session
            return 'Low'  # Typically range-bound
        else:
            return 'Very Low'  # Transition periods
    
    def _determine_session_bias(self, active_sessions, overlap_zone, hour):
        """
        🧠 DETERMINE SESSION-SPECIFIC MARKET BIAS
        Different sessions exhibit different behavioral patterns
        """
        # London/NY Overlap - Momentum and breakouts
        if overlap_zone == 'London/NY Overlap':
            return 'Momentum'
        
        # London Session - Trend initiation, breakouts
        elif 'London' in active_sessions and hour < 8:
            return 'Breakout'
        elif 'London' in active_sessions:
            return 'Momentum'
        
        # NY Session patterns
        elif 'New York' in active_sessions:
            if 8 <= hour <= 12:
                return 'Momentum'  # Morning momentum
            elif 13 <= hour <= 16:
                return 'Reversal'  # Afternoon reversals
            else:
                return 'Consolidation'
        
        # Asian Session - Range trading, mean reversion
        elif 'Asia' in active_sessions:
            return 'Range'
        
        else:
            return 'Neutral'
    
    def get_bias_dispatch_settings(self):
        """
        ⚙️ GET BIAS-SPECIFIC TRADING SETTINGS
        Returns adjusted parameters for harmony with market flow
        """
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        session_info = self.get_current_session_info()
        bias = session_info['suggested_bias']
        volatility = session_info['volatility_level']
        
        settings = {
            'bias': bias,
            'volatility': volatility,
            'sl_adjustment': 1.0,
            'min_confluence': 7.0,
            'scan_interval': 10,
            'max_concurrent': 3
        }
        
        # Bias-specific adjustments
        if bias == 'Momentum':
            settings.update({
                'sl_adjustment': creds.BULL_SL_ADJUSTMENT,  # Wider SL for momentum
                'min_confluence': 6.8,  # Lower threshold for trending
                'scan_interval': 5  # Faster scanning
            })
        elif bias == 'Range':
            settings.update({
                'sl_adjustment': creds.BEAR_SL_ADJUSTMENT,  # Tighter SL for ranges
                'min_confluence': 7.2,  # Higher threshold for ranges
                'scan_interval': 15  # Slower scanning
            })
        elif bias == 'Breakout':
            settings.update({
                'sl_adjustment': 1.1,  # Slightly wider for breakouts
                'min_confluence': 7.5,  # High threshold for quality
                'scan_interval': 8
            })
        elif bias == 'Reversal':
            settings.update({
                'sl_adjustment': 0.95,  # Tighter for reversals
                'min_confluence': 7.8,  # Very high threshold
                'scan_interval': 12
            })
        
        # Volatility adjustments
        if volatility == 'Very High':
            settings['sl_adjustment'] *= 1.2  # Extra room for volatility
            settings['max_concurrent'] = 5
        elif volatility == 'Low':
            settings['sl_adjustment'] *= 0.9  # Tighter for low vol
            settings['max_concurrent'] = 2
        
        return settings
    
    def _get_default_session_info(self):
        """Default session info for error cases"""
        return {
            'hamilton_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S EST'),
            'active_sessions': [],
            'current_session': 'Unknown',
            'overlap_zone': None,
            'volatility_level': 'Unknown',
            'suggested_bias': 'Neutral',
            'is_weekend': False,
            'is_oanda_open': False,
            'hour': 12,
            'weekday': 0
        }

def display_market_status():
    """Display current market status for Hamilton, NJ trader"""
    manager = MarketSessionManager()
    
    print("🌍 MARKET SESSION STATUS - HAMILTON, NJ TRADER")
    print("=" * 50)
    
    # Current times
    times = manager.get_market_times()
    for market, time_obj in times.items():
        print(f"📍 {market.upper()}: {time_obj.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # OANDA status
    oanda_status = "🟢 OPEN" if manager.is_oanda_open() else "🔴 CLOSED"
    print(f"\n💱 OANDA Market: {oanda_status}")
    print(f"   Hours: Sunday 5PM - Friday 6PM EST")
    
    # Current session
    current_session = manager.get_current_session()
    sessions = manager.get_optimal_trading_sessions()
    
    if current_session in sessions:
        session_info = sessions[current_session]
        print(f"\n🎯 CURRENT SESSION: {current_session.upper()}")
        print(f"   Time: {session_info['local_time']}")
        print(f"   Focus: {session_info['description']}")
        print(f"   Optimal Pairs: {', '.join(session_info['pairs'])}")
    
    return manager

if __name__ == "__main__":
    display_market_status()
