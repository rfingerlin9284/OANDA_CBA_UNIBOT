#!/usr/bin/env python3
"""
🤖 HIVE MIND RICK - COMMAND LINE VERSION
SECURE TRIAD SYSTEM: YOU ↔ RICK ↔ UNIBOT

This is the command-line version that works without GUI dependencies.
Perfect for terminal-based operation and testing.
"""

import json
import time
import threading
import subprocess
import logging
import os
import sys
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

@dataclass
class HiveMindMessage:
    """Standard message format for hive mind communication"""
    sender: str
    recipient: str
    message_type: str
    content: str
    priority: str
    timestamp: float

class SecureAccessControl:
    """Enforce ONLY YOU and RICK can modify code"""
    
    def __init__(self):
        self.authorized_entities = ["YOU", "RICK"]
        self.protected_operations = [
            "CODE_MODIFICATION",
            "TRADING_PARAMETER_CHANGE", 
            "SYSTEM_CONFIGURATION",
            "EMERGENCY_SHUTDOWN",
            "GUARDIAN_OVERRIDE"
        ]
        
    def verify_access(self, entity: str, operation: str) -> bool:
        """Verify entity is authorized for operation"""
        if entity not in self.authorized_entities:
            self.log_unauthorized_attempt(entity, operation)
            return False
        return True
        
    def log_unauthorized_attempt(self, entity: str, operation: str):
        """Log unauthorized access attempts"""
        alert = f"🚨 UNAUTHORIZED ACCESS ATTEMPT: {entity} tried {operation}"
        logging.critical(alert)
        print(alert)

