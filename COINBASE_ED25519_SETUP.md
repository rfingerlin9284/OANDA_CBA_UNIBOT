# 🔐 COINBASE ADVANCED TRADE ED25519 SETUP GUIDE

## ✅ JWT ed25519 Authentication Now Implemented!


## 🚀 What's Been Fixed

### 1. New Coinbase API Client (`coinbase_advanced_api.py`)
- **JWT ed25519 signature authentication** ✅
- **Live endpoints only** (`https://api.coinbase.com`) ✅
- **Hamilton, NJ timezone awareness** (EST/EDT) ✅
- **Market session detection** (London/NY/China focus) ✅
- **Spot trading methods** for live execution ✅

### 2. Updated Dependencies
```bash
✅ cryptography>=41.0.0    # ed25519 cryptographic support
✅ PyJWT>=2.8.0           # JWT token creation and signing
✅ pycryptodome>=3.18.0   # Additional crypto support
✅ requests               # HTTP client
✅ pytz                   # Timezone handling
```

### 3. Updated Credentials Format
The `credentials.py` file now expects:
```python
COINBASE_API_KEY = "your_api_key_name"           # API Key NAME (not secret)
COINBASE_PRIVATE_KEY_B64 = "your_private_key"    # Base64 ed25519 private key
```

## 📋 How to Get Your Coinbase Advanced Trade API Credentials

### Step 1: Create API Key
1. Go to [Coinbase Developer Portal](https://portal.cdp.coinbase.com/access/api)
2. Click "Create API Key"
3. **IMPORTANT**: Select **"trade"** permissions for live trading
4. Download the JSON file (contains your credentials)

### Step 2: Extract Credentials
The downloaded JSON file looks like this:
```json
{
  "name": "organizations/your-org/apiKeys/your-key-id",
  "privateKey": "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEI...\n-----END EC PRIVATE KEY-----\n"
}
```

### Step 3: Update credentials.py
```python
# Copy the "name" field (the full path)
COINBASE_API_KEY = "organizations/your-org/apiKeys/your-key-id"

# Copy the "privateKey" field (including BEGIN/END lines)
COINBASE_PRIVATE_KEY_B64 = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEI...\n-----END EC PRIVATE KEY-----\n"
```

## 🧪 Test Your Setup

```bash
cd /home/ing/FOUR_horsemen/ALPHA_FOUR/proto_oanda/wolfpack-lite
```

Expected output for working credentials:
```
🔐 COINBASE ADVANCED TRADE AUTHENTICATION TEST
✅ Found X trading products
✅ Successfully authenticated!
📊 Found X accounts
💰 USD: 1234.56
✅ COINBASE ADVANCED TRADE JWT ED25519 AUTHENTICATION WORKING!
```

## 🎯 Live Trading Features Now Available

### Market Orders
```python
# Buy $100 of BTC
cb_api.create_spot_market_buy("BTC-USD", 100.00)

# Sell 0.001 BTC
cb_api.create_spot_market_sell("BTC-USD", 0.001)
```

### Limit Orders
```python
# Buy 0.001 BTC at $45,000
cb_api.create_spot_limit_buy("BTC-USD", 0.001, 45000.00)

# Sell 0.001 BTC at $50,000
cb_api.create_spot_limit_sell("BTC-USD", 0.001, 50000.00)
```

### Portfolio Management
```python
# Get all accounts
accounts = cb_api.get_accounts()

# Get order history
orders = cb_api.list_orders()

# Cancel orders
cb_api.cancel_orders(['order-id-1', 'order-id-2'])
```

## 🌍 Timezone & Market Session Features

The system automatically detects:
- **Current time in Hamilton, NJ** (EST/EDT)
- **Active market sessions**:
  - Asian (Tokyo/Hong Kong): 3 AM - 8 AM ET
  - London: 8 AM - 12 PM ET  
  - New York: 9 AM - 5 PM ET
  - Overlap periods for maximum liquidity

## 🚨 Security Notes

1. **Never commit credentials to git**
2. **Use environment variables in production**
3. **API keys have expiration dates**
4. **Monitor API usage limits**
5. **Test with small amounts first**

## 🔧 Integration Status

- ✅ **coinbase_advanced_api.py** - Complete JWT ed25519 implementation
- ✅ **credentials.py** - Updated for ed25519 format
- ✅ **main.py** - Updated to use new API client
- ✅ **Dependencies** - All cryptographic libraries installed

## 🎉 Ready for Live Trading!

Once you update your credentials, the system will be ready for:
- **24/7 Coinbase spot trading**
- **Real-time portfolio updates**  
- **Live FVG signal execution**
- **Arbitrage between OANDA and Coinbase**
- **Hamilton, NJ timezone-aware trading**

