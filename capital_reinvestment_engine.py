#!/usr/bin/env python3
"""Capital Reinvestment Engine - Compound Growth via Strategy Performance"""
import json
from datetime import datetime, timedelta

class CapitalReinvestmentEngine:
    def __init__(self):
        self.strategy_allocations = {
            'MODEL_A': 1.0,
            'MODEL_B': 1.0,
            'MODEL_C': 1.0,
            'MODEL_D': 1.0,
            'RSI': 0.8,
            'MACD': 0.8
        }
        self.performance_history = {}
        self.reallocation_threshold = 0.70  # 70% win rate threshold
        self.max_allocation = 2.0  # Max 2x allocation
        self.min_allocation = 0.3  # Min 0.3x allocation
        
    def update_strategy_performance(self, strategy, outcome, profit_loss):
        """Track strategy performance for allocation decisions"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if strategy not in self.performance_history:
            self.performance_history[strategy] = {}
        
        if today not in self.performance_history[strategy]:
            self.performance_history[strategy][today] = {
                'trades': 0,
                'wins': 0,
                'total_pnl': 0.0,
                'trades_list': []
            }
        
        day_stats = self.performance_history[strategy][today]
        day_stats['trades'] += 1
        day_stats['total_pnl'] += profit_loss
        day_stats['trades_list'].append({
            'outcome': outcome,
            'pnl': profit_loss,
            'timestamp': datetime.now().isoformat()
        })
        
        if outcome == 'WIN':
            day_stats['wins'] += 1
    
    def calculate_new_allocations(self):
        """
        💰 CAPITAL REINVESTMENT: Reallocate based on performance
        Fixes: No compound allocation - profits not reinvested into winners
        """
        print(f"💰 CALCULATING STRATEGY REALLOCATIONS...")
        
        # Get recent performance (last 3 days)
        recent_days = []
        for i in range(3):
            day = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            recent_days.append(day)
        
        strategy_scores = {}
        
        for strategy in self.strategy_allocations.keys():
            total_trades = 0
            total_wins = 0
            total_pnl = 0.0
            
            # Aggregate recent performance
            for day in recent_days:
                if (strategy in self.performance_history and 
                    day in self.performance_history[strategy]):
                    
                    day_stats = self.performance_history[strategy][day]
                    total_trades += day_stats['trades']
                    total_wins += day_stats['wins']
                    total_pnl += day_stats['total_pnl']
            
            # Calculate metrics
            win_rate = total_wins / max(total_trades, 1)
            avg_pnl = total_pnl / max(total_trades, 1)
            
            # Composite score (win rate + profit factor)
            score = (win_rate * 0.6) + (min(avg_pnl / 20, 1.0) * 0.4)  # Normalize avg_pnl
            
            strategy_scores[strategy] = {
                'trades': total_trades,
                'win_rate': win_rate,
                'avg_pnl': avg_pnl,
                'total_pnl': total_pnl,
                'score': score
            }
            
            print(f"📊 {strategy}:")
            print(f"   Trades: {total_trades}")
            print(f"   Win Rate: {win_rate:.1%}")
            print(f"   Avg P&L: ${avg_pnl:.2f}")
            print(f"   Total P&L: ${total_pnl:.2f}")
            print(f"   Score: {score:.3f}")
        
        # Reallocate based on scores
        if strategy_scores:
            # Sort by score
            sorted_strategies = sorted(strategy_scores.items(), 
                                     key=lambda x: x[1]['score'], reverse=True)
            
            print(f"\n🏆 REALLOCATION DECISIONS:")
            
            for i, (strategy, stats) in enumerate(sorted_strategies):
                current_allocation = self.strategy_allocations[strategy]
                
                if i == 0 and stats['score'] > 0.8:  # Top performer
                    new_allocation = min(current_allocation * 1.3, self.max_allocation)
                    change = "🚀 BOOST TOP PERFORMER"
                elif i < len(sorted_strategies) // 2 and stats['score'] > 0.6:  # Upper half
                    new_allocation = min(current_allocation * 1.1, self.max_allocation)
                    change = "📈 SLIGHT INCREASE"
                elif stats['score'] < 0.3 and stats['trades'] > 5:  # Poor performer
                    new_allocation = max(current_allocation * 0.7, self.min_allocation)
                    change = "📉 REDUCE ALLOCATION"
                else:  # Keep current
                    new_allocation = current_allocation
                    change = "➡️ MAINTAIN"
                
                self.strategy_allocations[strategy] = new_allocation
                
                print(f"   {strategy}: {current_allocation:.2f}x → {new_allocation:.2f}x ({change})")
        
        return self.strategy_allocations

    """Test capital reinvestment engine"""
    engine = CapitalReinvestmentEngine()
    
    # Simulate some performance data
        ('MODEL_A', 'WIN', 25.5),
        ('MODEL_A', 'WIN', 18.2),
        ('MODEL_A', 'LOSS', -12.1),
        ('MODEL_B', 'LOSS', -15.8),
        ('MODEL_B', 'LOSS', -9.3),
        ('MODEL_C', 'WIN', 22.7),
        ('MODEL_C', 'WIN', 31.2),
        ('MODEL_C', 'WIN', 19.8)
    ]
    
        engine.update_strategy_performance(strategy, outcome, pnl)
    
    print("🧪 Testing reinvestment engine:")
    new_allocations = engine.calculate_new_allocations()

if __name__ == "__main__":
