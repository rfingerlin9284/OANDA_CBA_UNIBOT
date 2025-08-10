#!/usr/bin/env python3
"""
🔐 MASTER COINBASE ADVANCED ED25519 JWT AUTHENTICATION PROTOCOL
CONSTITUTIONAL PIN: 841921
Uses JSON credentials format provided by user
References existing protocols and enhances with proper JSON credential structure

PROTOCOL INHERITANCE:
- coinbase_advanced_api.py: Base ED25519 JWT implementation
- coinbase_jwt_auth.py: JWT generation utilities
- coinbase_cdp_auth.py: CDP authentication methods
- AMENDMENT_V1.0_COINBASE_AUTH.md: Official protocol specification

JSON CREDENTIAL FORMAT (User Provided):
{
    "id": "2636c881-b44e-4263-b05d-fb10a5ad1836",
    "privateKey": "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="
}
"""

import os
import time
import json
import base64
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import requests
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MasterCoinbaseED25519Protocol:
    """
    🔥 MASTER COINBASE ADVANCED ED25519 JWT AUTHENTICATION PROTOCOL
    
    Uses exact JSON credentials provided by user:
    - API Key ID: 2636c881-b44e-4263-b05d-fb10a5ad1836
    - Private Key: s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg==
    
    LIVE TRADING ONLY - Constitutional PIN 841921
    """
    
    # CONSTITUTIONAL CREDENTIALS - FROM USER'S JSON FILE
    COINBASE_API_KEY_ID = "2636c881-b44e-4263-b05d-fb10a5ad1836"
    COINBASE_PRIVATE_KEY = "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="
    
    # LIVE ENDPOINTS ONLY
    COINBASE_LIVE_BASE_URL = "https://api.coinbase.com"
    COINBASE_CDP_BASE_URL = "https://api.cdp.coinbase.com"
    
    # ED25519 SIGNATURE ALGORITHM
    JWT_ALGORITHM = "EdDSA"
    SIGNATURE_ALGORITHM = "ed25519"
    
    def __init__(self, use_cdp_endpoint: bool = False):
        """
        Initialize Master ED25519 Authentication Protocol
        
        Args:
            use_cdp_endpoint: If True, use CDP endpoint; if False, use Advanced Trade endpoint
        """
        self.api_key_id = self.COINBASE_API_KEY_ID
        self.private_key_b64 = self.COINBASE_PRIVATE_KEY
        self.base_url = self.COINBASE_CDP_BASE_URL if use_cdp_endpoint else self.COINBASE_LIVE_BASE_URL
        self.use_cdp = use_cdp_endpoint
        
        # Load and validate ED25519 private key
        self.private_key = self._load_ed25519_private_key()
        
        logger.info("🔐 MASTER COINBASE ED25519 PROTOCOL INITIALIZED")
        logger.info(f"   API Key ID: {self.api_key_id}")
        logger.info(f"   Base URL: {self.base_url}")
        logger.info(f"   Algorithm: {self.JWT_ALGORITHM} (ED25519)")
        logger.info(f"   Endpoint Type: {'CDP' if use_cdp_endpoint else 'Advanced Trade'}")
        logger.info(f"   Constitutional PIN: 841921 ✅")
    
    def _load_ed25519_private_key(self):
        """
        Load ED25519 private key from base64 format
        
        Supports multiple formats:
        1. Raw 32-byte ED25519 private key (base64 encoded)
        2. 64-byte private+public key combination (base64 encoded)
        3. PEM format ED25519 private key
        """
        try:
            # First try: Direct base64 decode (32 bytes = raw private key)
            private_key_bytes = base64.b64decode(self.private_key_b64)
            
            logger.info(f"🔍 Private key decoded length: {len(private_key_bytes)} bytes")
            
            if len(private_key_bytes) == 32:
                # Raw ED25519 private key (32 bytes)
                private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
                logger.info("✅ Loaded 32-byte ED25519 private key")
                return private_key
                
            elif len(private_key_bytes) == 64:
                # Combined private+public key (64 bytes total, first 32 are private)
                private_key_only = private_key_bytes[:32]
                private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_only)
                logger.info("✅ Loaded 64-byte ED25519 private key (extracted first 32 bytes)")
                return private_key
                
            else:
                # Try PEM format parsing
                try:
                    # Assume it might be PEM format in base64
                    pem_data = base64.b64decode(self.private_key_b64).decode('utf-8')
                    if '-----BEGIN PRIVATE KEY-----' in pem_data:
                        private_key = serialization.load_pem_private_key(
                            pem_data.encode('utf-8'),
                            password=None
                        )
                        if isinstance(private_key, ed25519.Ed25519PrivateKey):
                            logger.info("✅ Loaded PEM format ED25519 private key")
                            return private_key
                except:
                    pass
                
                raise ValueError(f"Unsupported private key length: {len(private_key_bytes)} bytes")
                
        except Exception as e:
            logger.error(f"❌ Failed to load ED25519 private key: {e}")
            
            # Fallback: Try direct string interpretation
            try:
                # Maybe it's already a PEM string
                if '-----BEGIN PRIVATE KEY-----' in self.private_key_b64:
                    private_key = serialization.load_pem_private_key(
                        self.private_key_b64.encode('utf-8'),
                        password=None
                    )
                    if isinstance(private_key, ed25519.Ed25519PrivateKey):
                        logger.info("✅ Loaded direct PEM format ED25519 private key")
                        return private_key
            except:
                pass
                
            raise Exception(f"Could not load ED25519 private key in any supported format: {e}")
    
    def generate_jwt_token(self, method: str = "GET", path: str = "/api/v3/brokerage/accounts", body: str = "") -> str:
        """
        Generate JWT token using ED25519 signature
        
        Supports both Advanced Trade and CDP formats based on initialization
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            body: Request body for POST requests
            
        Returns:
            JWT token string
        """
        current_time = int(time.time())
        
        if self.use_cdp:
            # CDP Format (from coinbase_cdp_auth.py)
            payload = {
                'iss': 'cdp',  # Coinbase Developer Platform
                'nbf': current_time,
                'exp': current_time + 120,  # 2 minutes
                'sub': self.api_key_id,
                'uri': f"{method.upper()} {self.base_url}{path}",
                'aud': ['cdp_service']
            }
            
            headers = {
                'kid': self.api_key_id,
                'nonce': str(uuid.uuid4()),
                'typ': 'JWT',
                'alg': self.JWT_ALGORITHM
            }
            
        else:
            # Advanced Trade Format (from coinbase_advanced_api.py)
            payload = {
                'iss': self.api_key_id,  # API Key ID as issuer
                'exp': current_time + 120,  # 2 minutes
                'iat': current_time,  # Issued at
                'sub': self.api_key_id  # Subject
            }
            
            # Add request-specific claims for Advanced Trade
            if path and method:
                payload['uri'] = f"{method.upper()} {self.base_url}{path}"
            
            headers = {
                'alg': self.JWT_ALGORITHM,
                'kid': self.api_key_id,
                'typ': 'JWT'
            }
        
        try:
            # Generate JWT with ED25519 signature
            token = jwt.encode(
                payload,
                self.private_key,
                algorithm=self.JWT_ALGORITHM,
                headers=headers
            )
            
            logger.info(f"✅ JWT token generated successfully")
            logger.info(f"   Method: {method.upper()}")
            logger.info(f"   Path: {path}")
            logger.info(f"   Format: {'CDP' if self.use_cdp else 'Advanced Trade'}")
            
            return token
            
        except Exception as e:
            logger.error(f"❌ JWT generation failed: {e}")
            raise
    
    def get_auth_headers(self, method: str = "GET", path: str = "/api/v3/brokerage/accounts", body: str = "") -> Dict[str, str]:
        """
        Get complete authentication headers for API requests
        
        Returns headers ready for requests.request() calls
        """
        jwt_token = self.generate_jwt_token(method, path, body)
        
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Add API key header for some endpoints
        if not self.use_cdp:
            headers["CB-ACCESS-KEY"] = self.api_key_id
        
        return headers
    
    def make_authenticated_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> requests.Response:
        """
        Make authenticated request to Coinbase API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (with or without leading /)
            data: Request data for POST requests
            
        Returns:
            requests.Response object
        """
        # Ensure endpoint starts with /
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
            
        # Construct full URL
        url = f"{self.base_url}{endpoint}"
        
        # Get authentication headers
        body_str = json.dumps(data) if data else ""
        headers = self.get_auth_headers(method, endpoint, body_str)
        
        logger.info(f"📡 Making {method.upper()} request to {url}")
        
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=data if data else None,
                timeout=30
            )
            
            logger.info(f"📡 Response: {response.status_code}")
            
            if response.status_code not in [200, 201]:
                logger.error(f"❌ Request failed: {response.status_code}")
                logger.error(f"❌ Response text: {response.text}")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Request exception: {e}")
            raise
    
        """
        Test authentication by making a liveple API call
        
        Returns:
            True if authentication successful, False otherwise
        """
        logger.info("🧪 Testing authentication...")
        
        try:
            # Try accounts endpoint
            response = self.make_authenticated_request("GET", "/api/v3/brokerage/accounts")
            
            if response.status_code == 200:
                data = response.json()
                account_count = len(data.get('accounts', []))
                logger.info(f"✅ Authentication successful!")
                logger.info(f"   Accounts found: {account_count}")
                
                # Show USD balance if available
                for account in data.get('accounts', []):
                    if account.get('currency') == 'USD':
                        balance = account.get('available_balance', {}).get('value', '0')
                        if float(balance) > 0:
                            logger.info(f"   USD Balance: ${float(balance):,.2f}")
                            break
                
                return True
            else:
                logger.error(f"❌ Authentication failed: {response.status_code}")
                logger.error(f"❌ Response: {response.text}")
                return False
                
        except Exception as e:
            return False
    
    def get_accounts(self) -> Dict[str, Any]:
        """Get trading accounts"""
        response = self.make_authenticated_request("GET", "/api/v3/brokerage/accounts")
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get accounts: {response.status_code} - {response.text}")
    
    def list_products(self) -> Dict[str, Any]:
        """List available trading products"""
        response = self.make_authenticated_request("GET", "/api/v3/brokerage/products")
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to list products: {response.status_code} - {response.text}")
    
    def place_market_order(self, product_id: str, side: str, amount: str) -> Dict[str, Any]:
        """
        Place market order
        
        Args:
            product_id: Trading pair (e.g., 'BTC-USD')
            side: 'BUY' or 'SELL'
            amount: Order amount as string
            
        Returns:
            Order response data
        """
        order_data = {
            "client_order_id": f"wolf_{int(time.time())}_{uuid.uuid4().hex[:8]}",
            "product_id": product_id,
            "side": side.upper(),
            "order_configuration": {
                "market_market_ioc": {
                    "base_size": amount
                }
            }
        }
        
        logger.info(f"🚀 Placing market order: {side} {amount} {product_id}")
        
        response = self.make_authenticated_request("POST", "/api/v3/brokerage/orders", order_data)
        
        if response.status_code in [200, 201]:
            logger.info("✅ Order placed successfully")
            return response.json()
        else:
            raise Exception(f"Order failed: {response.status_code} - {response.text}")

    """
    Test the master ED25519 authentication protocol
    """
    print("🔐 MASTER COINBASE ED25519 AUTHENTICATION PROTOCOL TEST")
    print("=" * 60)
    print("JSON Credentials Used:")
    print(f"  API Key ID: 2636c881-b44e-4263-b05d-fb10a5ad1836")
    print(f"  Private Key: s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg==")
    print("=" * 60)
    
    # Test Advanced Trade endpoint
    print("\n🧪 Testing Advanced Trade Endpoint...")
    try:
        auth_advanced = MasterCoinbaseED25519Protocol(use_cdp_endpoint=False)
        
        if success_advanced:
            print("✅ Advanced Trade authentication successful!")
        else:
            print("❌ Advanced Trade authentication failed")
            
    except Exception as e:
        success_advanced = False
    
    # Test CDP endpoint
    print("\n🧪 Testing CDP Endpoint...")
    try:
        auth_cdp = MasterCoinbaseED25519Protocol(use_cdp_endpoint=True)
        
        if success_cdp:
            print("✅ CDP authentication successful!")
        else:
            print("❌ CDP authentication failed")
            
    except Exception as e:
        success_cdp = False
    
    # Summary
    print("\n🎯 PROTOCOL TEST SUMMARY")
    print("=" * 40)
    print(f"Advanced Trade API: {'✅ PASS' if success_advanced else '❌ FAIL'}")
    print(f"CDP API:           {'✅ PASS' if success_cdp else '❌ FAIL'}")
    print("=" * 40)
    
    if success_advanced or success_cdp:
        print("🚀 MASTER PROTOCOL READY FOR INTEGRATION!")
        print("Constitutional PIN: 841921")
        return True
    else:
        print("⚠️  AUTHENTICATION ISSUES - CHECK CREDENTIALS")
        return False

if __name__ == "__main__":
