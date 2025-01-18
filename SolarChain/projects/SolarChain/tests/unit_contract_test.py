from collections.abc import Iterator

import pytest
from Cryptodome.SelfTest.Util.test_number import MiscTests
from algopy_testing import AlgopyTestContext, algopy_testing_context
from algopy import Asset

from smart_contracts.unit_transfer.unit_contract import AssetPurchase


@pytest.fixture()
def context() -> Iterator[AlgopyTestContext]:
    with algopy_testing_context() as ctx:
        yield ctx


def test_purchase(context: AlgopyTestContext) -> None:
    # Arrange
    dummy_buyer_account = context.any.account()
    dummy_seller_account = context.any.account()
    dummy_price = context.any.uint64(min_value=1, max_value=10)
    dummy_qty = context.any.uint64(min_value=1, max_value=10)
    dummy_asset = context.any.asset(1016)
    contract = AssetPurchase()

    # Act
    output = contract.purchase(dummy_buyer_account, dummy_seller_account, dummy_price, dummy_qty, dummy_asset)

    # Assert
    assert output == None
