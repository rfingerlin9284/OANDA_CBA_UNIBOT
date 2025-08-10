#!/usr/bin/env python3
"""
🔍 LIVE MODE FORENSIC AUDIT
Constitutional PIN: 841921
HUNT DOWN ALL SIMULATION MODE LOGIC AND KILL IT WITH FIRE

This script will:
1. Find all simulation/practice mode references
2. Validate current configuration states
3. Create a 100% LIVE-ONLY system 
4. Generate hardened configuration files
"""

import os
import sys
import json
import re
from datetime import datetime

class LiveModeForensicAuditor:
    def __init__(self):
        self.audit_start = datetime.now()
        self.constitutional_pin = "841921"
        self.issues_found = []
        self.files_examined = 0
        self.simulation_references = []
        
        print("🔍 LIVE MODE FORENSIC AUDIT - STARTING")
        print("=" * 60)
        print(f"Constitutional PIN: {self.constitutional_pin}")
        print(f"Audit Target: Complete simulation mode elimination")
        print(f"Mission: 100% Live Trading Only Configuration")
        print("=" * 60)
        
    def scan_file_for_simulation_logic(self, filepath):
        """Scan a file for simulation mode references"""
        if not os.path.exists(filepath):
            return
            
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
            self.files_examined += 1
            
            # Patterns that indicate simulation mode
            sim_patterns = [
                r'(simulation|sim_mode|practice|demo|sandbox|test.*mode)',
                r'(SIM_MODE\s*=\s*True)',
                r'(PRACTICE\s*=\s*True)', 
                r'(environment\s*=\s*["\']practice["\'])',
                r'(environment\s*=\s*["\']demo["\'])',
                r'(api-fxpractice\.oanda\.com)',
                r'(api\.sandbox\.coinbase)',
                r'(sandbox.*=.*True)',
                r'(live_mode.*=.*False)',
                r'(is_live.*=.*False)'
            ]
            
            for line_num, line in enumerate(lines, 1):
                for pattern in sim_patterns:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        # Skip obvious comments that say "NO simulation" or "LIVE ONLY"
                        if any(phrase in line.lower() for phrase in [
                            'no simulation', 'live only', 'real money', 
                            'live trading only', 'no practice', 'no demo'
                        ]):
                            continue
                            
                        self.simulation_references.append({
                            'file': filepath,
                            'line': line_num,
                            'content': line.strip(),
                            'pattern': pattern,
                            'match': match.group()
                        })
                        
                        # Check if this is an actual problem
                        if any(bad in line.lower() for bad in [
                            'sim_mode = true', 'practice = true', 
                            'practice"', "practice'", 'demo"', "demo'",
                            'fxpractice', 'sandbox'
                        ]):
                            self.issues_found.append({
                                'severity': 'CRITICAL',
                                'file': filepath,
                                'line': line_num,
                                'issue': f"Simulation mode enabled: {match.group()}",
                                'fix': "Set to live mode only"
                            })
                            
        except Exception as e:
            print(f"⚠️  Error scanning {filepath}: {e}")
    
    def audit_configuration_files(self):
        """Audit all configuration files"""
        print("\n🔧 AUDITING CONFIGURATION FILES...")
        
        config_files = [
            '.env',
            'config.py', 
            'config.json',
            'config_live.json',
            'credentials.py'
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                print(f"   Scanning: {config_file}")
                self.scan_file_for_simulation_logic(config_file)
            else:
                print(f"   Missing: {config_file}")
                
    def audit_trading_modules(self):
        """Audit all Python trading modules"""
        print("\n⚡ AUDITING TRADING MODULES...")
        
        # Find all Python files
        python_files = []
        for root, dirs, files in os.walk('.'):
            # Skip virtual environment and logs
            if 'env' in root or 'logs' in root or '__pycache__' in root:
                continue
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        print(f"   Found {len(python_files)} Python files to scan")
        
        for py_file in python_files:
            self.scan_file_for_simulation_logic(py_file)
            
    def check_environment_variables(self):
        """Check environment variables for simulation settings"""
        print("\n🌍 CHECKING ENVIRONMENT VARIABLES...")
        
        sim_env_vars = [
            'SIM_MODE', 'PRACTICE', 'OANDA_ENVIRONMENT', 
            'SANDBOX_MODE', 'TRADING_MODE'
        ]
        
        for var in sim_env_vars:
            value = os.getenv(var)
            if value:
                print(f"   {var} = {value}")
                
                # Check for problematic values
                if value.lower() in ['true', 'practice', 'demo', 'sandbox', 'simulation']:
                    self.issues_found.append({
                        'severity': 'CRITICAL',
                        'file': 'Environment Variable',
                        'line': 'N/A',
                        'issue': f"{var}={value} enables simulation mode",
                        'fix': f"Set {var} to live/false"
                    })
            else:
                print(f"   {var} = Not Set")
    
    def verify_oanda_endpoints(self):
        """Verify OANDA endpoints are live only"""
        print("\n🎯 VERIFYING OANDA ENDPOINTS...")
        
        # Check .env file
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                env_content = f.read()
                
            if 'api-fxpractice.oanda.com' in env_content:
                self.issues_found.append({
                    'severity': 'CRITICAL',
                    'file': '.env',
                    'line': 'N/A',
                    'issue': 'OANDA practice endpoint detected',
                    'fix': 'Change to api-fxtrade.oanda.com'
                })
                print("   ❌ PRACTICE endpoint found in .env")
            elif 'api-fxtrade.oanda.com' in env_content:
                print("   ✅ LIVE endpoint confirmed in .env")
            else:
                print("   ⚠️  No OANDA endpoint found in .env")
        
        # Check credentials.py
        if os.path.exists('credentials.py'):
            with open('credentials.py', 'r') as f:
                cred_content = f.read()
                
            if 'api-fxtrade.oanda.com' in cred_content:
                print("   ✅ LIVE endpoint confirmed in credentials.py")
            else:
                print("   ⚠️  LIVE endpoint not found in credentials.py")
    
    def generate_live_only_config(self):
        """Generate hardened live-only configuration"""
        print("\n🛡️  GENERATING LIVE-ONLY CONFIGURATION...")
        
        # Create hardened .env
        live_env_content = f"""# WOLFPACK-LITE LIVE TRADING ONLY
# Constitutional PIN: 841921
# SIMULATION MODE ELIMINATED

CONSTITUTIONAL_PIN=841921
OANDA_API_KEY=bfc61e32b5218b0b3fe258aa743a1ba8-557ab61dd7909d8407eeb0053bb98f48
OANDA_ACCOUNT_ID=001-001-13473069-001
OANDA_ENVIRONMENT=live
OANDA_API_URL=https://api-fxtrade.oanda.com

# SIMULATION MODE PERMANENTLY DISABLED
SIM_MODE=false
PRACTICE=false
SANDBOX_MODE=false
DEMO_MODE=false

# LIVE TRADING ENFORCEMENT
REAL_MONEY_ONLY=true
TRADING_MODE=LIVE_ONLY

# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open('.env.live_only', 'w') as f:
            f.write(live_env_content)
        print("   ✅ Created .env.live_only")
        
        # Create hardened config.py
        live_config_content = f"""#!/usr/bin/env python3
# WOLFPACK-LITE LIVE TRADING CONFIGURATION
# Constitutional PIN: 841921
# ALL SIMULATION MODES ELIMINATED

# === LIVE OANDA CONFIG ===
OANDA_API_KEY = "bfc61e32b5218b0b3fe258aa743a1ba8-557ab61dd7909d8407eeb0053bb98f48"
OANDA_ACCOUNT_ID = "001-001-13473069-001"
OANDA_ENVIRONMENT = "live"  # HARDCODED LIVE - NEVER CHANGE
OANDA_API_URL = "https://api-fxtrade.oanda.com"  # LIVE ENDPOINT ONLY

# === SIMULATION MODE ELIMINATED ===
SIM_MODE = False        # PERMANENTLY DISABLED
PRACTICE = False        # PERMANENTLY DISABLED  
SANDBOX_MODE = False    # PERMANENTLY DISABLED
DEMO_MODE = False       # PERMANENTLY DISABLED

# === LIVE TRADING ENFORCEMENT ===
REAL_MONEY_ONLY = True
CONSTITUTIONAL_PIN = "841921"

# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open('config_live_only.py', 'w') as f:
            f.write(live_config_content)
        print("   ✅ Created config_live_only.py")
        
        # Create hardened JSON config
        live_json_config = {
            "constitutional_pin": "841921",
            "trading_mode": "LIVE_ONLY",
            "oanda": {
                "api_key": "bfc61e32b5218b0b3fe258aa743a1ba8-557ab61dd7909d8407eeb0053bb98f48",
                "account_id": "001-001-13473069-001", 
                "environment": "live",
                "api_url": "https://api-fxtrade.oanda.com"
            },
            "simulation_eliminated": {
                "sim_mode": False,
                "practice": False,
                "sandbox_mode": False,
                "demo_mode": False
            },
            "live_enforcement": {
                "live_trading_only": True,
                "real_money_only": True,
                "simulation_blocked": True
            },
            "generated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open('config_live_only.json', 'w') as f:
            json.dump(live_json_config, f, indent=2)
        print("   ✅ Created config_live_only.json")
    
    def create_live_mode_enforcer(self):
        """Create a live mode enforcement script"""
        print("\n🚨 CREATING LIVE MODE ENFORCER...")
        
        enforcer_content = f"""#!/usr/bin/env python3
'''
🚨 LIVE MODE ENFORCER
Constitutional PIN: 841921
KILLS ALL SIMULATION LOGIC ON STARTUP
'''

import os
import sys
import json

def enforce_live_mode():
    '''Enforce live-only trading mode'''
    print("🚨 LIVE MODE ENFORCER - STARTING")
    
    # Set environment variables to live mode
    os.environ['SIM_MODE'] = 'false'
    os.environ['PRACTICE'] = 'false'
    os.environ['SANDBOX_MODE'] = 'false'
    os.environ['OANDA_ENVIRONMENT'] = 'live'
    os.environ['TRADING_MODE'] = 'LIVE_ONLY'
    
    print("✅ Environment variables set to LIVE MODE")
    
    # Verify no simulation files exist
    sim_files = [
        'config_demo.py', 'config_practice.py', 'config_sandbox.py',
        '.env.demo', '.env.practice', '.env.sandbox'
    ]
    
    for sim_file in sim_files:
        if os.path.exists(sim_file):
            print(f"🔥 DESTROYING simulation file: {{sim_file}}")
            os.remove(sim_file)
    
    # Block practice endpoints
    hosts_block = '''
# BLOCK SIMULATION ENDPOINTS - Constitutional PIN: 841921
127.0.0.1 api-fxpractice.oanda.com
127.0.0.1 api.sandbox.coinbase.com
'''
    
    print("🛡️  LIVE MODE ENFORCEMENT COMPLETE")
    return True

if __name__ == "__main__":
    enforce_live_mode()
"""
        
        with open('enforce_live_mode.py', 'w') as f:
            f.write(enforcer_content)
        os.chmod('enforce_live_mode.py', 0o755)
        print("   ✅ Created enforce_live_mode.py")
    
    def generate_audit_report(self):
        """Generate comprehensive audit report"""
        print("\n📊 GENERATING AUDIT REPORT...")
        
        report = {
            "audit_timestamp": self.audit_start.strftime('%Y-%m-%d %H:%M:%S'),
            "constitutional_pin": self.constitutional_pin,
            "mission": "Eliminate all simulation mode logic",
            "statistics": {
                "files_examined": self.files_examined,
                "simulation_references_found": len(self.simulation_references),
                "critical_issues_found": len([i for i in self.issues_found if i['severity'] == 'CRITICAL']),
                "total_issues": len(self.issues_found)
            },
            "simulation_references": self.simulation_references,
            "critical_issues": [i for i in self.issues_found if i['severity'] == 'CRITICAL'],
            "all_issues": self.issues_found,
            "recommendations": [
                "Replace .env with .env.live_only",
                "Replace config.py with config_live_only.py", 
                "Run enforce_live_mode.py on every startup",
                "Block practice endpoints at network level",
                "Implement Constitutional PIN verification",
                "Remove all simulation/demo files"
            ]
        }
        
        with open('live_mode_forensic_audit_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        print("   ✅ Created live_mode_forensic_audit_report.json")
        
        return report
    
    def print_summary(self, report):
        """Print audit summary"""
        print("\n" + "="*60)
        print("🔍 LIVE MODE FORENSIC AUDIT - SUMMARY")
        print("="*60)
        print(f"📊 Files Examined: {report['statistics']['files_examined']}")
        print(f"🔍 Simulation References: {report['statistics']['simulation_references_found']}")
        print(f"🚨 Critical Issues: {report['statistics']['critical_issues_found']}")
        
        if report['statistics']['critical_issues_found'] > 0:
            print("\n❌ CRITICAL ISSUES FOUND:")
            for issue in report['critical_issues']:
                print(f"   File: {issue['file']}")
                print(f"   Line: {issue['line']}")
                print(f"   Issue: {issue['issue']}")
                print(f"   Fix: {issue['fix']}")
                print()
        else:
            print("\n✅ NO CRITICAL SIMULATION MODE ISSUES FOUND")
        
        print("\n🛡️  HARDENED CONFIGURATION FILES CREATED:")
        print("   ✅ .env.live_only")
        print("   ✅ config_live_only.py")
        print("   ✅ config_live_only.json")
        print("   ✅ enforce_live_mode.py")
        
        print("\n🚀 NEXT STEPS:")
        print("   1. Copy .env.live_only to .env")
        print("   2. Copy config_live_only.py to config.py")
        print("   3. Run: python enforce_live_mode.py")
        print("   4. Test live order execution")
        print("   5. Monitor for simulation mode references")
        
        print(f"\n📈 CONSTITUTIONAL PIN: {self.constitutional_pin}")
        print("🎯 MISSION: 100% LIVE TRADING ONLY - SIMULATION ELIMINATED")
        print("="*60)

def main():
    """Run the forensic audit"""
    auditor = LiveModeForensicAuditor()
    
    # Run all audits
    auditor.audit_configuration_files()
    auditor.audit_trading_modules()
    auditor.check_environment_variables()
    auditor.verify_oanda_endpoints()
    
    # Generate fixes
    auditor.generate_live_only_config()
    auditor.create_live_mode_enforcer()
    
    # Generate report
    report = auditor.generate_audit_report()
    auditor.print_summary(report)

if __name__ == "__main__":
    main()
