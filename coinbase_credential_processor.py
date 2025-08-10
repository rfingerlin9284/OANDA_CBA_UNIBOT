#!/usr/bin/env python3
"""
🔐 COINBASE CREDENTIAL EXTRACTION & CONVERSION UTILITY
Constitutional PIN: 841921

This utility provides exact methods to extract and convert Coinbase Advanced Trade
API credentials from JSON format to all required formats with detailed examples.

EXACT PLACEHOLDER EXAMPLES:
- API Key ID: 2636c881-b44e-4263-b05d-fb10a5ad1836
- Private Key: s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg==
"""

import base64
import json
import binascii
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

class CoinbaseCredentialProcessor:
    """
    🔧 EXACT CREDENTIAL PROCESSING WITH PLACEHOLDER EXAMPLES
    
    This class provides exact methods to process Coinbase credentials
    with detailed format specifications and working examples.
    """
    
    def __init__(self):
        print("🔧 Coinbase Credential Processor Initialized")
        print("Constitutional PIN: 841921")
    
    @staticmethod
    def process_json_credentials(json_data):
        """
        📄 PROCESS JSON CREDENTIALS - EXACT METHOD
        
        Processes Coinbase API credentials from JSON format and extracts
        all required formats with exact specifications.
        
        Args:
            json_data (dict or str): JSON credentials from Coinbase
            
        Returns:
            dict: Complete credential formats
        """
        
        # Parse JSON if string
        if isinstance(json_data, str):
            credentials = json.loads(json_data)
        else:
            credentials = json_data
        
        # Extract basic fields
        api_key_id = credentials.get('id')
        private_key_b64 = credentials.get('privateKey')
        
        print(f"📋 Processing Coinbase Credentials:")
        print(f"   API Key ID: {api_key_id}")
        print(f"   Private Key Length: {len(private_key_b64)} characters")
        
        # Decode the 64-byte private key
        private_key_bytes = base64.b64decode(private_key_b64)
        print(f"   Decoded Private Key: {len(private_key_bytes)} bytes")
        
        # Extract Ed25519 seed (first 32 bytes)
        ed25519_seed = private_key_bytes[:32]
        ed25519_seed_b64 = base64.b64encode(ed25519_seed).decode('utf-8')
        ed25519_seed_hex = ed25519_seed.hex()
        
        print(f"   Ed25519 Seed: {len(ed25519_seed)} bytes")
        print(f"   Ed25519 Seed (B64): {len(ed25519_seed_b64)} characters")
        print(f"   Ed25519 Seed (Hex): {len(ed25519_seed_hex)} characters")
        
        # Generate Ed25519 private key object
        ed25519_private_key = ed25519.Ed25519PrivateKey.from_private_bytes(ed25519_seed)
        
        # Convert to PEM format
        pem_private_key = ed25519_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')
        
        print(f"   PEM Format: {len(pem_private_key)} characters")
        
        # Return complete format specification
        return {
            "source_json": {
                "id": api_key_id,
                "privateKey": private_key_b64
            },
            "extracted_formats": {
                "api_key_id": {
                    "value": api_key_id,
                    "format": "UUID v4",
                    "length": len(api_key_id),
                    "usage": "JWT 'sub' claim and 'kid' header"
                },
                "private_key_original": {
                    "value": private_key_b64,
                    "format": "Base64 encoded 64-byte key",
                    "length": len(private_key_b64),
                    "decoded_length": len(private_key_bytes),
                    "usage": "Original format from Coinbase"
                },
                "ed25519_seed": {
                    "value": ed25519_seed_b64,
                    "format": "Base64 encoded 32-byte Ed25519 seed",
                    "length": len(ed25519_seed_b64),
                    "decoded_length": len(ed25519_seed),
                    "usage": "Ed25519 key generation"
                },
                "ed25519_hex": {
                    "value": ed25519_seed_hex,
                    "format": "Hexadecimal 32-byte Ed25519 seed",
                    "length": len(ed25519_seed_hex),
                    "usage": "Debugging and verification"
                },
                "pem_format": {
                    "value": pem_private_key,
                    "format": "PKCS#8 PEM private key",
                    "length": len(pem_private_key),
                    "usage": "Direct use with PyJWT EdDSA algorithm"
                }
            },
            "validation": {
                "key_type": str(type(ed25519_private_key)),
                "is_valid": True,
                "can_sign": True
            }
        }
    
    @staticmethod
    def generate_exact_placeholder_examples():
        """
        📋 GENERATE EXACT PLACEHOLDER EXAMPLES
        
        Generates exact placeholder examples showing the format specifications
        for Coinbase Advanced Trade API credentials.
        """
        
        placeholder_examples = {
            "title": "COINBASE ADVANCED TRADE API CREDENTIAL PLACEHOLDERS",
            "description": "Exact placeholder examples with format specifications",
            
            "json_source_format": {
                "description": "Original JSON format from Coinbase Developer Portal",
                "file_name": "coinbase_api_key.json",
                "exact_format": {
                    "id": "XXXXXXXX-XXXX-4XXX-YXXX-XXXXXXXXXXXX",
                    "privateKey": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                },
                "real_example": {
                    "id": "2636c881-b44e-4263-b05d-fb10a5ad1836",
                    "privateKey": "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="
                },
                "field_specifications": {
                    "id": {
                        "description": "API Key ID",
                        "format": "UUID version 4",
                        "pattern": "8-4-4-4-12 hexadecimal digits",
                        "total_length": 36,
                        "example_breakdown": "2636c881-b44e-4263-b05d-fb10a5ad1836"
                    },
                    "privateKey": {
                        "description": "Ed25519 private key + public key",
                        "format": "Base64 encoded",
                        "total_length": 88,
                        "decoded_length": 64,
                        "structure": "32 bytes private seed + 32 bytes public key",
                        "encoding": "Standard Base64 with padding"
                    }
                }
            },
            
            "credentials_py_format": {
                "description": "Format for credentials.py file",
                "code_template": '''
# ========== COINBASE ADVANCED TRADE CREDENTIALS ==========
class CoinbaseCredentials:
    """Coinbase Advanced Trade API Credentials - Constitutional PIN 841921"""
    
    # Primary Credentials (from JSON file)
    COINBASE_API_KEY_ID = "REPLACE_WITH_YOUR_API_KEY_ID"
    COINBASE_PRIVATE_KEY = "REPLACE_WITH_YOUR_PRIVATE_KEY_BASE64"
    
    # Extracted Ed25519 Formats
    COINBASE_PRIVATE_KEY_SEED = "REPLACE_WITH_EXTRACTED_32_BYTE_SEED"
    COINBASE_PRIVATE_KEY_HEX = "REPLACE_WITH_HEX_SEED"
    COINBASE_PRIVATE_KEY_PEM = """-----BEGIN PRIVATE KEY-----
REPLACE_WITH_PEM_CONTENT_LINE_1
REPLACE_WITH_PEM_CONTENT_LINE_2
-----END PRIVATE KEY-----"""
    
    # Endpoint Configuration
    COINBASE_LIVE_URL = "https://api.coinbase.com"
    COINBASE_ALGORITHM = "EdDSA"  # Ed25519
''',
                "replacement_guide": {
                    "REPLACE_WITH_YOUR_API_KEY_ID": {
                        "source": "JSON 'id' field",
                        "format": "36-character UUID",
                        "example": "2636c881-b44e-4263-b05d-fb10a5ad1836"
                    },
                    "REPLACE_WITH_YOUR_PRIVATE_KEY_BASE64": {
                        "source": "JSON 'privateKey' field",
                        "format": "88-character base64 string",
                        "example": "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="
                    },
                    "REPLACE_WITH_EXTRACTED_32_BYTE_SEED": {
                        "source": "First 32 bytes of decoded privateKey",
                        "format": "44-character base64 string",
                        "example": "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2Ic="
                    },
                    "REPLACE_WITH_HEX_SEED": {
                        "source": "32-byte seed in hexadecimal",
                        "format": "64-character hex string",
                        "example": "b3e8d4792e781b1a7143758e339b8b1c7966f4984222bb41784f57d43ae7d887"
                    },
                    "REPLACE_WITH_PEM_CONTENT_LINE_1": {
                        "source": "PEM private key content (line 1)",
                        "format": "Base64 encoded PKCS#8 content",
                        "example": "MC4CAQAwBQYDK2VwBCIEILPo1HkueBsacUN1jjObixx5ZvSYQiK7QXhPV9Q659iH"
                    },
                    "REPLACE_WITH_PEM_CONTENT_LINE_2": {
                        "source": "Usually just the end marker",
                        "format": "May be empty or continuation",
                        "example": "(usually empty for Ed25519)"
                    }
                }
            },
            
            "jwt_payload_format": {
                "description": "JWT payload format with exact placeholders",
                "template": {
                    "iss": "cdp",
                    "sub": "REPLACE_WITH_API_KEY_ID",
                    "nbf": "REPLACE_WITH_CURRENT_TIMESTAMP",
                    "exp": "REPLACE_WITH_EXPIRY_TIMESTAMP", 
                    "uri": "REPLACE_WITH_REQUEST_URI",
                    "aud": ["cdp_service"]
                },
                "placeholder_examples": {
                    "REPLACE_WITH_API_KEY_ID": {
                        "format": "API Key ID (same as credentials)",
                        "example": "2636c881-b44e-4263-b05d-fb10a5ad1836"
                    },
                    "REPLACE_WITH_CURRENT_TIMESTAMP": {
                        "format": "Unix timestamp (integer)",
                        "example": 1722873367,
                        "generation": "int(time.time())"
                    },
                    "REPLACE_WITH_EXPIRY_TIMESTAMP": {
                        "format": "Unix timestamp (current + 120)",
                        "example": 1722873487,
                        "generation": "int(time.time()) + 120"
                    },
                    "REPLACE_WITH_REQUEST_URI": {
                        "format": "METHOD hostname/path",
                        "example": "GET api.coinbase.com/api/v3/brokerage/accounts",
                        "template": "{METHOD} api.coinbase.com{PATH}"
                    }
                },
                "critical_notes": [
                    "iss MUST be 'cdp' - never change this",
                    "aud MUST be ['cdp_service'] as array - not string",
                    "Maximum expiry is 120 seconds",
                    "URI must include method and full hostname"
                ]
            }
        }
        
        return placeholder_examples
    
    @staticmethod 
    def create_conversion_script():
        """
        🔄 CREATE CREDENTIAL CONVERSION SCRIPT
        
        Creates a complete script to convert Coinbase JSON credentials
        to all required formats with exact examples.
        """
        
        script = '''#!/usr/bin/env python3
"""
🔄 COINBASE CREDENTIAL CONVERTER
Constitutional PIN: 841921

This script converts Coinbase JSON credentials to all required formats.

USAGE:
1. Replace the JSON data below with your actual credentials
2. Run the script to get all converted formats
3. Copy the outputs to your credentials.py file

EXAMPLE INPUT:
{"id": "2636c881-b44e-4263-b05d-fb10a5ad1836", "privateKey": "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="}
"""

import base64
import json
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

def convert_coinbase_credentials():
    """Convert Coinbase JSON credentials to all formats"""
    
    # 🔄 REPLACE THIS WITH YOUR ACTUAL CREDENTIALS
    json_credentials = {
        "id": "REPLACE_WITH_YOUR_API_KEY_ID",
        "privateKey": "REPLACE_WITH_YOUR_PRIVATE_KEY_BASE64"
    }
    
    print("🔄 COINBASE CREDENTIAL CONVERTER")
    print("Constitutional PIN: 841921")
    print("=" * 50)
    print()
    
    # Extract basic info
    api_key_id = json_credentials["id"]
    private_key_b64 = json_credentials["privateKey"]
    
    print(f"📋 INPUT CREDENTIALS:")
    print(f"   API Key ID: {api_key_id}")
    print(f"   Private Key: {private_key_b64[:20]}... ({len(private_key_b64)} chars)")
    print()
    
    # Decode and extract Ed25519 seed
    private_key_bytes = base64.b64decode(private_key_b64)
    ed25519_seed = private_key_bytes[:32]
    ed25519_seed_b64 = base64.b64encode(ed25519_seed).decode('utf-8')
    ed25519_seed_hex = ed25519_seed.hex()
    
    # Generate PEM format
    ed25519_private_key = ed25519.Ed25519PrivateKey.from_private_bytes(ed25519_seed)
    pem_private_key = ed25519_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    
    print("🔄 CONVERTED FORMATS:")
    print("=" * 30)
    print()
    
    print("📄 1. CREDENTIALS.PY FORMAT:")
    print('# ========== COINBASE ADVANCED TRADE CREDENTIALS ==========')
    print(f'COINBASE_API_KEY_ID = "{api_key_id}"')
    print(f'COINBASE_PRIVATE_KEY = "{private_key_b64}"')
    print()
    print(f'# Extracted Ed25519 Formats')
    print(f'COINBASE_PRIVATE_KEY_SEED = "{ed25519_seed_b64}"')
    print(f'COINBASE_PRIVATE_KEY_HEX = "{ed25519_seed_hex}"')
    print('COINBASE_PRIVATE_KEY_PEM = """' + pem_private_key + '"""')
    print()
    
    print("📄 2. FORMAT SPECIFICATIONS:")
    print(f"   API Key ID: {len(api_key_id)} characters (UUID format)")
    print(f"   Original Private Key: {len(private_key_b64)} characters (Base64)")
    print(f"   Ed25519 Seed: {len(ed25519_seed_b64)} characters (Base64)")
    print(f"   Ed25519 Hex: {len(ed25519_seed_hex)} characters (Hexadecimal)")
    print(f"   PEM Format: {len(pem_private_key)} characters (PKCS#8)")
    print()
    
    print("✅ 3. VALIDATION:")
    print(f"   Decoded Key Length: {len(private_key_bytes)} bytes ✅")
    print(f"   Ed25519 Seed Length: {len(ed25519_seed)} bytes ✅")
    print(f"   Key Type: {type(ed25519_private_key)} ✅")
    print()
    
    print("🔐 4. USAGE NOTES:")
    print("   • Use API_KEY_ID for JWT 'sub' claim and 'kid' header")
    print("   • Use PEM format for JWT signing with PyJWT")
    print("   • Use Seed format for direct Ed25519 operations")
    print("   • Original private key contains seed + public key")
    print()
    
    print("🚀 CONVERSION COMPLETE - Ready for integration!")

if __name__ == "__main__":
    convert_coinbase_credentials()
'''
        
        return script

