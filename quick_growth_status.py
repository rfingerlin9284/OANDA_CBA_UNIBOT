#!/usr/bin/env python3
import json
import os
import datetime

def check_growth_status():
    print("🚀 SMART PROFIT GROWTH STATUS")
    print("=" * 40)
    
    # Check overlay PID
    if os.path.exists('data/growth_overlay.pid'):
        with open('data/growth_overlay.pid', 'r') as f:
            pid = f.read().strip()
        
        try:
            os.kill(int(pid), 0)  # Check if process exists
            print(f"✅ Growth overlay running (PID: {pid})")
        except OSError:
            print(f"❌ Growth overlay stopped (PID: {pid})")
    else:
        print("❌ No growth overlay PID found")
    
    # Check daily P&L
    if os.path.exists('data/daily_pnl.json'):
        with open('data/daily_pnl.json', 'r') as f:
            pnl_data = json.load(f)
        
        current = pnl_data.get('current_daily_pnl', 0)
        target = pnl_data.get('target_daily_pnl', 400)
        progress = (current / target * 100) if target > 0 else 0
        
        print(f"💰 Daily P&L: ${current:.2f} / ${target:.2f} ({progress:.1f}%)")
    
    # Check positions
    if os.path.exists('data/current_positions.json'):
        with open('data/current_positions.json', 'r') as f:
            pos_data = json.load(f)
        
        positions = pos_data.get('positions', [])
        print(f"📊 Active positions: {len(positions)}")
        
        for pos in positions:
            pair = pos.get('instrument', 'Unknown')
            units = pos.get('units', 0)
            pnl = pos.get('unrealizedPL', 0)
            print(f"   {pair}: {units} units, ${pnl:.2f} P&L")
    
    # Check recent activity
    if os.path.exists('logs/growth_overlay.log'):
        print("\n📋 Recent activity:")
        with open('logs/growth_overlay.log', 'r') as f:
            lines = f.readlines()
        
        for line in lines[-3:]:
            print(f"   {line.strip()}")

if __name__ == "__main__":
    check_growth_status()
