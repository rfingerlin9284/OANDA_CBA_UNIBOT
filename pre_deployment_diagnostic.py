#!/usr/bin/env python3
"""
📊 RBOTZILLA ELITE 18+18 PRE-DEPLOYMENT DIAGNOSTIC REPORT
Constitutional PIN: 841921
Comprehensive system validation before live deployment
"""

import os
import json
import subprocess
import sys
from datetime import datetime
import logging

class RBOTzillaPreDeploymentDiagnostic:
    def __init__(self):
        self.constitutional_pin = "841921"
        self.base_path = "/home/ing/overlord/wolfpack-lite/oanda_cba_unibot"
        self.report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "constitutional_pin": self.constitutional_pin,
            "system_status": "ANALYZING",
            "critical_errors": [],
            "warnings": [],
            "confirmations": [],
            "deployment_ready": False
        }
        
        # Setup logging
        os.makedirs(f"{self.base_path}/logs", exist_ok=True)
        logging.basicConfig(
            filename=f"{self.base_path}/logs/pre_deployment_diagnostic.log",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def print_header(self):
        """Print diagnostic report header"""
        print("=" * 80)
        print("📊 RBOTZILLA ELITE 18+18 PRE-DEPLOYMENT DIAGNOSTIC REPORT")
        print("=" * 80)
        print(f"🔐 Constitutional PIN: {self.constitutional_pin}")
        print(f"⏰ Analysis Time: {self.report['timestamp']}")
        print(f"📍 Base Path: {self.base_path}")
        print("=" * 80)
        
    def check_critical_files(self):
        """Check for critical system files"""
        print("\n🔍 CRITICAL FILE VERIFICATION")
        print("-" * 50)
        
        critical_files = [
            ("main.py", "Main system launcher"),
            ("credentials.py", "Authentication credentials"),
            ("live_battle_narrator.py", "Live trading narrator"),
            ("config/live_config.json", "Live configuration"),
            ("oanda_ws_stream.py", "Oanda WebSocket handler"),
            ("coinbase_ws_stream.py", "Coinbase WebSocket handler"),
            ("execution_router_oanda.py", "Oanda execution router"),
            ("execution_router_coinbase.py", "Coinbase execution router"),
            ("dual_model_router.py", "AI model router"),
            ("oco_enforcer.py", "OCO order enforcer"),
            ("dashboard_trigger.py", "Dashboard controller")
        ]
        
        for file_path, description in critical_files:
            full_path = os.path.join(self.base_path, file_path)
            if os.path.exists(full_path):
                file_size = os.path.getsize(full_path)
                print(f"✅ {file_path:<30} - {description} ({file_size} bytes)")
                self.report["confirmations"].append(f"✅ {file_path}: Found ({file_size} bytes)")
            else:
                print(f"❌ {file_path:<30} - MISSING: {description}")
                self.report["critical_errors"].append(f"❌ MISSING: {file_path} - {description}")
                
    def check_configuration(self):
        """Validate configuration files"""
        print("\n⚙️ CONFIGURATION VALIDATION")
        print("-" * 50)
        
        # Check live_config.json
        config_path = os.path.join(self.base_path, "config/live_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                # Validate configuration structure
                if "pairs" in config:
                    forex_pairs = len(config["pairs"].get("forex", []))
                    crypto_pairs = len(config["pairs"].get("crypto", []))
                    print(f"✅ Trading Pairs: {forex_pairs} Forex + {crypto_pairs} Crypto = {forex_pairs + crypto_pairs} Total")
                    self.report["confirmations"].append(f"✅ Trading Pairs: {forex_pairs + crypto_pairs} pairs configured")
                else:
                    print("⚠️ Trading pairs not configured")
                    self.report["warnings"].append("⚠️ Trading pairs not configured in live_config.json")
                    
                print(f"✅ Configuration: Valid JSON format")
                self.report["confirmations"].append("✅ Configuration: Valid JSON format")
                
            except json.JSONDecodeError as e:
                print(f"❌ Configuration: Invalid JSON - {e}")
                self.report["critical_errors"].append(f"❌ Configuration: Invalid JSON - {e}")
        else:
            print("❌ Configuration: live_config.json not found")
            self.report["critical_errors"].append("❌ Configuration: live_config.json not found")
            
    def check_credentials(self):
        """Validate credentials and API access"""
        print("\n🔐 CREDENTIALS & API VALIDATION")
        print("-" * 50)
        
        try:
            # Import credentials
            sys.path.append(self.base_path)
            from credentials import WolfpackCredentials
            
            creds = WolfpackCredentials()
            
            # Check Oanda credentials
            if hasattr(creds, 'OANDA_API_KEY') and creds.OANDA_API_KEY:
                key_preview = creds.OANDA_API_KEY[:10] + "..." + creds.OANDA_API_KEY[-10:]
                print(f"✅ Oanda API Key: {key_preview}")
                self.report["confirmations"].append("✅ Oanda API Key: Present")
            else:
                print("❌ Oanda API Key: Missing or empty")
                self.report["critical_errors"].append("❌ Oanda API Key: Missing or empty")
                
            if hasattr(creds, 'OANDA_ACCOUNT_ID') and creds.OANDA_ACCOUNT_ID:
                print(f"✅ Oanda Account ID: {creds.OANDA_ACCOUNT_ID}")
                self.report["confirmations"].append(f"✅ Oanda Account ID: {creds.OANDA_ACCOUNT_ID}")
            else:
                print("❌ Oanda Account ID: Missing")
                self.report["critical_errors"].append("❌ Oanda Account ID: Missing")
                
            # Check Coinbase credentials
            if hasattr(creds, 'COINBASE_API_KEY_ID') and creds.COINBASE_API_KEY_ID:
                print(f"✅ Coinbase API Key: Present")
                self.report["confirmations"].append("✅ Coinbase API Key: Present")
            else:
                print("⚠️ Coinbase API Key: Missing (crypto trading disabled)")
                self.report["warnings"].append("⚠️ Coinbase API Key: Missing (crypto trading disabled)")
                
            # Verify Constitutional PIN
            if hasattr(creds, 'CONSTITUTIONAL_PIN') and creds.CONSTITUTIONAL_PIN == self.constitutional_pin:
                print(f"✅ Constitutional PIN: VERIFIED ({self.constitutional_pin})")
                self.report["confirmations"].append(f"✅ Constitutional PIN: VERIFIED")
            else:
                print(f"❌ Constitutional PIN: MISMATCH or missing")
                self.report["critical_errors"].append("❌ Constitutional PIN: MISMATCH or missing")
                
        except ImportError as e:
            print(f"❌ Credentials Import: Failed - {e}")
            self.report["critical_errors"].append(f"❌ Credentials Import: Failed - {e}")
            
        """Test live API connections"""
        print("\n🌐 API CONNECTION TESTING")
        print("-" * 50)
        
        try:
            import oandapyV20
            from oandapyV20.endpoints.accounts import AccountSummary
            sys.path.append(self.base_path)
            from credentials import WolfpackCredentials
            
            creds = WolfpackCredentials()
            
            # Test Oanda connection
            try:
                api = oandapyV20.API(
                    access_token=creds.OANDA_API_KEY,
                    environment="live"
                )
                
                request = AccountSummary(creds.OANDA_ACCOUNT_ID)
                api.request(request)
                
                # If we get here without exception, API connection works
                print(f"✅ Oanda API: CONNECTED")
                print(f"   � Environment: LIVE")
                print(f"   � Account ID: {creds.OANDA_ACCOUNT_ID}")
                
                self.report["confirmations"].append("✅ Oanda API: Connection successful")
                self.report["confirmations"].append("✅ Oanda API: Live environment verified")
                
                # Note: Full account details available after authentication
                print(f"✅ Account Access: Verified")
                self.report["confirmations"].append("✅ Account Access: Verified")
                    
            except Exception as e:
                print(f"❌ Oanda API: Connection failed - {e}")
                self.report["critical_errors"].append(f"❌ Oanda API: Connection failed - {e}")
                
        except ImportError as e:
            print(f"❌ API Testing: Missing dependencies - {e}")
            self.report["critical_errors"].append(f"❌ API Testing: Missing dependencies - {e}")
            
    def check_log_system(self):
        """Verify logging system"""
        print("\n📝 LOGGING SYSTEM VERIFICATION")
        print("-" * 50)
        
        log_files = [
            ("logs/system_repair.log", "System repair log"),
            ("logs/deep_system_repair.log", "Deep system repair log"),
            ("logs/live_trades.log", "Live trades log"),
            ("logs/ml_predictions.log", "ML predictions log"),
            ("logs/system_health.log", "System health log")
        ]
        
        logs_dir = os.path.join(self.base_path, "logs")
        if os.path.exists(logs_dir):
            print(f"✅ Logs Directory: Present")
            self.report["confirmations"].append("✅ Logs Directory: Present")
            
            for log_file, description in log_files:
                log_path = os.path.join(self.base_path, log_file)
                if os.path.exists(log_path):
                    size = os.path.getsize(log_path)
                    print(f"✅ {log_file:<25} - {description} ({size} bytes)")
                    self.report["confirmations"].append(f"✅ {log_file}: Present ({size} bytes)")
                else:
                    print(f"⚠️ {log_file:<25} - {description} (will be created)")
                    self.report["warnings"].append(f"⚠️ {log_file}: Not found (will be created)")
        else:
            print(f"❌ Logs Directory: Missing")
            self.report["critical_errors"].append("❌ Logs Directory: Missing")
            
    def check_system_dependencies(self):
        """Check system dependencies"""
        print("\n📦 SYSTEM DEPENDENCIES CHECK")
        print("-" * 50)
        
        dependencies = [
            ("python3", "Python interpreter"),
            ("pip3", "Python package manager")
        ]
        
        python_packages = [
            "oandapyV20",
            "flask", 
            "requests",
            "json",
            "pickle",
            "logging"
        ]
        
        # Check system commands
        for cmd, description in dependencies:
            result = subprocess.run(f"which {cmd}", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {cmd:<15} - {description} - {result.stdout.strip()}")
                self.report["confirmations"].append(f"✅ {cmd}: Available")
            else:
                print(f"❌ {cmd:<15} - {description} - NOT FOUND")
                self.report["critical_errors"].append(f"❌ {cmd}: Not found")
                
        # Check Python packages
        print("\n📦 Python Package Verification:")
        for package in python_packages:
            try:
                __import__(package)
                print(f"✅ {package:<15} - Available")
                self.report["confirmations"].append(f"✅ Python package {package}: Available")
            except ImportError:
                print(f"❌ {package:<15} - MISSING")
                self.report["critical_errors"].append(f"❌ Python package {package}: Missing")
                
    def check_live_processes(self):
        """Check for any running processes"""
        print("\n🔄 LIVE PROCESS CHECK")
        print("-" * 50)
        
        process_patterns = [
            ("main.py", "Main trading system"),
            ("live_battle_narrator.py", "Battle narrator"),
            ("dashboard_trigger.py", "Dashboard controller")
        ]
        
        for pattern, description in process_patterns:
            result = subprocess.run(f"pgrep -f {pattern}", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                pids = result.stdout.strip().split('\n')
                print(f"⚠️ {pattern:<25} - {description} - RUNNING (PIDs: {', '.join(pids)})")
                self.report["warnings"].append(f"⚠️ {pattern}: Already running (PIDs: {', '.join(pids)})")
            else:
                print(f"✅ {pattern:<25} - {description} - Not running")
                self.report["confirmations"].append(f"✅ {pattern}: Not running (ready for fresh start)")
                
    def generate_final_report(self):
        """Generate final deployment readiness report"""
        print("\n" + "=" * 80)
        print("📊 FINAL DEPLOYMENT READINESS REPORT")
        print("=" * 80)
        
        # Count issues
        critical_count = len(self.report["critical_errors"])
        warning_count = len(self.report["warnings"])
        confirmation_count = len(self.report["confirmations"])
        
        print(f"✅ CONFIRMATIONS: {confirmation_count}")
        print(f"⚠️ WARNINGS: {warning_count}")
        print(f"❌ CRITICAL ERRORS: {critical_count}")
        
        # Deployment decision
        if critical_count == 0:
            if warning_count == 0:
                self.report["system_status"] = "READY FOR DEPLOYMENT"
                print("\n🚀 DEPLOYMENT STATUS: READY FOR LIVE DEPLOYMENT!")
                print("💥 All systems operational - RBOTzilla Elite 18+18 ready to dominate!")
                self.report["deployment_ready"] = True
            else:
                self.report["system_status"] = "READY WITH WARNINGS"
                print("\n⚠️ DEPLOYMENT STATUS: READY WITH WARNINGS")
                print("🔧 System functional but review warnings before deployment")
                self.report["deployment_ready"] = True
        else:
            self.report["system_status"] = "NOT READY - CRITICAL ISSUES"
            print("\n❌ DEPLOYMENT STATUS: NOT READY - CRITICAL ISSUES FOUND")
            print("🛠️ Fix critical errors before attempting live deployment")
            self.report["deployment_ready"] = False
            
        print("\n📋 DETAILED ISSUES:")
        
        if self.report["critical_errors"]:
            print("\n❌ CRITICAL ERRORS TO FIX:")
            for error in self.report["critical_errors"]:
                print(f"   {error}")
                
        if self.report["warnings"]:
            print("\n⚠️ WARNINGS TO REVIEW:")
            for warning in self.report["warnings"]:
                print(f"   {warning}")
                
        print(f"\n✅ CONFIRMED SYSTEMS ({confirmation_count}):")
        for confirmation in self.report["confirmations"][:10]:  # Show first 10
            print(f"   {confirmation}")
        if confirmation_count > 10:
            print(f"   ... and {confirmation_count - 10} more confirmations")
            
        print("\n" + "=" * 80)
        
        # Save report to JSON
        report_file = os.path.join(self.base_path, "logs/pre_deployment_report.json")
        with open(report_file, 'w') as f:
            json.dump(self.report, f, indent=2)
        print(f"📄 Full report saved to: {report_file}")
        
        return self.report["deployment_ready"]
        
    def run_full_diagnostic(self):
        """Run complete pre-deployment diagnostic"""
        self.print_header()
        self.check_critical_files()
        self.check_configuration()
        self.check_credentials()
        self.check_log_system()
        self.check_system_dependencies()
        self.check_live_processes()
        deployment_ready = self.generate_final_report()
        
        logging.info(f"Pre-deployment diagnostic completed - Ready: {deployment_ready}")
        return deployment_ready

def main():
    """Run the pre-deployment diagnostic"""
    diagnostic = RBOTzillaPreDeploymentDiagnostic()
    ready = diagnostic.run_full_diagnostic()
    
    if ready:
        print("\n🔥 RBOTzilla Elite 18+18: LOCKED AND LOADED FOR LIVE DEPLOYMENT!")
        sys.exit(0)
    else:
        print("\n🛑 RBOTzilla Elite 18+18: Fix critical issues before deployment")
        sys.exit(1)

if __name__ == "__main__":
    main()
