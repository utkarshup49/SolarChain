import algokit_utils
from algokit_utils import OnSchemaBreak, \
    OnUpdate, transfer, TransferParameters, TransferAssetParameters, get_account_from_mnemonic, Account, \
    get_indexer_client, get_default_localnet_config
from algosdk.transaction import SuggestedParams
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from SolarChain.projects.SolarChain.smart_contracts.artifacts.unit_transfer.asset_purchase_client import \
    AssetPurchaseClient
from playground.account_constants import ACCOUNTS_LOCAL, ACCOUNTS_TEST_NET

# LocalNet configuration

# Make sure all accounts are properly setup
LOCAL_NET: bool = False # Set to False for Test Net, and True to use Local Net
if LOCAL_NET:
    TOKEN = "a" * 64  # Default AlgoKit LocalNet token
    SERVER_ADDRESS = "http://localhost:4001"  # Default AlgoKit LocalNet endpoint
    INDEXER_ADDRESS = "http://localhost:8980"
    INDEXER_TOKEN = TOKEN
else:
    TOKEN = ""  # Default AlgoKit LocalNet token
    SERVER_ADDRESS = "https://testnet-api.4160.nodely.dev"  # Default AlgoKit LocalNet endpoint
    INDEXER_ADDRESS = "https://testnet-idx.4160.nodely.dev"
    INDEXER_TOKEN = ""

# Initialize the Algod client
algod_client: AlgodClient = AlgodClient(TOKEN, SERVER_ADDRESS)
print("Algod Client Created")

# Check the connection by fetching the node status
try:
    status = algod_client.status()
    print("Connected to Algorand Network.")
    print("Network Status:", status)
except Exception as e:
    print("Failed to connect:", e)

# Generate address and mnemonic if needed
if LOCAL_NET:
    acc1: Account = get_account_from_mnemonic(ACCOUNTS_LOCAL[0])
    acc2: Account = get_account_from_mnemonic(ACCOUNTS_LOCAL[1])
else:
    acc1: Account = get_account_from_mnemonic(ACCOUNTS_TEST_NET[0])
    acc2: Account = get_account_from_mnemonic(ACCOUNTS_TEST_NET[1])

params: SuggestedParams = algod_client.suggested_params()
params.min_fee = 0
params.flat_fee = True
created_asset = 730166188 if not LOCAL_NET else 1006

app_indexer_client: IndexerClient = IndexerClient(indexer_address=INDEXER_ADDRESS, indexer_token=INDEXER_TOKEN)
app_client = AssetPurchaseClient(
    algod_client=algod_client,
    creator=acc1,
    indexer_client=app_indexer_client
)

app_client.deploy(
    on_schema_break=OnSchemaBreak.AppendApp,
    on_update=OnUpdate.AppendApp,
)

price = 1_000_000
qty = 1

FEES = 3_000
transfer(
    algod_client,
    TransferParameters(
        from_account=acc2,
        to_address=app_client.app_address,
        micro_algos=(FEES+price)*qty+200_000,
    )
)

app_client.contract(seller=acc1.address, buyer=acc2.address, price=price, qty=qty, asset=created_asset)
app_client.asset_opt_in(asset=created_asset)

algokit_utils.transfer_asset(
    algod_client,
    TransferAssetParameters(
        from_account=acc1,
        to_address=app_client.app_address,
        asset_id=created_asset,
        amount=qty
    )
)

app_client.begin_transfer(asset=created_asset, seller=acc1.address, buyer=acc2.address, price=price, qty=qty)


# app_client.send_purchase_asset(seller=acc1.address, price=1, qty=1, asset_id=created_asset)
# app_client.purchase(buyer=acc2, price=1, qty=1, asset_id=created_asset)
# print("Ret", app_client.test(hh="T").return_value)
# app_client.basic_transfer()
# asset_id = app_client.non_fungible_asset_create().return_value
# print(asset_id)
# app_client.asset_opt_in(asset=1036)
