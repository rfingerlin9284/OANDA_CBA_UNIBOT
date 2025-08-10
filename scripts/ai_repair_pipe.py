#!/usr/bin/env python3
"""
🛠️ AI REPAIR PIPE - Auto-diagnosis and code repair system
Integrates with GPT/Claude for autonomous system recovery
"""

import os
import json
import subprocess
import hashlib
import ast
from datetime import datetime
import traceback

class AIRepairPipe:
    """AI-powered system repair and recovery"""
    
    def __init__(self):
        self.repair_log = "logs/errors/repair_report.json"
        self.allowed_repairs = [
            "syntax_error",
            "import_error", 
            "model_loading_error",
            "json_serialization_error",
            "feature_mismatch_error"
        ]
        self.repair_history = []
        
    def detect_system_errors(self):
        """Scan system for common error patterns"""
        errors_found = []
        
        # Check ML model loading
        if not self._check_ml_models():
            errors_found.append({
                'type': 'model_loading_error',
                'file': 'models/',
                'description': 'ML models missing or corrupted'
            })
        
        # Check syntax of critical files
        critical_files = [
            'scripts/ml_hybrid_engine.py',
            'scripts/orderbook_fusion.py'
        ]
        
        for file_path in critical_files:
            if os.path.exists(file_path):
                syntax_ok = self._check_syntax(file_path)
                if not syntax_ok:
                    errors_found.append({
                        'type': 'syntax_error',
                        'file': file_path,
                        'description': f'Syntax error in {file_path}'
                    })
        
        return errors_found
    
    def _check_ml_models(self):
        """Verify ML models exist and are valid"""
        for model_path in models:
            if not os.path.exists(model_path):
                return False
            if os.path.getsize(model_path) < 1000:  # Too small to be real model
                return False
        return True
    
    def _check_syntax(self, file_path):
        """Check Python file for syntax errors"""
        try:
            with open(file_path, 'r') as f:
                source_code = f.read()
            ast.parse(source_code)
            return True
        except SyntaxError:
            return False
        except Exception:
            return False
    
    def generate_repair_suggestion(self, error_info):
        """Generate AI repair suggestion based on error type"""
        repair_suggestions = {
            'model_loading_error': """
# AI REPAIR SUGGESTION: Recreate ML Models
python3 scripts/train_light_model.py
python3 scripts/quick_heavy_model.py
""",
            'syntax_error': """
# AI REPAIR SUGGESTION: Check file for common syntax issues
# - Missing colons after if/for/while statements
# - Unmatched parentheses or brackets
# - Incorrect indentation
# - Missing quotes or string terminators
""",
            'json_serialization_error': """
# AI REPAIR SUGGESTION: Convert numpy types to native Python
# Replace: np.float64(value) with float(value)
# Replace: np.int64(value) with int(value)
# Ensure all JSON values are serializable
"""
        }
        
        return repair_suggestions.get(error_info['type'], "No automated repair available")
    
    def execute_safe_repair(self, error_info):
        """Execute safe, pre-approved repairs only"""
        if error_info['type'] not in self.allowed_repairs:
            return False, "Repair type not in allowed list"
        
        try:
            if error_info['type'] == 'model_loading_error':
                # Recreate models
                result1 = subprocess.run(['python3', 'scripts/train_light_model.py'], 
                                       capture_output=True, text=True)
                result2 = subprocess.run(['python3', 'scripts/quick_heavy_model.py'], 
                                       capture_output=True, text=True)
                
                if result1.returncode == 0 and result2.returncode == 0:
                    return True, "ML models successfully recreated"
                else:
                    return False, f"Model creation failed: {result1.stderr} {result2.stderr}"
            
            return False, "No automated repair implemented for this error type"
            
        except Exception as e:
            return False, f"Repair execution failed: {str(e)}"
    
    def log_repair_action(self, error_info, repair_result, repair_success):
        """Log all repair actions for audit"""
        os.makedirs(os.path.dirname(self.repair_log), exist_ok=True)
        
        repair_entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': error_info['type'],
            'error_file': error_info['file'],
            'error_description': error_info['description'],
            'repair_attempted': True,
            'repair_success': repair_success,
            'repair_result': repair_result,
            'system_hash': self._get_system_hash()
        }
        
        self.repair_history.append(repair_entry)
        
        # Save to file
        with open(self.repair_log, 'w') as f:
            json.dump(self.repair_history[-20:], f, indent=2)  # Keep last 20 repairs
    
    def _get_system_hash(self):
        """Generate hash of critical system files for integrity check"""
        critical_files = [
            'scripts/ml_hybrid_engine.py',
            'config.json'
        ]
        
        combined_content = ""
        for file_path in critical_files:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    combined_content += f.read()
        
        return hashlib.md5(combined_content.encode()).hexdigest()[:16]
    
    def run_system_check(self):
        """Main system check and repair routine"""
        print("🛠️ AI Repair Pipe - Starting System Check...")
        
        errors = self.detect_system_errors()
        
        if not errors:
            print("✅ No system errors detected")
            return True
        
        print(f"🚨 Found {len(errors)} system errors:")
        for error in errors:
            print(f"  - {error['type']}: {error['description']}")
            
            # Generate repair suggestion
            suggestion = self.generate_repair_suggestion(error)
            print(f"  💡 Repair Suggestion:\n{suggestion}")
            
            # Attempt safe repair if allowed
            if error['type'] in self.allowed_repairs:
                success, result = self.execute_safe_repair(error)
                self.log_repair_action(error, result, success)
                
                if success:
                    print(f"  ✅ Repair successful: {result}")
                else:
                    print(f"  ❌ Repair failed: {result}")
            else:
                print(f"  ⚠️ Manual intervention required for {error['type']}")
        
        return len([e for e in errors if e['type'] in self.allowed_repairs]) == 0

if __name__ == "__main__":
    repair_pipe = AIRepairPipe()
    repair_pipe.run_system_check()
