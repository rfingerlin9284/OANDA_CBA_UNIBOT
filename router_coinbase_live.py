import os
import subprocess

def dns_auto_heal():
    """Auto-heal DNS by repairing /etc/resolv.conf and locking it."""
    resolv_conf = '/etc/resolv.conf'
    nameserver_line = 'nameserver 8.8.8.8\n'
    try:
        # Overwrite resolv.conf with Google DNS
        with open(resolv_conf, 'w') as f:
            f.write(nameserver_line)
        # Lock the file
        subprocess.run(['chattr', '+i', resolv_conf], check=True)
        print('🔧 DNS auto-heal: /etc/resolv.conf repaired and locked.')
    except Exception as e:
        print(f'❌ DNS auto-heal failed: {e}')

# Run DNS auto-heal on import
dns_auto_heal()

# ...existing router logic for Coinbase should be placed below...
