#!/bin/bash
# 🔐 RBOTZILLA SWARM: FIX PEM FORMATTER - CORRECT ED25519 WRAP
# Constitutional PIN: 841921 | Live Trading Only

echo "🔐 PHASE 1: FIXING PEM FORMATTER (NO ASN.1 SLICE POISON)"

# Extract the correct base64 key from credentials
PRIVATE_KEY_B64="s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="

# Create the surgical PEM fix script
cat > fix_format_pem.py << 'EOF'
#!/usr/bin/env python3
"""
🔐 RBOTZILLA PEM SURGICAL REPAIR
Fixes the ED25519 PEM format without ASN.1 structure poisoning
Constitutional PIN: 841921
"""
import base64

# Hard-coded private key from credentials.py (64-byte full key)
private_key_b64 = "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="

# Extract 32-byte seed (CORRECT method - first 32 bytes of decoded)
try:
    full_key = base64.b64decode(private_key_b64)
    seed_32_bytes = full_key[:32]
    
    # Create proper PKCS#8 DER structure for ED25519
    # PKCS#8 ED25519 private key structure:
    # SEQUENCE {
    #   version INTEGER { v1(0) }
    #   SEQUENCE { 1.3.101.112 }  # ED25519 OID
    #   OCTET STRING containing OCTET STRING of 32-byte seed
    # }
    
    pkcs8_prefix = bytes([
        0x30, 0x2e,  # SEQUENCE, 46 bytes
        0x02, 0x01, 0x00,  # INTEGER 0 (version)
        0x30, 0x05,  # SEQUENCE, 5 bytes  
        0x06, 0x03, 0x2b, 0x65, 0x70,  # OID 1.3.101.112 (ED25519)
        0x04, 0x22,  # OCTET STRING, 34 bytes
        0x04, 0x20   # OCTET STRING, 32 bytes (the actual seed)
    ])
    
    # Combine prefix + seed
    pkcs8_der = pkcs8_prefix + seed_32_bytes
    
    # Base64 encode the complete DER structure
    pkcs8_b64 = base64.b64encode(pkcs8_der).decode('ascii')
    
    # Create proper PEM format
    private_pem = f"-----BEGIN PRIVATE KEY-----\n{pkcs8_b64}\n-----END PRIVATE KEY-----"
    
    # Save the corrected PEM
    with open('coinbase_private_fixed.pem', 'w') as f:
        f.write(private_pem)
    
    print("[✅] SURGICAL SUCCESS: PEM formatted correctly (PKCS#8 ED25519)")
    print(f"[📁] Saved to: coinbase_private_fixed.pem")
    print(f"[🔐] Base64 length: {len(pkcs8_b64)} chars")
    print("[🎯] Ready for Coinbase Advanced Trade authentication")
    
    # Also save the seed in hex format for debugging
    seed_hex = seed_32_bytes.hex()
    print(f"[🔍] 32-byte seed (hex): {seed_hex}")
    
except Exception as e:
    print(f"[❌] PEM FORMAT FAILED: {e}")
    exit(1)
EOF

# Execute the PEM fix
python3 fix_format_pem.py

if [ $? -eq 0 ]; then
    echo "[✅] PHASE 1 COMPLETE: PEM formatter surgical strike successful"
    echo "[🔐] File created: coinbase_private_fixed.pem"
else
    echo "[❌] PHASE 1 FAILED: PEM formatting error"
    exit 1
fi
