from algokit_utils import get_indexer_client, get_default_localnet_config, get_localnet_default_account, OnSchemaBreak, \
    OnUpdate
from algosdk import transaction, mnemonic
from algosdk.account import address_from_private_key
from algosdk.logic import get_application_address
from algosdk.transaction import SuggestedParams, PaymentTxn, SignedTransaction
from algosdk.v2client.algod import AlgodClient

from SolarChain.projects.SolarChain.smart_contracts.artifacts.unit_transfer.asset_purchase_client import \
    AssetPurchaseClient
from playground.account_constants import ACCOUNTS_LOCAL, ACCOUNTS_TEST_NET, Account

# LocalNet configuration

LOCAL_NET: bool = True
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
    acc1 = Account(ACCOUNTS_LOCAL[0])
    acc2 = Account(ACCOUNTS_LOCAL[1])
else:
    acc1 = Account(ACCOUNTS_TEST_NET[3])
    acc2 = Account(ACCOUNTS_TEST_NET[4])

params: SuggestedParams = algod_client.suggested_params()

def create_asset():
    app_indexer_client = get_indexer_client(get_default_localnet_config("indexer"))
    app_client = AssetPurchaseClient(
        algod_client=algod_client,
        creator=get_localnet_default_account(algod_client),
        indexer_client=app_indexer_client
    )
    # Create the transaction
    a1 = get_application_address(app_client.app_id)
    txn = transaction.AssetConfigTxn(
        sender=a1,
        sp=params,
        default_frozen=False,
        unit_name="units",
        asset_name="Electrical Units",
        manager=a1,
        reserve=a1,
        freeze=a1,
        clawback=a1,
        url="https://path/to/my/asset/details",
        total=1000,
        decimals=0,
    )

    # Sign the transaction with the private key
    signed_txn: SignedTransaction = txn.sign(a1)

    # Send the transaction
    tx_id: str = algod_client.send_transaction(signed_txn)
    print(f"Sent asset create transaction with txid: {tx_id}")
    # Wait for the transaction to be confirmed
    results = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

    # grab the asset id for the asset we just created
    created_asset = results["asset-index"]
    print(f"Asset ID created: {created_asset}")

created_asset = 730166188 if not LOCAL_NET else 1006

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

    # Create transfer transaction
    xfer_txn = transaction.PaymentTxn(
        sender=acc2.address,
        sp=params,
        receiver=acc1.address,
        amt=units_bought*price_per_unit,
    )
    signed_xfer_txn = xfer_txn.sign(acc1.private_key)
    txid = algod_client.send_transaction(signed_xfer_txn)
    print(f"Sent transfer transaction with txid: {txid}")

    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

def transfer_contract():

    app_indexer_client = get_indexer_client(get_default_localnet_config("indexer"))
    app_client = AssetPurchaseClient(
        algod_client=algod_client,
        creator=get_localnet_default_account(algod_client),
        indexer_client=app_indexer_client
    )

    # params = algod_client.suggested_params()
    # fund_txn = PaymentTxn(
    #     sender=acc1.address,
    #     sp=params,
    #     receiver=get_application_address(app_client.app_id),  # Address of the smart contract account
    #     amt=2000000 # Amount in microALGOs
    # )
    # signed_fund_txn = fund_txn.sign(acc1.private_key)
    # algod_client.send_transaction(signed_fund_txn)
    # account_info = algod_client.account_info(get_application_address(app_client.app_id))
    # print(f"New Account Balance: {account_info['amount']} microALGOs")

    optin_txn = transaction.AssetOptInTxn(
        sender=app_client.app_address, sp=params, index=created_asset
    )
    app_client.signer.sign_transactions(optin_txn)
    # signed_optin_txn = optin_txn.sign()
    txid = algod_client.send_transaction(signed_optin_txn)
    print(f"Sent opt in transaction with txid: {txid}")

    # Wait for the transaction to be confirmed
    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

    xfer_txn = transaction.AssetTransferTxn(
        sender=acc1.address,
        sp=params,
        receiver=app_client.app_address,
        amt=100,
        index=created_asset,
    )
    signed_xfer_txn = xfer_txn.sign(acc1.private_key)
    txid = algod_client.send_transaction(signed_xfer_txn)
    print(f"Sent transfer transaction with txid: {txid}")

    results = transaction.wait_for_confirmation(algod_client, txid, 4)
    print(f"Result confirmed in round: {results['confirmed-round']}")

    app_client.deploy(
        on_schema_break=OnSchemaBreak.AppendApp,
        on_update=OnUpdate.AppendApp,
    )
    app_client.purchase(seller=acc1.address, buyer=acc2.address, price=10, qty=10, asset_id=created_asset)

# create_asset()
# receive_asset()
transfer_asset()
# transfer_contract()
