from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.v2client.algod import AlgodClient

# LocalNet configuration
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"  # Default AlgoKit LocalNet token
algod_address = "http://localhost:4001"  # Default AlgoKit LocalNet endpoint

# Initialize the Algod client
algod_client = algod.AlgodClient(algod_token, algod_address)
print("Algod Client Created:", algod_client.health())

# Check the connection by fetching the node status
try:
    status = algod_client.status()
    print("Connected to Algorand Network.")
    print("Network Status:", status)
except Exception as e:
    print("Failed to connect:", e)

# Generate address and mnemonic if needed
mnemonic_phrase = "bench where kingdom avocado candy bomb before mammal model rough oak snap satoshi belt tongue fold wide equal juice ripple wide galaxy reject above cover"

private_key = mnemonic.to_private_key(mnemonic_phrase)
public_address = account.address_from_private_key(private_key)

print("Public Address:", public_address)

# private_key, address = account.generate_account()
print("My address:", public_address)
print("My mnemonic:", mnemonic.from_private_key(private_key))

from algosdk import transaction

# Details for the transaction
receiver_address = "FDUYNCSL64XEJNYNQZ3IJMBRI64T4CB66DDDUPVIEGNY5GEJNIKCOZMV5A"  # Replace with the recipient's address
amount = 1000000  # Amount in microAlgos (0.1 ALGO)

# Get suggested transaction parameters
params = algod_client.suggested_params()

# Create the transaction
txn = transaction.PaymentTxn(public_address, params, receiver_address, amount)

# Sign the transaction with the private key
signed_txn = txn.sign(private_key)

# Send the transaction
tx_id = algod_client.send_transaction(signed_txn)
print("Transaction ID:", tx_id)

# Optional: Wait for confirmation
import time

def wait_for_confirmation(client: AlgodClient, txid):
    last_round = client.status().get("last-round")
    while True:
        tx_info = client.pending_transaction_info(txid)
        if tx_info.get("confirmed-round") and tx_info.get("confirmed-round") > 0:
            print("Transaction confirmed in round", tx_info.get("confirmed-round"))
            break
        print("Waiting for confirmation...")
        last_round += 1
        client.status_after_block(last_round)

wait_for_confirmation(algod_client, tx_id)