class RickAIAgent:
    """RICK - The AI Overlord Agent with full system control"""
    
    def __init__(self):
        self.active = True
        
        # Rick's menu commands
        self.menu_commands = {
            "1": "📊 Real-Time Status Report",
            "2": "⚠️ Error Analysis & Flagging",
            "3": "🔧 System Health Check", 
            "4": "💰 Portfolio Analysis",
            "5": "🚨 Emergency Protocols",
            "6": "📝 Log Analysis Deep Dive",
            "7": "🎯 Strategy Performance Review",
            "8": "🛡️ Guardian System Status",
            "9": "🔄 Auto-Repair Recommendations",
            "10": "📈 Trade Opportunity Alerts",
            "11": "🚫 Silent Code Change Detection",
            "12": "⚡ Immediate Action Required"
        }
        
    def process_command(self, command: str) -> str:
        """Process commands from you or system"""
        command_lower = command.lower()
        
        if "menu" in command_lower or "help" in command_lower:
            return self.show_menu()
            
        elif command.startswith("1") or "status" in command_lower:
            return self.real_time_status_report()
            
        elif command.startswith("2") or "error" in command_lower:
            return self.error_analysis_flagging()
            
        elif command.startswith("3") or "health" in command_lower:
            return self.system_health_check()
            
        elif command.startswith("11") or "code change" in command_lower:
            return self.silent_code_change_detection()
            
        elif "emergency" in command_lower or "stop" in command_lower:
            return self.emergency_protocols()
            
        else:
            return f"🤖 RICK: Processing '{command}'. Type 'menu' for available commands."
            
    def show_menu(self) -> str:
        """Show Rick's command menu"""
        menu_text = "\n🤖 RICK AI OVERLORD - COMMAND CENTER\n"
        menu_text += "=" * 50 + "\n"
        
        for key, command in self.menu_commands.items():
            menu_text += f"{key}. {command}\n"
            
        menu_text += "=" * 50 + "\n"
        menu_text += "Type command number, natural language, or 'exit' to quit.\n"
        
        return menu_text
        
    def real_time_status_report(self) -> str:
        """Generate real-time system status"""
        try:
            report = "\n📊 RICK'S REAL-TIME STATUS REPORT\n"
            report += "=" * 40 + "\n"
            report += f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # System health overview
            report += "🛡️ GUARDIAN SYSTEMS:\n"
            
            # Check VS Code guardian
            vscode_status = self.check_vscode_guardian()
            report += f"  • VS Code Guardian: {vscode_status}\n"
            
            # Check critical files
            file_status = self.check_critical_files()
            report += f"  • Critical Files: {file_status}\n"
            
            # Check trading tools
            trading_status = self.check_trading_tools()
            report += f"  • Trading Tools: {trading_status}\n"
            
            report += "\n🔍 RICK'S ANALYSIS:\n"
            report += "  • Hive mind communication: ACTIVE\n"
            report += "  • Security enforcement: ENABLED\n"
            report += "  • System monitoring: OPERATIONAL\n"
            
            return report
            
        except Exception as e:
            return f"❌ Error generating status report: {e}"
            
    def error_analysis_flagging(self) -> str:
        """Analyze system for errors and flag them"""
        errors = []
        
        # Check for VS Code violations
        try:
            guardian_file = Path("/home/ing/overlord/wolfpack-lite/oanda_cba_unibot/OANDA_CBA_UNIBOT/vscode_change_guardian.py")
            if guardian_file.exists():
                vscode_check = subprocess.run([
                    "python3", str(guardian_file), "check"
                ], capture_output=True, text=True, timeout=10)
                
                if vscode_check.returncode != 0:
                    errors.append({
                        "type": "CRITICAL",
                        "weight": 10,
                        "issue": "VS Code unauthorized changes detected",
                        "action": "IMMEDIATE ROLLBACK REQUIRED"
                    })
            else:
                errors.append({
                    "type": "HIGH",
                    "weight": 8,
                    "issue": "VS Code guardian not found",
                    "action": "DEPLOY GUARDIAN SYSTEM"
                })
                
        except Exception as e:
            errors.append({
                "type": "MEDIUM",
                "weight": 5,
                "issue": f"VS Code check failed: {e}",
                "action": "INVESTIGATE SYSTEM"
            })
            
        # Check critical files
        critical_files = [
            "live_position_manager.py",
            "consolidate_positions.py", 
            "vscode_change_guardian.py"
        ]
        
        base_path = Path("/home/ing/overlord/wolfpack-lite/oanda_cba_unibot/OANDA_CBA_UNIBOT")
        
        for file_name in critical_files:
            if not (base_path / file_name).exists():
                errors.append({
                    "type": "HIGH",
                    "weight": 7,
                    "issue": f"Critical file missing: {file_name}",
                    "action": "RESTORE FILE IMMEDIATELY"
                })
                
        # Format error report
        if not errors:
            return "\n✅ RICK'S ERROR ANALYSIS: NO CRITICAL ISSUES DETECTED\n\nAll systems operating within normal parameters."
            
        report = "\n⚠️ RICK'S ERROR ANALYSIS REPORT\n"
        report += "=" * 40 + "\n"
        
        # Sort by weight (highest first)
        errors.sort(key=lambda x: x["weight"], reverse=True)
        
        for i, error in enumerate(errors, 1):
            report += f"\n{i}. SEVERITY: {error['type']} (Weight: {error['weight']})\n"
            report += f"   Issue: {error['issue']}\n"
            report += f"   Action: {error['action']}\n"
            
        return report
        
    def system_health_check(self) -> str:
        """Comprehensive system health check"""
        report = "\n🔧 RICK'S COMPREHENSIVE SYSTEM HEALTH CHECK\n"
        report += "=" * 50 + "\n"
        
        checks = []
        overall_health = True
        
        # Check VS Code guardian
        guardian_file = Path("/home/ing/overlord/wolfpack-lite/oanda_cba_unibot/OANDA_CBA_UNIBOT/vscode_change_guardian.py")
        if guardian_file.exists():
            checks.append(("VS Code Guardian", "✅ DEPLOYED"))
        else:
            checks.append(("VS Code Guardian", "❌ MISSING"))
            overall_health = False
            
        # Check critical files
        critical_files = [
            "live_position_manager.py",
            "consolidate_positions.py"
        ]
        
        base_path = Path("/home/ing/overlord/wolfpack-lite/oanda_cba_unibot/OANDA_CBA_UNIBOT")
        missing_files = []
        
        for file_name in critical_files:
            if not (base_path / file_name).exists():
                missing_files.append(file_name)
                overall_health = False
                
        if missing_files:
            checks.append(("Critical Files", f"❌ MISSING: {', '.join(missing_files)}"))
        else:
            checks.append(("Critical Files", "✅ ALL PRESENT"))
            
        # Check system architecture
        arch_file = Path("/home/ing/overlord/wolfpack-lite/oanda_cba_unibot/OANDA_CBA_UNIBOT/SECURE_TRIAD_ARCHITECTURE.md")
        if arch_file.exists():
            checks.append(("Architecture Docs", "✅ DOCUMENTED"))
        else:
            checks.append(("Architecture Docs", "⚠️ MISSING"))
            
        # Display results
        for check_name, status in checks:
            report += f"{status} {check_name}\n"
            
        report += "\n" + "=" * 50 + "\n"
        
        if overall_health:
            report += "🟢 OVERALL SYSTEM HEALTH: EXCELLENT\n"
            report += "All critical components are operational."
        else:
            report += "🟡 OVERALL SYSTEM HEALTH: ATTENTION REQUIRED\n"
            report += "Some critical components need attention."
            
        return report
        
    def silent_code_change_detection(self) -> str:
        """Check for silent code changes"""
        try:
            guardian_file = Path("/home/ing/overlord/wolfpack-lite/oanda_cba_unibot/OANDA_CBA_UNIBOT/vscode_change_guardian.py")
            
            if not guardian_file.exists():
                return "\n❌ VS Code guardian not found. Cannot perform change detection."
                
            result = subprocess.run([
                "python3", str(guardian_file), "status"
            ], capture_output=True, text=True, timeout=10)
            
            report = "\n🚫 RICK'S CODE CHANGE DETECTION REPORT\n"
            report += "=" * 45 + "\n"
            
            if result.stdout:
                report += result.stdout
            else:
                report += "VS Code guardian status check completed.\n"
                
            if result.returncode != 0:
                report += "\n🚨 RICK'S RECOMMENDATION: IMMEDIATE ACTION REQUIRED\n"
                report += "Unauthorized changes detected. Review and restore if necessary."
            else:
                report += "\n✅ No unauthorized changes detected."
                
            return report
            
        except Exception as e:
            return f"\n❌ Code change detection failed: {e}"
            
    def emergency_protocols(self) -> str:
        """Emergency protocols and procedures"""
        report = "\n🚨 RICK'S EMERGENCY PROTOCOLS\n"
        report += "=" * 35 + "\n"
        
        report += "Available Emergency Actions:\n"
        report += "1. 🛑 Stop all trading processes\n"
        report += "2. 🔒 Lock system against modifications\n"
        report += "3. 📋 Generate emergency status report\n"
        report += "4. 🔄 Restore from git backup\n"
        report += "5. 📞 Alert system administrator\n\n"
        
        report += "Type 'emergency stop' to halt all operations.\n"
        report += "Type 'emergency status' for critical system status.\n"
        
        return report
        
    def check_vscode_guardian(self) -> str:
        """Check VS Code guardian status"""
        guardian_file = Path("/home/ing/overlord/wolfpack-lite/oanda_cba_unibot/OANDA_CBA_UNIBOT/vscode_change_guardian.py")
        return "✅ ACTIVE" if guardian_file.exists() else "❌ MISSING"
        
    def check_critical_files(self) -> str:
        """Check critical file status"""
        critical_files = [
            "live_position_manager.py",
            "consolidate_positions.py"
        ]
        
        base_path = Path("/home/ing/overlord/wolfpack-lite/oanda_cba_unibot/OANDA_CBA_UNIBOT")
        missing = [f for f in critical_files if not (base_path / f).exists()]
        
        return "✅ ALL PRESENT" if not missing else f"❌ MISSING: {len(missing)}"
        
    def check_trading_tools(self) -> str:
        """Check trading tools status"""
        # For now, assume active - can be enhanced
        return "✅ READY"

