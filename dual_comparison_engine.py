#!/usr/bin/env python3
# ⚔️ DUAL COMPARISON ENGINE - Swarm vs Monolithic Head-to-Head
import json
import subprocess
import time
import os
from datetime import datetime

class DualComparisonEngine:
    def __init__(self):
        self.results = {
            "swarm_results": {},
            "monolithic_results": {},
            "winner": "",
            "performance_gap": 0.0
        }
    
    def run_comparison(self, duration_minutes=3):
        """Run head-to-head comparison"""
        print(f"\n⚔️ DUAL COMPARISON ENGINE - {duration_minutes} minute battle")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Clear previous results
        
        # Run Monolithic Bot Test
        print(f"\n🏛️ PHASE 1: Running Monolithic Bot...")
        mono_start = time.time()
        mono_duration = time.time() - mono_start
        
        # Analyze existing swarm logs
        print(f"\n🪖 PHASE 2: Analyzing Swarm Bot Performance...")
        
        # Load results
        self._load_results()
        
        # Compare and declare winner
        self._determine_winner()
        
        # Generate comprehensive report
        self._generate_comparison_report()
    
    def _load_results(self):
        """Load results from both bots"""
        try:
                self.results["swarm_results"] = json.load(f)
        except:
            print("[⚠️] Could not load swarm results")
            self.results["swarm_results"] = {"total_trades": 0, "win_rate": 0, "total_pnl": 0}
        
        try:
                self.results["monolithic_results"] = json.load(f)
        except:
            print("[⚠️] Could not load monolithic results")
            self.results["monolithic_results"] = {"total_trades": 0, "win_rate": 0, "total_pnl": 0}
    
    def _determine_winner(self):
        """Determine the winner based on multiple metrics"""
        swarm = self.results["swarm_results"]
        mono = self.results["monolithic_results"]
        
        # Score based on multiple metrics
        swarm_score = (
            swarm.get("total_trades", 0) * 2 +  # Volume bonus
            swarm.get("win_rate", 0) * 1 +      # Win rate
            max(0, swarm.get("total_pnl", 0)) * 0.1  # P&L bonus
        )
        
        mono_score = (
            mono.get("total_trades", 0) * 2 +
            mono.get("win_rate", 0) * 1 +
            max(0, mono.get("total_pnl", 0)) * 0.1
        )
        
        if swarm_score > mono_score:
            self.results["winner"] = "SWARM"
            self.results["performance_gap"] = swarm_score - mono_score
        else:
            self.results["winner"] = "MONOLITHIC"
            self.results["performance_gap"] = mono_score - swarm_score
    
    def _generate_comparison_report(self):
        """Generate comprehensive comparison report"""
        swarm = self.results["swarm_results"]
        mono = self.results["monolithic_results"]
        
        print(f"\n⚔️ DUAL COMPARISON FINAL RESULTS")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"🪖 SWARM BOT:")
        print(f"   Trades: {swarm.get('total_trades', 0)}")
        print(f"   Win Rate: {swarm.get('win_rate', 0):.1f}%")
        print(f"   Total P&L: {swarm.get('total_pnl', 0):.2f}")
        print(f"   Architecture: ⚡ PARALLEL")
        print()
        print(f"🏛️ MONOLITHIC BOT:")
        print(f"   Trades: {mono.get('total_trades', 0)}")
        print(f"   Win Rate: {mono.get('win_rate', 0):.1f}%") 
        print(f"   Total P&L: {mono.get('total_pnl', 0):.2f}")
        print(f"   Architecture: 🐌 SEQUENTIAL")
        print()
        print(f"🏆 WINNER: {self.results['winner']} BOT")
        print(f"📊 Performance Gap: {self.results['performance_gap']:.2f} points")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Save comparison results
        with open("dual_comparison_results.json", "w") as f:
            json.dump(self.results, f, indent=2, default=str)

if __name__ == "__main__":
    engine = DualComparisonEngine()
    engine.run_comparison(duration_minutes=3)
