#!/bin/bash
# generate_ed25519_key.sh: Generate or fix ED25519 key pair
cat > generate_ed25519_key.py << 'EOF'
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption, PublicFormat
import base64, json
import os

print("🔧 GENERATING ED25519 KEY PAIR FOR COINBASE...")

# Use provided key from credentials
provided_key = "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="

# Try to extract 32-byte seed (first 32 bytes if concatenated)
try:
    key_bytes = base64.b64decode(provided_key)
    print(f"Decoded key length: {len(key_bytes)} bytes")
    
    if len(key_bytes) == 64:
        # Take first 32 bytes as ED25519 seed
        seed = key_bytes[:32]
        print("Using first 32 bytes from 64-byte key")
    elif len(key_bytes) == 32:
        seed = key_bytes
        print("Using 32-byte key directly")
    else:
        raise ValueError(f"Invalid key length: {len(key_bytes)} bytes")
        
    # Create private key from seed
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
    print("✅ ED25519 private key created from provided seed")
    
except Exception as e:
    print(f"[❌] Key decode error: {e}. Generating new key.")
    private_key = ed25519.Ed25519PrivateKey.generate()
    seed = private_key.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())

# Get the raw 32-byte private key
raw_private_bytes = private_key.private_bytes(
    encoding=Encoding.Raw,
    format=PrivateFormat.Raw,
    encryption_algorithm=NoEncryption()
)

# Save raw private key as base64 for API usage
raw_b64 = base64.b64encode(raw_private_bytes).decode('utf-8')
with open('ed25519_raw.key', 'w') as f:
    f.write(raw_b64)

# Save private key as PEM for backup
private_pem = private_key.private_bytes(
    encoding=Encoding.PEM,
    format=PrivateFormat.PKCS8,
    encryption_algorithm=NoEncryption()
)
with open('ed25519_private.pem', 'wb') as f:
    f.write(private_pem)

# Save public key
public_key = private_key.public_key()
public_bytes = public_key.public_bytes(Encoding.Raw, PublicFormat.Raw)
public_pem = public_key.public_bytes(
    encoding=Encoding.PEM,
    format=PublicFormat.SubjectPublicKeyInfo
)
with open('ed25519_public.pem', 'wb') as f:
    f.write(public_pem)

print(f"[✅] ED25519 keys saved:")
print(f"    Raw key (32 bytes): ed25519_raw.key")
print(f"    Private PEM: ed25519_private.pem") 
print(f"    Public PEM: ed25519_public.pem")
print(f"    Raw key base64: {raw_b64}")
EOF

python3 generate_ed25519_key.py
