import algopy
from algopy import ARC4Contract, UInt64, Account, itxn, Asset, Global
from algopy.arc4 import abimethod


class AssetPurchase(ARC4Contract):

    seller: Account
    buyer: Account
    price: UInt64
    qty: UInt64
    asset: Asset

    @abimethod
    def contract(self, seller: Account, buyer: Account, price: UInt64, qty: UInt64, asset: Asset) -> None:
        self.seller = seller
        self.buyer = buyer
        self.price = price
        self.qty = qty
        self.asset = asset

    # @abimethod
    # def non_fungible_asset_create(self) -> UInt64:
    #     """
    #     Following the ARC3 standard, the total supply must be 1 for a non-fungible asset.
    #     If you want to create fractional NFTs, `total` * `decimals` point must be 1.
    #     ex) total=100, decimals=2, 100 * 0.01 = 1
    #     """
    #     itxn_result = itxn.AssetConfig(
    #         total=100,
    #         decimals=2,
    #         unit_name="ML",
    #         asset_name="Mona Lisa",
    #         url="https://link_to_ipfs/Mona_Lisa",
    #         manager=Global.current_application_address,
    #         reserve=Global.current_application_address,
    #         freeze=Global.current_application_address,
    #         clawback=Global.current_application_address,
    #         fee=1000,
    #     ).submit()
    #     return itxn_result.created_asset.id

    @abimethod
    def asset_opt_in(self, asset: Asset) -> None:
        itxn.AssetTransfer(
            asset_receiver=Global.current_application_address,
            xfer_asset=asset,
            asset_amount=0,
            fee=1000,
        ).submit()

    @abimethod
    def begin_transfer(self, asset: Asset, buyer: Account, seller: Account, price: UInt64, qty: UInt64) -> None:
        itxn.AssetTransfer(
            xfer_asset = asset,
            asset_receiver=buyer,
            asset_amount=qty,
            fee=1000
        ).submit()

        itxn.Payment(
            receiver=seller,
            amount=price * qty,
            fee=1000
        ).submit()

        # TODO
        # group_id: int = transaction.assign_group_id([from_buyer, from_seller])



