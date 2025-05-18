import json

from algosdk.transaction import ApplicationCallTxn, ApplicationCreateTxn, OnComplete, PaymentTxn, StateSchema, \
    calculate_group_id
from algosdk.v2client import algod
from algosdk import account, mnemonic

from playground.account_constants import ACCOUNTS

# Replace these with your account details
creator_mnemonic = ACCOUNTS[3]
algod_token = ""
algod_address = "https://testnet-api.algonode.cloud"


# Helper Functions
def get_private_key_from_mnemonic(mn):
    return mnemonic.to_private_key(mn)


def wait_for_confirmation(client, txid):
    while True:
        try:
            tx_info = client.pending_transaction_info(txid)
            if tx_info.get("confirmed-round", 0) > 0:
                print(f"Transaction confirmed in round {tx_info['confirmed-round']}")
                return tx_info
        except Exception:
            pass


# Initialize the client
algod_client = algod.AlgodClient(algod_token, algod_address)

# Load account credentials
creator_private_key = get_private_key_from_mnemonic(creator_mnemonic)
creator_address = account.address_from_private_key(creator_private_key)


# Deploy the smart contract
def deploy_contract(client, private_key):
    approval_program = b"..."  # Compiled approval program (PyTeal output)
    clear_program = b"..."  # Compiled clear state program (PyTeal output)

    global_schema = StateSchema(num_uints=2, num_byte_slices=1)
    local_schema = StateSchema(num_uints=0, num_byte_slices=0)

    params = client.suggested_params()
    txn = ApplicationCreateTxn(
        sender=account.address_from_private_key(private_key),
        sp=params,
        on_complete=OnComplete.NoOpOC.real,
        approval_program=approval_program,
        clear_program=clear_program,
        global_schema=global_schema,
        local_schema=local_schema,
    )

    signed_txn = txn.sign(private_key)
    txid = client.send_transaction(signed_txn)
    wait_for_confirmation(client, txid)
    response = client.pending_transaction_info(txid)
    app_id = response["application-index"]
    print(f"Deployed app ID: {app_id}")
    return app_id


# Update energy for sale
def update_energy(client, app_id, private_key, energy_units, credit_price):
    params = client.suggested_params()
    txn = ApplicationCallTxn(
        sender=account.address_from_private_key(private_key),
        sp=params,
        index=app_id,
        on_complete=OnComplete.NoOpOC.real,
        app_args=[
            b"update",
            int(energy_units).to_bytes(8, "big"),
            int(credit_price).to_bytes(8, "big"),
        ],
    )
    signed_txn = txn.sign(private_key)
    txid = client.send_transaction(signed_txn)
    wait_for_confirmation(client, txid)
    print("Updated energy and price.")


# Buy energy
def buy_energy(client, app_id, buyer_private_key, energy_units, total_price, seller_address):
    params = client.suggested_params()
    # Payment to the smart contract
    pay_txn = PaymentTxn(
        sender=account.address_from_private_key(buyer_private_key),
        sp=params,
        receiver=seller_address,
        amt=total_price,
    )

    # Application call
    app_call_txn = ApplicationCallTxn(
        sender=account.address_from_private_key(buyer_private_key),
        sp=params,
        index=app_id,
        on_complete=OnComplete.NoOpOC.real,
        app_args=[b"buy", int(energy_units).to_bytes(8, "big")],
    )

    # Group transactions
    gid = calculate_group_id([pay_txn, app_call_txn])
    pay_txn.group = gid
    app_call_txn.group = gid

    signed_pay_txn = pay_txn.sign(buyer_private_key)
    signed_app_call_txn = app_call_txn.sign(buyer_private_key)

    client.send_transactions([signed_pay_txn, signed_app_call_txn])
    wait_for_confirmation(client, app_call_txn.get_txid())
    print("Energy purchased.")


# Example Usage
if __name__ == "__main__":
    # Deploy contract
    app_id = deploy_contract(algod_client, creator_private_key)

    # Seller updates energy and price
    update_energy(algod_client, app_id, creator_private_key, energy_units=50, credit_price=1000)

    # Buyer buys energy
    # buyer_mnemonic = ACCOUNTS[4]
    # buyer_private_key = get_private_key_from_mnemonic(buyer_mnemonic)
    # buyer_address = account.address_from_private_key(buyer_private_key)
    # buy_energy(algod_client, app_id, buyer_private_key, energy_units=10, total_price=10000,
    #            seller_address=creator_address)