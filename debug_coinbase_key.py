#!/usr/bin/env python3
"""
Debug script to determine proper Ed25519 key format and generate PEM
Using JSON credentials from your system
"""

import os
import base64
import logging
from credentials import WolfpackCredentials

def debug_key_format():
    """Debug the private key format and find working solution"""
    
    creds = WolfpackCredentials()
    private_key_b64 = creds.COINBASE_PRIVATE_KEY
    api_key_id = creds.COINBASE_API_KEY_ID
    
    print(f"API Key ID: {api_key_id}")
    print(f"Private Key: {private_key_b64}")
    print(f"Key Length: {len(private_key_b64)}")
    print(f"Length % 4: {len(private_key_b64) % 4}")
    print()
    
    # Try different approaches to fix the base64 key
    approaches = [
        ("Direct decode", lambda k: base64.b64decode(k)),
        ("Remove last char", lambda k: base64.b64decode(k[:-1])),
        ("Add padding", lambda k: base64.b64decode(k + "=")),
        ("Add double padding", lambda k: base64.b64decode(k + "==")),
        ("Add triple padding", lambda k: base64.b64decode(k + "===")),
        ("URL safe decode", lambda k: base64.urlsafe_b64decode(k + "==")),
    ]
    
    working_key = None
    working_method = None
    
    for method_name, decode_func in approaches:
        try:
            decoded_bytes = decode_func(private_key_b64)
            print(f"{method_name}: Decoded {len(decoded_bytes)} bytes")
            
            # Try different byte positions for 32-byte ed25519 seed
            for offset in [0, 32, len(decoded_bytes) - 32] if len(decoded_bytes) >= 32 else [0]:
                try:
                    if offset + 32 <= len(decoded_bytes):
                        seed = decoded_bytes[offset:offset + 32]
                        
                        # Try to load as ED25519 key
                        try:
                            from cryptography.hazmat.primitives.asymmetric import ed25519
                            from cryptography.hazmat.primitives import serialization
                            key = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
                            
                            # Generate PEM format
                            pem = key.private_bytes(
                                encoding=serialization.Encoding.PEM,
                                format=serialization.PrivateFormat.PKCS8,
                                encryption_algorithm=serialization.NoEncryption()
                            )
                            
                            print(f"✓ SUCCESS: {method_name} with offset {offset}")
                            print(f"  Seed length: {len(seed)} bytes")
                            print(f"  PEM format generated successfully")
                            print(f"  PEM Preview: {pem.decode()[:100]}...")
                            
                            working_key = seed
                            working_method = method_name
                            working_pem = pem.decode()
                            
                            # Test JWT generation if PyJWT is available
                            try:
                                import jwt
                                import time
                                
                                payload = {
                                    "iat": int(time.time()),
                                    "exp": int(time.time()) + 60,
                                    "iss": api_key_id,
                                    "sub": api_key_id
                                }
                                
                                jwt_token = jwt.encode(payload, pem, algorithm="EdDSA")
                                print(f"  JWT Token: {jwt_token[:50]}...")
                                
                            except ImportError:
                            except Exception as e:
                                print(f"  JWT generation failed: {e}")
                            
                            return {
                                "method": method_name,
                                "offset": offset,
                                "seed_hex": seed.hex(),
                                "seed_b64": base64.b64encode(seed).decode(),
                                "pem": working_pem,
                                "working": True
                            }
                            
                        except ImportError:
                            print(f"  Cryptography library not available")
                        except Exception as e:
                            print(f"  Failed to create ED25519 key: {e}")
                            
                except Exception as e:
                    print(f"  Failed at offset {offset}: {e}")
                    
        except Exception as e:
            print(f"{method_name}: Failed - {e}")
        
        print()
    
    print("❌ No working method found")
    return None

def analyze_base64_structure():
    """Analyze the base64 structure of your private key"""
    creds = WolfpackCredentials()
    private_key_b64 = creds.COINBASE_PRIVATE_KEY
    
    print("📊 BASE64 STRUCTURE ANALYSIS")
    print("=" * 40)
    print(f"Original key: {private_key_b64}")
    print(f"Length: {len(private_key_b64)} characters")
    print(f"Padding needed: {(4 - len(private_key_b64) % 4) % 4} characters")
    
    # Character frequency analysis
    char_count = {}
    for char in private_key_b64:
        char_count[char] = char_count.get(char, 0) + 1
    
    print(f"Character frequency: {dict(sorted(char_count.items()))}")
    
    # Check for common base64 patterns
    if private_key_b64.endswith('='):
        print("✓ Already has padding")
    else:
        print("! No padding detected")
    
    if any(char in private_key_b64 for char in ['+', '/']):
        print("✓ Standard base64 characters detected")
    elif any(char in private_key_b64 for char in ['-', '_']):
        print("✓ URL-safe base64 characters detected")
    else:
        print("! No special base64 characters detected")

if __name__ == "__main__":
    print("🔧 ED25519 KEY FORMAT DEBUG")
    print("=" * 50)
    print("JSON Credentials:")
    print('{"id": "2636c881-b44e-4263-b05d-fb10a5ad1836",')
    print(' "privateKey": "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="}')
    print("=" * 50)
    
    # First analyze the structure
    analyze_base64_structure()
    print()
    
    # Then try to find working format
    result = debug_key_format()
    
    if result:
        print("\n" + "="*60)
        print("🎉 WORKING SOLUTION FOUND!")
        print("="*60)
        print(f"Method: {result['method']}")
        print(f"Offset: {result['offset']}")
        print(f"Seed (hex): {result['seed_hex']}")
        print(f"Seed (base64): {result['seed_b64']}")
        print(f"\nPEM Format:")
        print(result['pem'])
        print("\n🔧 INTEGRATION OPTIONS:")
        print("="*30)
        print("Option 1 - Update credentials.py:")
        print(f"COINBASE_PRIVATE_KEY_SEED = \"{result['seed_b64']}\"")
        print(f"COINBASE_PRIVATE_KEY_PEM = \"\"\"")
        print(f"{result['pem'].strip()}")
        print(f"\"\"\"")
        
    else:
        print("\n❌ Could not determine working key format")
        print("💡 The private key may need to be regenerated in proper ED25519 format")
        print("💡 Or it might be in a different encoding format")