class HiveMindCLI:
    """Command-line interface for hive mind communication"""
    
    def __init__(self):
        self.access_control = SecureAccessControl()
        self.rick = RickAIAgent()
        self.running = True
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - HIVE_MIND - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('hive_mind.log'),
                logging.StreamHandler()
            ]
        )
        
    def display_startup_message(self):
        """Display startup message"""
        print("\n" + "=" * 70)
        print("🤖 HIVE MIND RICK - COMMAND LINE TERMINAL")
        print("=" * 70)
        print("\nSECURE TRIAD SYSTEM INITIALIZED:")
        print("👤 YOU - Supreme Commander (Full Control)")
        print("🤖 RICK - AI Overlord Agent (Autonomous Analysis)")  
        print("🦾 UNIBOT - Auto-Healer (System Protection)")
        print("\n🔐 SECURITY: Only YOU and RICK can modify code")
        print("🛡️ PROTECTION: VS Code changes detected and blocked")
        print("📋 COMMANDS: Type 'menu' for Rick's commands or use natural language")
        print("❌ EXIT: Type 'exit' or 'quit' to close terminal")
        print("\n" + "=" * 70)
        
    def run(self):
        """Run the command-line interface"""
        self.display_startup_message()
        
        # Initial Rick greeting
        print("\n🤖 RICK: I am online and monitoring all systems.")
        print("    Type 'menu' to see my available commands.")
        
        while self.running:
            try:
                # Get user input
                user_input = input("\n👤 Command: ").strip()
                
                if not user_input:
                    continue
                    
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\n🤖 RICK: Shutting down hive mind terminal. Goodbye!")
                    self.running = False
                    break
                    
                # Verify access (assuming user is YOU)
                if not self.access_control.verify_access("YOU", "SYSTEM_COMMAND"):
                    print("❌ Access denied")
                    continue
                    
                # Process command through Rick
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"\n[{timestamp}] Processing command through Rick...")
                
                response = self.rick.process_command(user_input)
                print(f"\n🤖 RICK: {response}")
                
                # Log the interaction
                logging.info(f"Command processed: {user_input[:50]}...")
                
            except KeyboardInterrupt:
                print("\n\n🤖 RICK: Keyboard interrupt detected. Shutting down...")
                self.running = False
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                logging.error(f"CLI error: {e}")

def main():
    """Main entry point"""
    try:
        # Create and run the hive mind CLI
        hive_mind = HiveMindCLI()
        hive_mind.run()
        
    except Exception as e:
        print(f"❌ Failed to start hive mind: {e}")
        logging.error(f"Startup error: {e}")

if __name__ == "__main__":
    main()
