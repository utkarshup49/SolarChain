import algopy.itxn
from algopy import ARC4Contract, String, UInt64, Account, Global, Asset
from algopy.arc4 import abimethod
from algopy.itxn import AssetTransferInnerTransaction


class AssetPurchase(ARC4Contract):

    @abimethod
    def purchase(self, seller: Account, buyer: Account, price: UInt64, qty: UInt64, asset: UInt64) -> None:
        """
        Purchase electrical units
        :param seller: Seller Account
        :param buyer: Buyer account
        :param price: Unit Price
        :param qty:  Unit Quantity
        :return:
        """
        algopy.itxn.AssetTransfer(
            xfer_asset=asset,
            asset_receiver=buyer,
            asset_amount=qty,
            asset_sender=seller,
            fee=1000
        ).submit()

