# PY crypto HD wallet
[![PyPI version](https://badge.fury.io/py/py-crypto-hd-wallet.svg)](https://badge.fury.io/py/py-crypto-hd-wallet)
[![Build Status](https://travis-ci.com/ebellocchia/py_crypto_hd_wallet.svg?branch=master)](https://travis-ci.com/ebellocchia/py_crypto_hd_wallet)
[![codecov](https://codecov.io/gh/ebellocchia/py_crypto_hd_wallet/branch/master/graph/badge.svg)](https://codecov.io/gh/ebellocchia/py_crypto_hd_wallet)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/45f6f8c688e4479e83069427ccd24e19)](https://www.codacy.com/gh/ebellocchia/py_crypto_hd_wallet/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ebellocchia/py_crypto_hd_wallet&amp;utm_campaign=Badge_Grade)
[![CodeFactor](https://www.codefactor.io/repository/github/ebellocchia/py_crypto_hd_wallet/badge)](https://www.codefactor.io/repository/github/ebellocchia/py_crypto_hd_wallet)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://raw.githubusercontent.com/ebellocchia/py_crypto_hd_wallet/master/LICENSE)

# Introduction

This package contains a very basic implementation of a HD (Hierarchical Deterministic) wallet based on my [bip_utils](https://github.com/ebellocchia/bip_utils) library.\
It is basically a nice wrapper for the *bip_utils* library for generating mnemonics, seeds, public/private keys and addresses.
Therefore, it has no network functionalities.\
The supported coins are the same of the [bip_utils](https://github.com/ebellocchia/bip_utils) library, so check the related page.

# Install the package

The package requires Python 3, it is not compatible with Python 2.
To install it:
- Using *pip*, from this directory (local):

        pip install .

- Using *pip*, from PyPI:

        pip install py_crypto_hd_wallet

**NOTE:** if you are using an Apple M1, please make sure to update *coincurve* (required by *bip_utils*) to version 17.0.0 otherwise it won't work.

To run tests:

    python -m unittest discover

Or you can install *tox*:

    pip install tox

And then simply run it:

    tox

This will run code coverage with different Python versions and perform style and code analysis.\
For quick test:

    tox -e unittest

# Modules description

- [BIP wallet](https://github.com/ebellocchia/py_crypto_hd_wallet/tree/master/readme/bip_wallet.md)
- [Algorand wallet](https://github.com/ebellocchia/py_crypto_hd_wallet/tree/master/readme/algorand_wallet.md)
- [Cardano Shelley wallet](https://github.com/ebellocchia/py_crypto_hd_wallet/tree/master/readme/cardano_shelley_wallet.md)
- [Electrum V1 wallet](https://github.com/ebellocchia/py_crypto_hd_wallet/tree/master/readme/electrum_v1_wallet.md)
- [Electrum V2 wallet](https://github.com/ebellocchia/py_crypto_hd_wallet/tree/master/readme/electrum_v2_wallet.md)
- [Monero wallet](https://github.com/ebellocchia/py_crypto_hd_wallet/tree/master/readme/monero_wallet.md)
- [Substrate wallet](https://github.com/ebellocchia/py_crypto_hd_wallet/tree/master/readme/substrate_wallet.md)

# Examples of wallet JSON outputs

- [BIP wallet](https://github.com/ebellocchia/py_crypto_hd_wallet/tree/master/readme/bip_wallet_examples.md)
- [Algorand wallet](https://github.com/ebellocchia/py_crypto_hd_wallet/tree/master/readme/algorand_wallet_examples.md)
- [Cardano Shelley wallet](https://github.com/ebellocchia/py_crypto_hd_wallet/tree/master/readme/cardano_shelley_wallet_examples.md)
- [Electrum V1 wallet](https://github.com/ebellocchia/py_crypto_hd_wallet/tree/master/readme/electrum_v1_wallet_examples.md)
- [Electrum V2 wallet](https://github.com/ebellocchia/py_crypto_hd_wallet/tree/master/readme/electrum_v2_wallet_examples.md)
- [Monero wallet](https://github.com/ebellocchia/py_crypto_hd_wallet/tree/master/readme/monero_wallet_examples.md)
- [Substrate wallet](https://github.com/ebellocchia/py_crypto_hd_wallet/tree/master/readme/substrate_wallet_examples.md)

# Documentation

The library documentation is available at [py-crypto-hd-wallet.readthedocs.io](https://py-crypto-hd-wallet.readthedocs.io).

# Buy me a coffee

You know, I'm italian and I love drinking coffee (especially while coding :D). So, if you'd like to buy me one:
- BTC: `bc1qq4r9cglwzd6f2hzxvdkucmdejvr9h8me5hy0k8`
- ERC20/BEP20: `0xf84e4898E5E10bf1fBe9ffA3EEC845e82e364b5B`

Thank you very much for your support.

# License

This software is available under the MIT license.
