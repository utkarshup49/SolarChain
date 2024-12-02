from algopy import ARC4Contract, String, UInt64, Account
from algopy.arc4 import abimethod


class AssetPurchase(ARC4Contract):
    # PRICE_PER_UNIT = UInt64(100_000)
    # ASSET_ID = 1016

    @abimethod
    def purchase(self, buyer: Account, amount: UInt64, test: String) -> String:
        """
        Purchase electrical units
        :param buyer: Buyer account
        :param amount: Amount of units to buy
        :return:
        """
        return "Buying units from an account with bal: " + test
