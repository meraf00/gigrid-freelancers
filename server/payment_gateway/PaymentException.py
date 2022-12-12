class TransactionException(Exception):
    """Exception class for payment related errors"""

    def __init__(self, message):
        Exception.__init__(self, message)
