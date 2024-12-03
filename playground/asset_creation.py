import algokit_utils
from algokit_utils import get_account, get_account_from_mnemonic, get_default_localnet_config, get_indexer_client, \
    get_localnet_default_account
from algosdk import account, mnemonic
from algosdk.transaction import SuggestedParams, PaymentTxn, SignedTransaction, AssetConfigTxn
from algosdk.v2client import algod
from algosdk.v2client.algod import AlgodClient
from algosdk import transaction
from algosdk.v2client.indexer import IndexerClient

from SolarChain.projects.SolarChain.smart_contracts.artifacts.unit_transfer.asset_purchase_client import \
    AssetPurchaseClient
from playground.account_constants import ACCOUNTS, Account

# LocalNet configuration

LOCAL_NET: bool = False
if LOCAL_NET:
    TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"  # Default AlgoKit LocalNet token
    SERVER_ADDRESS = "http://localhost:4001"  # Default AlgoKit LocalNet endpoint
else:
    TOKEN = ""  # Default AlgoKit LocalNet token
    SERVER_ADDRESS = "https://testnet-api.algonode.cloud"  # Default AlgoKit LocalNet endpoint

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
    acc1 = Account(ACCOUNTS[0])
    acc2 = Account(ACCOUNTS[1])
else:
    acc1 = Account(ACCOUNTS[3])
    acc2 = Account(ACCOUNTS[4])

print("Public Address:", acc1.address)
print("My address:", acc1.private_key)
print("My mnemonic:", acc1.mnemonic)

# amount = 1 * 1000000  # Amount in microAlgos (0.1 ALGO)

params: SuggestedParams = algod_client.suggested_params()

def create_asset():
    # Create the transaction
    txn = transaction.AssetConfigTxn(
        sender=acc1.address,
        sp=params,
        default_frozen=False,
        unit_name="units",
        asset_name="Electrical Units",
        manager=acc1.address,
        reserve=acc1.address,
        freeze=acc1.address,
        clawback=acc1.address,
        url="https://path/to/my/asset/details",
        total=1000,
        decimals=0,
    )

    # Sign the transaction with the private key
    signed_txn: SignedTransaction = txn.sign(acc1.private_key)

    # Send the transaction
    tx_id: str = algod_client.send_transaction(signed_txn)
    print(f"Sent asset create transaction with txid: {tx_id}")
    # Wait for the transaction to be confirmed
    results = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

    # grab the asset id for the asset we just created
    created_asset = results["asset-index"]
    print(f"Asset ID created: {created_asset}")

created_asset = 730166188 if not LOCAL_NET else 1016

def receive_asset():
    optin_txn = transaction.AssetOptInTxn(
        sender=acc2.address, sp=params, index=created_asset
    )
    signed_optin_txn = optin_txn.sign(acc2.private_key)
    txid = algod_client.send_transaction(signed_optin_txn)
    print(f"Sent opt in transaction with txid: {txid}")

    # Wait for the transaction to be confirmed
    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

def transfer_asset():
    # Create transfer transaction
    xfer_txn = transaction.AssetTransferTxn(
        sender=acc1.address,
        sp=params,
        receiver=acc2.address,
        amt=1,
        index=created_asset,
    )
    signed_xfer_txn = xfer_txn.sign(acc1.private_key)
    txid = algod_client.send_transaction(signed_xfer_txn)
    print(f"Sent transfer transaction with txid: {txid}")

    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

def transfer_contract():
    indexer_client = IndexerClient(TOKEN, "https://testnet-idx.algonode.cloud")
    client = AssetPurchaseClient(
        algod_client,
        creator=get_account_from_mnemonic(ACCOUNTS[3]),
        indexer_client=indexer_client,
    )

    client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
    )

    client.purchase(buyer=acc2.address, seller=acc1.address, price=10, qty=10, asset=created_asset)



# create_asset()
# receive_asset()
# transfer_asset()

transfer_contract()
