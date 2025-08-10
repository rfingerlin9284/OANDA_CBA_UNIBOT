#!/bin/bash

# Self-contained Bash script to set up and test Coinbase Advanced API with Python SDK
# Installs dependencies if needed, creates/updates Python script, runs connection test, and optional small trade test
# Run with: bash setup_coinbase_test.sh [test_trade] — add 'test_trade' arg to perform a $1 BUY test (live money, use caution!)

DIRECTORY="/home/ing/overlord/wolfpack-lite/oanda_cba_unibot"
KEY_FILE="$DIRECTORY/cdp_api_key.json"
PYTHON_FILE="$DIRECTORY/coinbase_test_api.py"
LOG_FILE="$DIRECTORY/coinbase_test_log.txt"

# Step 1: Install essentials if not present (numpy/pandas for future, but not used in test)
if ! pip3 show coinbase-advanced-py > /dev/null 2>&1; then
  pip3 install --user coinbase-advanced-py numpy pandas
  echo "Installed coinbase-advanced-py SDK." | tee -a $LOG_FILE
fi

# Step 2: Create/Update the Python test script (connects, fetches accounts/prices, optional small trade)
cat << 'PYEOF' > $PYTHON_FILE
import json
import time
import logging
from coinbase.rest import RESTClient
from coinbase.rest.types import ApiException

logging.basicConfig(filename='coinbase_test_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CoinbaseTest:
    def __init__(self, key_file='cdp_api_key.json'):
        self.client = None
        self.key_file = key_file
        self.connect()

    def connect(self):
        try:
            with open(self.key_file, 'r') as f:
                key_data = json.load(f)
            api_key = key_data['name']
            private_key = key_data['privateKey']
            self.client = RESTClient(api_key=api_key, api_secret=private_key)
            logger.info('Connected to Coinbase Advanced API (live).')
            print('Connection successful!')  # User feedback
        except Exception as e:
            logger.error(f'Connection failed: {str(e)}')
            print(f'Error: {str(e)}. Check log for details (e.g., bad key format? Ensure PEM starts/ends correctly).')
            raise

    def test_fetch_accounts(self):
        try:
            accounts = self.client.get_accounts().to_dict()
            logger.info('Fetched accounts: %s', accounts)
            print('Accounts fetched successfully. See log for details.')
            return accounts
        except Exception as e:
            logger.error(f'Fetch accounts failed: {str(e)}')
            print(f'Error fetching accounts: {str(e)} (e.g., rate limit? Wait and retry).')
            raise

    def test_fetch_price(self, product_id='BTC-USD'):
        try:
            product = self.client.get_product(product_id)
            price = float(product['price'])
            logger.info(f'Price for {product_id}: {price}')
            print(f'Current {product_id} price: {price}')
            return price
        except Exception as e:
            logger.error(f'Fetch price failed: {str(e)}')
            print(f'Error fetching price: {str(e)} (e.g., invalid product? Check Coinbase listings).')
            raise

    def test_place_small_order(self, side='BUY', product_id='BTC-USD', quote_size='1'):
        try:
            client_order_id = f'test_order_{int(time.time())}'
            if side == 'BUY':
                order = self.client.market_order_buy(client_order_id=client_order_id, product_id=product_id, quote_size=quote_size)
            elif side == 'SELL':
                order = self.client.market_order_sell(client_order_id=client_order_id, product_id=product_id, quote_size=quote_size)
            else:
                raise ValueError('Invalid side.')
            order_dict = order.to_dict()
            logger.info('Placed test order: %s', order_dict)
            print('Test order placed successfully. Details in log (LIVE TRADE EXECUTED—check Coinbase app!).')
            return order_dict
        except ApiException as e:
            logger.error(f'Order failed: {str(e)}')
            print(f'Error placing order: {str(e)} (e.g., insufficient funds? Add $1+ to account; or rate limit—wait 10s).')
            raise
        except Exception as e:
            logger.error(f'Unexpected order error: {str(e)}')
            print(f'Error: {str(e)}.')
            raise

if __name__ == '__main__':
    tester = CoinbaseTest()
    tester.test_fetch_accounts()
    tester.test_fetch_price()
    # Uncomment next line for live test trade (caution: uses real money!)
    # tester.test_place_small_order('BUY', 'BTC-USD', '1')  # $1 BUY BTC-USD
PYEOF

echo "Python test script created/updated at $PYTHON_FILE." | tee -a $LOG_FILE

# Step 3: Run tests (connection, fetch accounts/price)
python3 $PYTHON_FILE | tee -a $LOG_FILE

# Step 4: Optional test trade if arg provided (live, small $1 BUY)
if [ "$1" = "test_trade" ]; then
  echo "Performing live test trade ($1 BUY BTC-USD—confirm? Press Ctrl+C to cancel, or Enter to proceed."
  read -p ""
  sed -i 's/# tester.test_place_small_order/tester.test_place_small_order/' $PYTHON_FILE  # Enable trade line
  python3 $PYTHON_FILE | tee -a $LOG_FILE
  sed -i 's/tester.test_place_small_order/# tester.test_place_small_order/' $PYTHON_FILE  # Disable after run
  echo "Test trade complete. Check Coinbase for execution. Log: $LOG_FILE" | tee -a $LOG_FILE
else
  echo "Tests complete (no trade). To test trade, run: bash $0 test_trade" | tee -a $LOG_FILE
fi
