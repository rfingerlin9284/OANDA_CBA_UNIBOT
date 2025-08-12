#!/usr/bin/env python3
"""
VS CODE CHANGE GUARDIAN - IMMEDIATE PROTECTION
Detects and prevents unauthorized VS Code modifications to trading system
CRITICAL: Protects real money trading system from silent alterations
"""

import hashlib
import time
import json
import subprocess
import shutil
from pathlib import Path
import logging
from datetime import datetime

class VSCodeChangeGuardian:
    def __init__(self):
        self.protected_files = [
            "hardcoded_live_trading.py",
            "trade_guardian.py",
            "oco_guard.py", 
            "sl_immutability_guardian.py",
            "mandatory_oco_enforcer.py",
            "live_position_manager.py",
            "consolidate_positions.py",
            "executor.py",
            "capital_manager.py",
            ".env.live",
            "config/oco_policy.env"
        ]
        
        self.baseline_file = "vscode_baseline.json"
        self.violation_log = "vscode_violations.log"
        self.backup_dir = Path("vscode_backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - GUARDIAN - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.violation_log),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize baseline
        self.load_or_create_baseline()
        
    def calculate_file_hash(self, file_path):
        """Calculate SHA256 hash of file"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            self.logger.error(f"Error hashing {file_path}: {e}")
            return None
            
    def load_or_create_baseline(self):
        """Load existing baseline or create new one"""
        if Path(self.baseline_file).exists():
            with open(self.baseline_file, 'r') as f:
                self.file_hashes = json.load(f)
            self.logger.info("Loaded existing baseline hashes")
        else:
            self.create_baseline()
            
    def create_baseline(self):
        """Create baseline hashes for all protected files"""
        self.file_hashes = {}
        
        for file_path in self.protected_files:
            if Path(file_path).exists():
                file_hash = self.calculate_file_hash(file_path)
                if file_hash:
                    self.file_hashes[file_path] = {
                        "hash": file_hash,
                        "last_authorized": datetime.now().isoformat(),
                        "size": Path(file_path).stat().st_size
                    }
                    
        self.save_baseline()
        self.logger.info(f"Created baseline for {len(self.file_hashes)} protected files")
        
    def save_baseline(self):
        """Save current baseline to file"""
        with open(self.baseline_file, 'w') as f:
            json.dump(self.file_hashes, f, indent=2)
            
    def detect_changes(self):
        """Detect any changes to protected files"""
        violations = []
        
        for file_path in self.protected_files:
            if not Path(file_path).exists():
                if file_path in self.file_hashes:
                    violations.append({
                        "type": "FILE_DELETED",
                        "file": file_path,
                        "severity": "CRITICAL",
                        "timestamp": datetime.now().isoformat()
                    })
                continue
                
            current_hash = self.calculate_file_hash(file_path)
            if not current_hash:
                continue
                
            baseline_data = self.file_hashes.get(file_path)
            if not baseline_data:
                # New file detected
                violations.append({
                    "type": "NEW_FILE",
                    "file": file_path,
                    "severity": "HIGH",
                    "timestamp": datetime.now().isoformat(),
                    "current_hash": current_hash
                })
                continue
                
            if current_hash != baseline_data["hash"]:
                # File modified
                violations.append({
                    "type": "FILE_MODIFIED", 
                    "file": file_path,
                    "severity": "CRITICAL",
                    "timestamp": datetime.now().isoformat(),
                    "original_hash": baseline_data["hash"],
                    "current_hash": current_hash,
                    "last_authorized": baseline_data.get("last_authorized", "Unknown")
                })
                
        return violations
        
    def handle_violations(self, violations):
        """Handle detected violations"""
        for violation in violations:
            self.logger.critical(f"🚨 VIOLATION DETECTED: {violation}")
            
            if violation["type"] == "FILE_MODIFIED":
                self.handle_file_modification(violation)
            elif violation["type"] == "FILE_DELETED":
                self.handle_file_deletion(violation)
            elif violation["type"] == "NEW_FILE":
                self.handle_new_file(violation)
                
    def handle_file_modification(self, violation):
        """Handle unauthorized file modification"""
        file_path = violation["file"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Create backup of modified file
        backup_path = self.backup_dir / f"{Path(file_path).name}.modified.{timestamp}"
        try:
            shutil.copy2(file_path, backup_path)
            self.logger.info(f"Backed up modified file to {backup_path}")
        except Exception as e:
            self.logger.error(f"Failed to backup {file_path}: {e}")
            
        # 2. Attempt to restore from git
        if self.restore_from_git(file_path):
            self.logger.info(f"✅ Restored {file_path} from git")
            # Update baseline
            new_hash = self.calculate_file_hash(file_path)
            if new_hash:
                self.file_hashes[file_path]["hash"] = new_hash
                self.save_baseline()
        else:
            # 3. CRITICAL ALERT - Manual intervention needed
            self.trigger_critical_alert(violation)
            
    def restore_from_git(self, file_path):
        """Attempt to restore file from git"""
        try:
            result = subprocess.run(
                ["git", "checkout", "HEAD", "--", file_path],
                capture_output=True,
                text=True,
                cwd=Path.cwd()
            )
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Git restore failed for {file_path}: {e}")
            return False
            
    def trigger_critical_alert(self, violation):
        """Trigger critical alert for manual intervention"""
        alert_message = f"""
🚨🚨🚨 CRITICAL SYSTEM VIOLATION 🚨🚨🚨

File: {violation['file']}
Type: {violation['type']} 
Time: {violation['timestamp']}
Severity: {violation['severity']}

UNAUTHORIZED CHANGE DETECTED IN LIVE TRADING SYSTEM!

Manual intervention required immediately.
Trading operations may be compromised.

Action required:
1. Review changes in backup file
2. Verify trading system integrity  
3. Update baseline if changes are authorized
4. Investigate source of unauthorized modification

🚨🚨🚨 END CRITICAL ALERT 🚨🚨🚨
"""
        
        # Log critical alert
        self.logger.critical(alert_message)
        
        # Write to emergency alert file
        with open("CRITICAL_VIOLATION_ALERT.txt", "w") as f:
            f.write(alert_message)
            
        # Attempt to send notification (if configured)
        self.send_emergency_notification(alert_message)
        
    def send_emergency_notification(self, message):
        """Send emergency notification (implement your preferred method)"""
        # Could implement:
        # - Email notification
        # - Slack/Discord webhook
        # - System notification
        # - SMS alert
        pass
        
    def authorize_current_changes(self):
        """Manually authorize current file states as new baseline"""
        print("🔐 AUTHORIZING CURRENT FILE STATES AS NEW BASELINE")
        print("This will update the baseline to match current file states.")
        print("Only do this if you have manually verified all changes are legitimate.")
        
        confirm = input("Type 'AUTHORIZE' to confirm: ").strip()
        if confirm != "AUTHORIZE":
            print("❌ Authorization cancelled")
            return False
            
        # Update baseline to current state
        old_count = len(self.file_hashes)
        self.create_baseline()
        new_count = len(self.file_hashes)
        
        print(f"✅ Baseline updated: {old_count} -> {new_count} files")
        self.logger.info("Manual authorization: Baseline updated to current state")
        return True
        
    def monitor_continuously(self, check_interval=5):
        """Continuously monitor for changes"""
        self.logger.info(f"🛡️ Starting continuous monitoring (interval: {check_interval}s)")
        
        try:
            while True:
                violations = self.detect_changes()
                if violations:
                    self.handle_violations(violations)
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("👋 Monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"Monitoring error: {e}")
            
    def status_report(self):
        """Generate status report"""
        print("\n🛡️ VS CODE CHANGE GUARDIAN STATUS REPORT")
        print("=" * 50)
        print(f"Protected Files: {len(self.protected_files)}")
        print(f"Baseline Entries: {len(self.file_hashes)}")
        print(f"Baseline File: {self.baseline_file}")
        print(f"Violations Log: {self.violation_log}")
        print(f"Backup Directory: {self.backup_dir}")
        
        # Check current status
        violations = self.detect_changes()
        if violations:
            print(f"\n🚨 ACTIVE VIOLATIONS: {len(violations)}")
            for v in violations:
                print(f"  - {v['type']}: {v['file']} ({v['severity']})")
        else:
            print("\n✅ ALL FILES SECURE - NO VIOLATIONS DETECTED")
            
        print("=" * 50)

def main():
    import sys
    
    guardian = VSCodeChangeGuardian()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "monitor":
            guardian.monitor_continuously()
        elif command == "check":
            violations = guardian.detect_changes()
            if violations:
                guardian.handle_violations(violations)
                sys.exit(1)  # Exit with error if violations found
            else:
                print("✅ No violations detected")
                sys.exit(0)
        elif command == "status":
            guardian.status_report()
        elif command == "authorize":
            guardian.authorize_current_changes()
        elif command == "baseline":
            guardian.create_baseline()
            print("✅ New baseline created")
        else:
            print("Usage: python vscode_change_guardian.py [monitor|check|status|authorize|baseline]")
    else:
        # Default: show status and start monitoring
        guardian.status_report()
        print("\nStarting continuous monitoring...")
        guardian.monitor_continuously()

if __name__ == "__main__":
    main()
