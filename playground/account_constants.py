import re

from algosdk import mnemonic, account

ACCOUNTS = [
    # Local net
    "ordinary trick boost jar hand census comfort again lamp multiply rude material wet garlic banner beef image champion resemble cloud runway apple gas absorb reason",
    "eager suit quarter income spider goat web present talent sail dutch method spike welcome skate between soldier reveal ethics hover like october obvious absent raccoon",
    "blush tornado delay draw slide item little fame pig bind banner tomato person deposit expire board clap range comic panel sand human verify about dust",

    # Test Net
    "about speed cupboard cushion middle catalog twenty mango nest produce tortoise orient shoe obvious gloom half fortune pride uncover member divert today dad abandon hire",
    "surge doctor duck usage clog congress claw number lucky cannon label illness limit business volcano peace result member tribe wagon vendor senior crane about job",
    "cup shallow usage network direct bulk night wash know boring confirm congress recycle client year river owner lamp film ginger father absorb rhythm tape clean"
]

class Account:

    def __init__(self, account_mnemonic_phrase: str):
        super().__init__()
        self._mnemonic_phrase: str = account_mnemonic_phrase
        self._private_key = mnemonic.to_private_key(account_mnemonic_phrase)
        self._public_address: str = account.address_from_private_key(self._private_key)

    @property
    def private_key(self) -> str:
        return self._private_key

    @property
    def mnemonic(self):
        return self._mnemonic_phrase

    @property
    def address(self):
        return self._public_address
