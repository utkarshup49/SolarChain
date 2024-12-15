from algokit_utils import get_account_from_mnemonic
from algopy import Account
from algosdk import transaction
from algosdk.transaction import SuggestedParams, SignedTransaction
from algosdk.v2client.algod import AlgodClient

from playground.account_constants import ACCOUNTS_LOCAL, ACCOUNTS_TEST_NET

# LocalNet configuration

LOCAL_NET: bool = True  # Set to False for Test Net, and True to use Local Net
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

def create_asset():
    # Create the transaction
    a1 = acc1.address
    txn = transaction.AssetConfigTxn(
        sender=a1,
        sp=params,
        default_frozen=False,
        unit_name="units",
        asset_name="Electrical Units Test 2",
        manager=a1,
        reserve=a1,
        freeze=a1,
        clawback=a1,
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

# Update the asset ID then call the receive_asset function
created_asset = 730166188 if not LOCAL_NET else 1006

def receive_asset(asset_id: int, account: Account):
    """
    Opts in the account for the asset
    :return: None
    """
    optin_txn = transaction.AssetOptInTxn(
        sender=account.address, sp=params, index=asset_id
    )
    signed_optin_txn = optin_txn.sign(account.private_key)
    txid = algod_client.send_transaction(signed_optin_txn)
    print(f"Sent opt in transaction with txid: {txid}")

    # Wait for the transaction to be confirmed
    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

# This is done via smart contract now
# def transfer_asset():
#     # Create transfer transaction
#     xfer_txn = transaction.AssetTransferTxn(
#         sender=acc1.address,
#         sp=params,
#         receiver=acc2.address,
#         amt=1,
#         index=created_asset,
#     )
#     signed_xfer_txn = xfer_txn.sign(acc1.private_key)
#     txid = algod_client.send_transaction(signed_xfer_txn)
#     print(f"Sent transfer transaction with txid: {txid}")
#
#     results = transaction.wait_for_confirmation(algod_client, txid, 4)
#     print(f"Result confirmed in round: {results['confirmed-round']}")
#
#     # Create transfer transaction
#     xfer_txn = transaction.PaymentTxn(
#         sender=acc2.address,
#         sp=params,
#         receiver=acc1.address,
#         amt=units_bought*price_per_unit,
#     )
#     signed_xfer_txn = xfer_txn.sign(acc1.private_key)
#     txid = algod_client.send_transaction(signed_xfer_txn)
#     print(f"Sent transfer transaction with txid: {txid}")
#
#     results = transaction.wait_for_confirmation(algod_client, txid, 4)
#     print(f"Result confirmed in round: {results['confirmed-round']}")


# create_asset()
receive_asset(created_asset, acc2)
