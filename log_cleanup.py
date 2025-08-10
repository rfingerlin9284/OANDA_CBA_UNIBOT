#!/usr/bin/env python3
import os
import gzip
import shutil
from datetime import datetime, timedelta

def cleanup_logs():
    log_dir = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/logs"
    
    # Compress logs older than 1 day
    cutoff_time = datetime.now() - timedelta(days=1)
    
    for filename in os.listdir(log_dir):
        if not filename.endswith('.log'):
            continue
        
        filepath = os.path.join(log_dir, filename)
        
        if os.path.getmtime(filepath) < cutoff_time.timestamp():
            # Compress the file
            compressed_name = f"{filename}_{datetime.now().strftime('%Y%m%d')}.gz"
            compressed_path = os.path.join(log_dir, compressed_name)
            
            with open(filepath, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            os.remove(filepath)
            print(f"✅ Compressed and cleaned: {filename}")
    
    # Remove compressed logs older than 30 days
    old_cutoff = datetime.now() - timedelta(days=30)
    
    for filename in os.listdir(log_dir):
        if not filename.endswith('.gz'):
            continue
        
        filepath = os.path.join(log_dir, filename)
        
        if os.path.getmtime(filepath) < old_cutoff.timestamp():
            os.remove(filepath)
            print(f"🗑️ Removed old log: {filename}")

if __name__ == "__main__":
    cleanup_logs()
