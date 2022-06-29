# Copyright (c) 2021 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Module for generating wallets based on BIP specifications."""

# Imports
from typing import Any, Dict, Union
from bip_utils import Bip44Levels
from bip_utils.bip.bip32.bip32_key_data import Bip32KeyDataConst
from bip_utils.bip.bip44_base import Bip44Base
from py_crypto_hd_wallet.bip.hd_wallet_bip_addr import HdWalletBipAddresses
from py_crypto_hd_wallet.bip.hd_wallet_bip_enum import HdWalletBipDataTypes, HdWalletBipChanges
from py_crypto_hd_wallet.bip.hd_wallet_bip_keys import HdWalletBipKeys
from py_crypto_hd_wallet.common import HdWalletDataTypes, HdWalletBase
from py_crypto_hd_wallet.utils import Utils


class HdWalletBipConst:
    """Class container for HD wallet BIP constants."""

    # Map data types to dictionary key
    DATA_TYPE_TO_DICT_KEY: Dict[HdWalletDataTypes, str] = {
        HdWalletBipDataTypes.WALLET_NAME: "wallet_name",
        HdWalletBipDataTypes.COIN_NAME: "coin_name",
        HdWalletBipDataTypes.SPEC_NAME: "spec_name",
        HdWalletBipDataTypes.MNEMONIC: "mnemonic",
        HdWalletBipDataTypes.PASSPHRASE: "passphrase",
        HdWalletBipDataTypes.SEED_BYTES: "seed_bytes",
        HdWalletBipDataTypes.ACCOUNT_IDX: "account_idx",
        HdWalletBipDataTypes.CHANGE_IDX: "change_idx",
        HdWalletBipDataTypes.MASTER_KEY: "master_key",
        HdWalletBipDataTypes.PURPOSE_KEY: "purpose_key",
        HdWalletBipDataTypes.COIN_KEY: "coin_key",
        HdWalletBipDataTypes.ACCOUNT_KEY: "account_key",
        HdWalletBipDataTypes.CHANGE_KEY: "change_key",
        HdWalletBipDataTypes.ADDRESS_OFF: "address_off",
        HdWalletBipDataTypes.ADDRESS: "address",
    }


