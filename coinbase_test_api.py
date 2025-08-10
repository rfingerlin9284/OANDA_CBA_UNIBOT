import json
import time
import logging
from coinbase.rest import RESTClient
try:
    from coinbase.rest.types import ApiException
except ImportError:
    # Fallback for different SDK versions
    class ApiException(Exception):
        pass

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
