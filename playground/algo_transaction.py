from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.v2client.algod import AlgodClient

# Replace with your own Algod token and address
algod_token = "RkdKl_fL-TBRy2lhOQmQgBRxPNUrEBc4VLuuIpvI.kZo8GTe_vgxGjNOaiod8RdCfJR4156g_Gtr8WZhSvPw"
algod_address = "https://testnet-algorand.api.purestake.io/ps2"

# Headers needed if you're using PureStake
headers = {"X-API-Key": algod_token}

# Create the client
algod_client: AlgodClient = algod.AlgodClient(algod_token, algod_address, headers)
# print("Algod Client Created:", algod_client.health())
#
# # Check the connection by fetching the node status
# try:
#     status = algod_client.status()
#     print("Connected to Algorand Network.")
#     print("Network Status:", status)
# except Exception as e:
#     print("Failed to connect:", e)
#
# Generate address and mnemonic if needed
mnemonic_phrase = "balance ship reject pause bubble charge elegant envelope table prosper detail tonight shield source shiver asset senior fan matter kangaroo caught addict similar abstract drift"
private_key = mnemonic.to_private_key(mnemonic_phrase)
public_address = account.address_from_private_key(private_key)


# print("Public Address:", public_address)

# private_key, address = account.generate_account()
print("My address:", public_address)
print("My mnemonic:", mnemonic.from_private_key(private_key))

from algosdk import transaction

# Details for the transaction
# receiver_address = "HL34LEN2JX24MJWW6ZRUD7IQGTANY4O35MMLTHHLBTXUHYUL4ZEADLBVP4"  # Replace with the recipient's address
# amount = 1  # Amount in microAlgos (0.1 ALGO)

# Get suggested transaction parameters
# params = algod_client.suggested_params()

# Create the transaction
# txn = transaction.PaymentTxn(public_address, params, receiver_address, amount)

# Sign the transaction with the private key
# signed_txn = txn.sign(private_key)
#
# # Send the transaction
# tx_id = algod_client.send_transaction(signed_txn)
# print("Transaction ID:", tx_id)
#
# # Optional: Wait for confirmation
# import time
#
# def wait_for_confirmation(client: AlgodClient, txid):
#     last_round = client.status().get("last-round")
#     while True:
#         tx_info = client.pending_transaction_info(txid)
#         if tx_info.get("confirmed-round") and tx_info.get("confirmed-round") > 0:
#             print("Transaction confirmed in round", tx_info.get("confirmed-round"))
#             break
#         print("Waiting for confirmation...")
#         last_round += 1
#         client.status_after_block(last_round)
#
# wait_for_confirmation(algod_client, tx_id)