class HdWalletBip(HdWalletBase):
    """
    HD wallet BIP class.
    It allows to generate a complete wallet based on BIP specifications.
    """

    m_bip_obj: Bip44Base

    #
    # Public methods
    #

    def __init__(self,
                 wallet_name: str,
                 bip_obj: Bip44Base,
                 mnemonic: str = "",
                 passphrase: str = "",
                 seed_bytes: bytes = b"") -> None:
        """
        Construct class.

        Args:
            wallet_name (str)           : Wallet name
            bip_obj (Bip44Base object)  : Bip44Base object
            mnemonic (str, optional)    : Mnemonic, empty if not specified
            passphrase (str, optional)  : Passphrase, empty if not specified
            seed_bytes (bytes, optional): Seed_bytes, empty if not specified
        """
        super().__init__(HdWalletBipDataTypes, HdWalletBipConst.DATA_TYPE_TO_DICT_KEY)
        self.m_bip_obj = bip_obj
        # Initialize data
        self.__InitData(wallet_name, mnemonic, passphrase, seed_bytes)

    def Generate(self,
                 **kwargs: Any) -> None:
        """
        Generate wallet keys and addresses.

        Other Parameters:
            acc_idx (int, optional)                  : Account index (default: 0)
            change_idx (HdWalletBipChanges, optional): Change index (default: external)
            addr_num (int, optional)                 : Number of addresses to be generated (default: 20)
            addr_off (int, optional)                 : Starting address index (default: 0)
        """

        # Get parameters
        acc_idx = kwargs.get("acc_idx", 0)
        change_idx = kwargs.get("change_idx", HdWalletBipChanges.CHAIN_EXT)
        addr_num = kwargs.get("addr_num", 20)
        addr_off = kwargs.get("addr_off", 0)

        # Check parameters
        if not isinstance(change_idx, HdWalletBipChanges):
            raise TypeError("Change index is not an enumerative of HdWalletBipChanges")
        if addr_num < 0 or addr_num > Bip32KeyDataConst.KEY_INDEX_MAX_VAL:
            raise ValueError("Address number shall be greater or equal to zero and less than 2^32")
        if addr_off < 0 or ((addr_off + addr_num) > Bip32KeyDataConst.KEY_INDEX_MAX_VAL):
            raise ValueError("Address offset shall be greater or equal to zero and less than 2^32")

        # Save the BIP object
        bip_obj = self.m_bip_obj

        # Set master keys and derive purpose if correct level
        if bip_obj.IsLevel(Bip44Levels.MASTER):
            self.__SetKeys(HdWalletBipDataTypes.MASTER_KEY, bip_obj)
            bip_obj = bip_obj.Purpose()
        # Set purpose keys and derive coin if correct level
        if bip_obj.IsLevel(Bip44Levels.PURPOSE):
            self.__SetKeys(HdWalletBipDataTypes.PURPOSE_KEY, bip_obj)
            bip_obj = bip_obj.Coin()
        # Set coin keys and derive account if correct level
        if bip_obj.IsLevel(Bip44Levels.COIN):
            self.__SetKeys(HdWalletBipDataTypes.COIN_KEY, bip_obj)
            self._SetData(HdWalletBipDataTypes.ACCOUNT_IDX, acc_idx)
            bip_obj = bip_obj.Account(acc_idx)
        # Set account keys and derive change if correct level
        if bip_obj.IsLevel(Bip44Levels.ACCOUNT):
            self.__SetKeys(HdWalletBipDataTypes.ACCOUNT_KEY, bip_obj)
            self._SetData(HdWalletBipDataTypes.CHANGE_IDX, int(change_idx))
            bip_obj = bip_obj.Change(change_idx)

        # Set change keys and derive addresses if correct level
        if bip_obj.IsLevel(Bip44Levels.CHANGE):
            self.__SetKeys(HdWalletBipDataTypes.CHANGE_KEY, bip_obj)

            if addr_off != 0:
                self._SetData(HdWalletBipDataTypes.ADDRESS_OFF, addr_off)

            self._SetData(HdWalletBipDataTypes.ADDRESS,
                           HdWalletBipAddresses(bip_obj, addr_num, addr_off))
        # In this case, the wallet was created from an address index extended key,
        # so there is only one address to generate
        else:
            self._SetData(HdWalletBipDataTypes.ADDRESS,
                           HdWalletBipAddresses(bip_obj, 1, 0))

    def IsWatchOnly(self) -> bool:
        """
        Get if the wallet is watch-only.

        Returns :
            bool: True if watch-only, false otherwise
        """
        return self.m_bip_obj.IsPublicOnly()

    #
    # Private methods
    #

    def __InitData(self,
                   wallet_name: str,
                   mnemonic: str,
                   passphrase: str,
                   seed_bytes: bytes) -> None:
        """
        Initialize data.

        Args:
            wallet_name (str): Wallet name
            mnemonic (str)   : Mnemonic
            passphrase (str) : Passphrase
            seed_bytes (bytes) : Seed_bytes
        """

        # Set wallet name
        self._SetData(HdWalletBipDataTypes.WALLET_NAME, wallet_name)
        # Set specification name
        self._SetData(HdWalletBipDataTypes.SPEC_NAME, self.m_bip_obj.SpecName())
        # Set coin name
        coin_names = self.m_bip_obj.CoinConf().CoinNames()
        self._SetData(HdWalletBipDataTypes.COIN_NAME, f"{coin_names.Name()} ({coin_names.Abbreviation()})")

        # Set optional data if specified
        if mnemonic != "":
            self._SetData(HdWalletBipDataTypes.MNEMONIC, mnemonic)
            self._SetData(HdWalletBipDataTypes.PASSPHRASE, passphrase)
        if seed_bytes != b"":
            self._SetData(HdWalletBipDataTypes.SEED_BYTES, Utils.BytesToHexString(seed_bytes))

    def __SetKeys(self,
                  data_type: HdWalletBipDataTypes,
                  bip_obj: Bip44Base) -> None:
        """
        Add keys to wallet data.

        Args:
            data_type (HdWalletBipDataTypes): Data type
            bip_obj (Bip object)            : BIP object
        """
        self._SetData(data_type, HdWalletBipKeys(bip_obj))
