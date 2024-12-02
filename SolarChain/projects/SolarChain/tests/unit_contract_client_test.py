import algokit_utils
import pytest
from algokit_utils import get_localnet_default_account
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algopy import ARC4Contract, String, UInt64, Account

from smart_contracts.artifacts.unit_transfer.asset_purchase_client import AssetPurchaseClient

@pytest.fixture(scope="session")
def unit_contract_client(
    algod_client: AlgodClient, indexer_client: IndexerClient
) -> AssetPurchaseClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = AssetPurchaseClient(
        algod_client,
        creator=get_localnet_default_account(algod_client),
        indexer_client=indexer_client,
    )

    client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
    )
    return client


def test_says_text(unit_contract_client: AssetPurchaseClient) -> None:
    buyer = Account("about speed cupboard cushion middle catalog twenty mango nest produce tortoise orient shoe obvious gloom half fortune pride uncover member divert today dad abandon hire")
    result = unit_contract_client.purchase(buyer=buyer, amount=1, test="World")

    assert result.return_value == "Hello, World"


# def test_simulate_says_hello_with_correct_budget_consumed(
#         unit_contract_client: AssetPurchaseClient, algod_client: AlgodClient
# ) -> None:
#     result = (
#         unit_contract_client.compose().hello(name="World").hello(name="Jane").simulate()
#     )
#
#     assert result.abi_results[0].return_value == "Hello, World"
#     assert result.abi_results[1].return_value == "Hello, Jane"
#     assert result.simulate_response["txn-groups"][0]["app-budget-consumed"] < 100
