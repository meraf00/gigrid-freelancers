from abc import ABC, abstractmethod
import json
import requests
from PaymentException import TransactionException


class PaymentHandler(ABC):
    """Abstract base class for all payment handlers"""

    def __init__(self, use_sandbox=True):
        """
        Args:
            use_sandbox (bool): initializes payment handler in test/production mode
                (default is True (test mode))
        """

        self.use_sandbox = use_sandbox

    @abstractmethod
    def generate_checkout_url(self, data: dict) -> str:
        pass

    @abstractmethod
    def verify_transaction(self, data: dict) -> bool:
        pass

    @abstractmethod
    def send_payment(self, data: dict):
        pass


class ChapaPaymentHandler(PaymentHandler):
    """PaymentHandler subclass using Chapa as payment provider"""

    API_VERSION = 'v1'

    BASE_URL = 'https://api.chapa.co'
    PAYMENT_URL = f'{BASE_URL}/{API_VERSION}/transaction/initialize'
    VERIFICATION_URL = f'{BASE_URL}/{API_VERSION}/transaction/verify'

    def __init__(self, secret_key, use_sandbox=True):
        """
        Args:
            secret_key (str): secret key provided by Chapa            
            use_sandbox (bool): initializes payment handler in test/production mode
                (default is True (test mode))
        """

        PaymentHandler.__init__(self, use_sandbox=use_sandbox)

        self.headers = {'Authorization': f'Bearer {secret_key}'}

    def __validate_data(self, data: dict) -> None:
        """Raises TransactionException if supplied data is not complient with
        what Chapa API expects

        Args:
            data (dict): key value pairs expected to be send to Chapa API

        Raises:
            TransactionException: if one of expected keys is missing in data
        """

        expected_keys = ['amount', 'currency', 'email', 'first_name',
                         'last_name', 'tx_ref', 'callback_url', 'return_url']

        for key in expected_keys:
            if not data.get(key):
                raise TransactionException(
                    f'{key} is missing in transaction data')

    def generate_checkout_url(self, data: dict) -> str:
        """Generates checkout url that users can use for payment

        Args:
            data (dict): transaction data as key value pairs expected by Chapa API

        Returns:
            str: checkout url
        """

        self.__validate_data(data)

        response = requests.post(self.PAYMENT_URL,
                                 data=data, headers=self.headers)
        response_json = json.loads(response.text)

        if response_json['status'] == 'success':
            return response_json['data']['checkout_url']

    def verify_transaction(self, data: dict) -> bool:
        return "super().verify_transaction(data)"

    def send_payment(self, data: dict):
        return 'super().send_payment(data)'


if __name__ == '__main__':
    handler = ChapaPaymentHandler('key')
    handler.generate_checkout_url({})
    print(handler.header)
