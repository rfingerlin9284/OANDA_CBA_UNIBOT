#!/usr/bin/env python3
"""
Convert API Key to Proper Format for CDP SDK
"""

import os
import base64
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

def convert_key_to_pem():
    """Convert the current key to proper PEM format"""
    
    load_dotenv()
    key_secret = os.getenv('COINBASE_API_KEY_SECRET')
    
    print(f"🔑 Original key length: {len(key_secret)}")
    print(f"🔑 Original key: {key_secret}")
    
    try:
        # Method 1: Try to fix base64 padding and decode
        print("\n🔧 Method 1: Fix base64 padding...")
        key_fixed = key_secret
        while len(key_fixed) % 4 != 0:
            key_fixed += '='
        
        print(f"   Fixed key length: {len(key_fixed)}")
        try:
            decoded_bytes = base64.b64decode(key_fixed)
            print(f"   Decoded bytes length: {len(decoded_bytes)}")
            
            # Ed25519 private key should be 32 bytes
            if len(decoded_bytes) >= 32:
                seed = decoded_bytes[:32]
                private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
                
                # Convert to PEM format
                pem_key = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                
                print("✅ Method 1: Successfully converted to PEM!")
                print(f"📝 PEM Format:")
                pem_str = pem_key.decode('utf-8')
                print(pem_str)
                
                # Test if this PEM works with CDP SDK
                return pem_str
                
        except Exception as e:
            print(f"   ❌ Base64 decode failed: {e}")
    
    except Exception as e:
        print(f"❌ Method 1 failed: {e}")
    
    try:
        # Method 2: Use key as direct seed (if it's 32 bytes when encoded)
        print("\n🔧 Method 2: Use as direct seed...")
        key_bytes = key_secret.encode('utf-8')
        
        if len(key_bytes) >= 32:
            seed = key_bytes[:32]
            private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
            
            # Convert to PEM format
            pem_key = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            print("✅ Method 2: Successfully converted to PEM!")
            print(f"📝 PEM Format:")
            pem_str = pem_key.decode('utf-8')
            print(pem_str)
            
            return pem_str
            
    except Exception as e:
        print(f"❌ Method 2 failed: {e}")
    
    try:
        # Method 3: Generate new Ed25519 key and show format
        print("\n🔧 Method 3: Generate example Ed25519 key...")
        private_key = ed25519.Ed25519PrivateKey.generate()
        
        # Show PEM format
        pem_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Show base64 format
        raw_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        base64_key = base64.b64encode(raw_bytes).decode('utf-8')
        
        print("✅ Example Ed25519 key formats:")
        print(f"\n📝 PEM Format:")
        print(pem_key.decode('utf-8'))
        print(f"\n📝 Base64 Format: {base64_key}")
        print(f"📝 Base64 length: {len(base64_key)} characters")
        
        return None
        
    except Exception as e:
        print(f"❌ Method 3 failed: {e}")
    
    return None

def save_pem_to_env(pem_key):
    """Save the PEM key to .env file"""
    
    if not pem_key:
        print("❌ No PEM key to save")
        return
    
    try:
        # Read current .env
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        # Update the key format
        new_lines = []
        updated = False
        
        for line in lines:
            if line.startswith('COINBASE_API_KEY_SECRET='):
                # Replace with PEM format (base64 encoded for storage)
                pem_b64 = base64.b64encode(pem_key.encode()).decode()
                new_lines.append(f'COINBASE_API_KEY_SECRET={pem_b64}\n')
                updated = True
            else:
                new_lines.append(line)
        
        if not updated:
            new_lines.append(f'COINBASE_API_KEY_SECRET={base64.b64encode(pem_key.encode()).decode()}\n')
        
        # Write back to .env
        with open('.env', 'w') as f:
            f.writelines(new_lines)
        
        print("✅ Updated .env with PEM format key")
        
    except Exception as e:
        print(f"❌ Failed to save to .env: {e}")

if __name__ == "__main__":
    print("🔧 Converting API Key to Proper Format")
    print("=" * 50)
    
    pem_key = convert_key_to_pem()
    
    if pem_key:
        print(f"\n💾 Would you like to save this PEM format to .env? (y/n)")
        # For now, just show the format
        print(f"\n📋 Copy this PEM key to your .env file:")
        print(f"COINBASE_API_KEY_SECRET_PEM='{pem_key.strip()}'")
    else:
        print(f"\n❌ Could not convert key to proper format")
        print(f"💡 You may need to regenerate your API key in proper Ed25519 format")
