"""
🎯 COINBASE FVG LIVE DASHBOARD
Real-time FVG detection monitoring for Coinbase spot crypto pairs
LIVE TRADING ONLY - NO live_mode/PRACTICE MODE
"""
import json
import time
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

class CoinbaseFVGDashboard:
    def __init__(self):
        self.console = Console()
        self.feed_file = "/home/ing/FOUR_horsemen/ALPHA_FOUR/proto_oanda/wolfpack-lite/dashboards/fvg_feed_coinbase.json"
        self.last_update = None
        
    def load_fvg_data(self):
        try:
            if os.path.exists(self.feed_file):
                with open(self.feed_file, 'r') as f:
                    data = json.load(f)
                    self.last_update = datetime.now().strftime("%H:%M:%S")
                    return data
            else:
                return {"pairs": {}, "last_scan": "No data yet", "active_trades": 0}
        except Exception as e:
            return {"error": f"Failed to load data: {e}"}
    
    def create_dashboard_table(self, data):
        """Create the main FVG monitoring table"""
        
        # Header panel
        header = Panel(
            Text("🎯 COINBASE FVG LIVE SNIPER DASHBOARD 🎯\n💰 SPOT CRYPTO PAIRS - LIVE TRADING ONLY", 
                 style="bold white", justify="center"),
            style="bold blue",
            title="WOLFPACK-LITE",
            border_style="blue"
        )
        
        # Stats panel
        stats_text = Text()
        stats_text.append("🔴 LIVE TRADING MODE - SPOT ONLY\n", style="bold red")
        stats_text.append(f"📊 Last Update: {self.last_update}\n", style="cyan")
        stats_text.append(f"📈 Active Trades: {data.get('active_trades', 0)}\n", style="green")
        stats_text.append(f"🔍 Last Scan: {data.get('last_scan', 'N/A')}\n", style="yellow")
        stats_text.append("💰 Market: Coinbase Advanced Trade (Spot)\n", style="magenta")
        
        stats_panel = Panel(stats_text, title="System Status", border_style="cyan")
        
        # FVG signals table
        table = Table(title="🎯 Live FVG Signals - Crypto Spot", show_header=True, header_style="bold magenta")
        table.add_column("Pair", style="cyan", width=12)
        table.add_column("Direction", style="white", width=10)
        table.add_column("Confidence", style="green", width=10)
        table.add_column("Entry ($)", style="yellow", width=12)
        table.add_column("Stop Loss ($)", style="red", width=12)
        table.add_column("Take Profit ($)", style="green", width=12)
        table.add_column("Status", style="white", width=12)
        table.add_column("Time", style="dim", width=10)
        
        # Add FVG data to table
        pairs_data = data.get('pairs', {})
        if pairs_data:
            for pair, signal_data in pairs_data.items():
                direction = signal_data.get('direction', 'N/A')
                confidence = f"{signal_data.get('confidence', 0):.2f}"
                entry = f"${signal_data.get('entry', 0):.2f}"
                sl = f"${signal_data.get('sl', 0):.2f}"
                tp = f"${signal_data.get('tp', 0):.2f}"
                status = signal_data.get('status', 'Pending')
                timestamp = signal_data.get('time', 'N/A')
                
                # Color coding based on direction and status
                direction_style = "green" if direction == "BUY" else "red" if direction == "SELL" else "white"
                status_style = "green" if status == "ACTIVE" else "yellow" if status == "PENDING" else "red"
                
                table.add_row(
                    pair,
                    f"[{direction_style}]{direction}[/{direction_style}]",
                    confidence,
                    entry,
                    sl,
                    tp,
                    f"[{status_style}]{status}[/{status_style}]",
                    timestamp
                )
        else:
            table.add_row("No signals", "---", "---", "---", "---", "---", "Scanning...", "---")
        
        return header, stats_panel, table
    
    def run_dashboard(self):
        """Run the live updating dashboard"""
        
        def generate_display():
            data = self.load_fvg_data()
            header, stats, table = self.create_dashboard_table(data)
            
            # Create console and render
            console = Console()
            
            # Clear screen and render components
            console.clear()
            console.print(header)
            console.print("")
            console.print(stats)
            console.print("")
            console.print(table)
            console.print("")
            console.print(Panel(
                Text("🚨 WARNING: LIVE SPOT CRYPTO TRADING WITH REAL MONEY 🚨\n"
                     "NO PERPS/MARGIN - SPOT TRADING ONLY\n"
                     "Press Ctrl+C to exit dashboard", 
                     style="bold red", justify="center"),
                style="bold yellow",
                border_style="yellow"
            ))
        
        # Start live dashboard
        try:
            while True:
                generate_display()
                time.sleep(10)  # Refresh every 10 seconds
                    
        except KeyboardInterrupt:
            self.console.print("\n[bold red]🛑 Dashboard stopped by user[/bold red]")
        except Exception as e:
            self.console.print(f"\n[bold red]❌ Dashboard error: {e}[/bold red]")

def main():
    """Launch Coinbase FVG Dashboard"""
    print("🚀 Starting Coinbase FVG Live Dashboard...")
    print("🚨 LIVE SPOT CRYPTO TRADING MODE - MONITORING REAL MONEY TRADES")
    print("💰 Coinbase Advanced Trade (Spot) - NO PERPS/MARGIN")
    print("Press Ctrl+C to stop\n")
    
    dashboard = CoinbaseFVGDashboard()
    dashboard.run_dashboard()

if __name__ == "__main__":
    main()
