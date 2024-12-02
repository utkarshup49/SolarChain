from collections.abc import Iterator

import pytest
from algopy_testing import AlgopyTestContext, algopy_testing_context

from smart_contracts.unit_transfer.unit_contract import AssetPurchase


@pytest.fixture()
def context() -> Iterator[AlgopyTestContext]:
    with algopy_testing_context() as ctx:
        yield ctx


def test_purchase(context: AlgopyTestContext) -> None:
    # Arrange
    dummy_account = context.any.account()
    dummy_amount = context.any.uint64(min_value=1, max_value=10)
    dummy_input = context.any.string(length=10)
    contract = AssetPurchase()

    # Act
    output = contract.purchase(dummy_account, dummy_amount, dummy_input)

    # Assert
    assert output == f"Buying units from an account with bal: {dummy_input}"
