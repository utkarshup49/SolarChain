# All app wide constants should be listed here in order to avoid magic numbers/data

APP_NAME = "SolarChain"
APP_VERSION = '0.0.1'
LOCAL_NET: bool = True  # Set to False for Test Net, and True to use Local Net

if LOCAL_NET:
    ALGOD_TOKEN = "a" * 64  # Default AlgoKit LocalNet token
    ALGOD_SERVER_ADDRESS = "http://localhost:4001"  # Default AlgoKit LocalNet endpoint
    INDEXER_ADDRESS = "http://localhost:8980"
    INDEXER_TOKEN = ALGOD_TOKEN
else:
    ALGOD_TOKEN = ""  # Default AlgoKit LocalNet token
    ALGOD_SERVER_ADDRESS = "https://testnet-api.4160.nodely.dev"  # Default AlgoKit LocalNet endpoint
    INDEXER_ADDRESS = "https://testnet-idx.4160.nodely.dev"
    INDEXER_TOKEN = ""
