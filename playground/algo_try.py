from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.v2client.algod import AlgodClient

# Replace with your own Algod token and address
algod_token = "YOUR_ALGOD_API_TOKEN"
algod_address = "https://testnet-algorand.api.purestake.io/ps2"  # PureStake Testnet URL

# Headers needed if you're using PureStake
headers = {"X-API-Key": algod_token}

# Create the client
algod_client: AlgodClient = algod.AlgodClient(algod_token, algod_address, headers)
print(algod_client)

private_key, address = account.generate_account()
print("My address:", address)
print("My mnemonic:", mnemonic.from_private_key(private_key))

mnemonic_phrase = "balance ship reject pause bubble charge elegant envelope table prosper detail tonight shield source shiver asset senior fan matter kangaroo caught addict similar abstract drift"
private_key = mnemonic.to_private_key(mnemonic_phrase)
public_address = account.address_from_private_key(private_key)