def main():
    """
    🔧 MAIN CREDENTIAL PROCESSING DEMONSTRATION
    
    Demonstrates the exact credential processing with placeholder examples.
    """
    
    print("🔧 COINBASE CREDENTIAL EXTRACTION & CONVERSION UTILITY")
    print("Constitutional PIN: 841921")
    print("=" * 70)
    print()
    
    processor = CoinbaseCredentialProcessor()
    
    # Example JSON credentials (with actual working example)
    example_json = {
        "id": "2636c881-b44e-4263-b05d-fb10a5ad1836",
        "privateKey": "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="
    }
    
    print("📄 1. PROCESSING EXAMPLE CREDENTIALS")
    print("-" * 40)
    
    # Process the credentials
    result = processor.process_json_credentials(example_json)
    
    print()
    print("📋 2. EXTRACTED FORMATS")
    print("-" * 40)
    
    for format_name, format_data in result["extracted_formats"].items():
        print(f"{format_name.upper()}:")
        print(f"   Value: {format_data['value'][:50]}{'...' if len(format_data['value']) > 50 else ''}")
        print(f"   Format: {format_data['format']}")
        print(f"   Length: {format_data['length']} characters")
        print(f"   Usage: {format_data['usage']}")
        print()
    
    print("📋 3. PLACEHOLDER EXAMPLES")
    print("-" * 40)
    
    placeholders = processor.generate_exact_placeholder_examples()
    
    print("JSON Source Format:")
    json_format = placeholders["json_source_format"]["exact_format"]
    print(f'  {{"id": "{json_format["id"]}"}}')
    print(f'  {{"privateKey": "{json_format["privateKey"]}"}}')
    print()
    
    print("Field Specifications:")
    for field, spec in placeholders["json_source_format"]["field_specifications"].items():
        print(f"  {field}: {spec['format']} - {spec['description']}")
        print(f"    Pattern: {spec.get('pattern', 'N/A')}")
        print(f"    Length: {spec['total_length']} characters")
    print()
    
    print("🔄 4. CONVERSION SCRIPT")
    print("-" * 40)
    
    script = processor.create_conversion_script()
    print("Conversion script created - can be saved as 'convert_credentials.py'")
    print("Script includes:")
    print("   • Exact placeholder replacement guide")
    print("   • Format validation")
    print("   • Ready-to-copy credentials.py format")
    print("   • Usage instructions")
    print()
    
    print("✅ CREDENTIAL PROCESSING COMPLETE")
    print("All formats documented with exact specifications and examples.")

if __name__ == "__main__":
    main()
