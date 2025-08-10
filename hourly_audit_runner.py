#!/usr/bin/env python3
"""Hourly Trade Auditor with Enhanced Analytics"""
import json
import time
from datetime import datetime, timedelta

def analyze_trade_performance():
    """
    🕵️ ENHANCED TRADE AUDITOR
    Analyzes recent performance and flags issues
    """
    try:
        # Load recent trades from logs
        today = datetime.now().strftime('%Y%m%d')
        log_file = f'logs/trade_json_{today}.json'
        
        trades = []
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        trades.append(json.loads(line))
        except FileNotFoundError:
            print("[AUDITOR] ⚠️ No trade log found for today")
            return
        
        if not trades:
            print("[AUDITOR] ℹ️ No trades to audit")
            return
        
        print(f"\n[AUDITOR] 📊 ANALYZING {len(trades)} TRADES")
        print("═" * 50)
        
        # Performance metrics
        total_trades = len(trades)
        high_confidence_trades = [t for t in trades if t.get('ml_confidence', 0) > 0.85]
        high_conf_losses = [t for t in high_confidence_trades if 'loss' in t.get('reason', '').lower()]
        
        # Strategy performance
        strategy_performance = {}
        pair_performance = {}
        
        for trade in trades:
            strategy = trade.get('data', {}).get('strategy', 'Unknown')
            pair = trade.get('data', {}).get('instrument', 'Unknown')
            confidence = trade.get('ml_confidence', 0)
            
            # Track strategy stats
            if strategy not in strategy_performance:
                strategy_performance[strategy] = {'count': 0, 'high_conf': 0, 'avg_conf': []}
            
            strategy_performance[strategy]['count'] += 1
            strategy_performance[strategy]['avg_conf'].append(confidence)
            
            if confidence > 0.85:
                strategy_performance[strategy]['high_conf'] += 1
            
            # Track pair stats
            if pair not in pair_performance:
                pair_performance[pair] = {'count': 0, 'high_conf': 0}
            
            pair_performance[pair]['count'] += 1
            if confidence > 0.85:
                pair_performance[pair]['high_conf'] += 1
        
        # Audit results
        issues = []
        
        if len(high_conf_losses) > 0:
            issues.append(f"❗ {len(high_conf_losses)} high-confidence trades lost")
            for trade in high_conf_losses:
                issues.append(f"   - {trade.get('data', {}).get('strategy', 'Unknown')} on {trade.get('data', {}).get('instrument', 'Unknown')}")
        
        # Strategy analysis
        print("📈 STRATEGY PERFORMANCE:")
        for strategy, stats in strategy_performance.items():
            avg_conf = sum(stats['avg_conf']) / len(stats['avg_conf']) if stats['avg_conf'] else 0
            high_conf_rate = (stats['high_conf'] / stats['count']) * 100 if stats['count'] > 0 else 0
            print(f"   {strategy}: {stats['count']} trades, {avg_conf:.1%} avg conf, {high_conf_rate:.1f}% high-conf")
        
        print("\n🌍 PAIR PERFORMANCE:")
        for pair, stats in sorted(pair_performance.items(), key=lambda x: x[1]['count'], reverse=True)[:5]:
            print(f"   {pair}: {stats['count']} trades, {stats['high_conf']} high-confidence")
        
        if issues:
            print(f"\n🚨 AUDIT FINDINGS:")
            for issue in issues:
                print(f"   {issue}")
        else:
            print(f"\n✅ AUDIT PASSED: No critical issues found")
        
        print("═" * 50)
        
        # Log audit results
        with open('logs/audit_results.log', 'a') as f:
            f.write(f"{datetime.now()} - Audited {total_trades} trades, {len(issues)} issues\n")
            for issue in issues:
                f.write(f"   {issue}\n")
        
        return issues
        
    except Exception as e:
        error_msg = f"❌ AUDIT ERROR: {e}"
        print(f"[AUDITOR] {error_msg}")
        return [error_msg]

if __name__ == "__main__":
    analyze_trade_performance()
