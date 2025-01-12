# bip-39 24 seed generator

This Python script allows you to create and retrieve Bitcoin wallets, including generating mnemonic (seed) phrases and printing backup paths.

Disclaimer: This code hasn't been extensively tested. Test and use at your own risk.

## Requirements

- Python 3.x
- Bitcoinlib library: `pip3 install bitcoinlib`
- qrcode library: `pip3 install qrcode[pil]`

## Features

- **Create a new wallet** with a specified name.
- **List existing wallets** and display public addresses.
- **Retrieve the mnemonic (secret words)** for a specific wallet and display its public address as a QR code.
- **Print the file path** to a specific wallet.

## Usage

### 1. **Create a New Wallet**

To create a new wallet with a specified name, use the `--create` option. This will generate a new mnemonic and create a wallet with the given name.

```bash
python3 wallet.py --create <WALLET_NAME>
```

Example:

```bash
python3 wallet.py --create MyWallet
```

This will generate a new wallet, create a mnemonic, and store the seed phrase securely in a file. The wallet address will also be displayed.

### 2. **List All Existing Wallets**

To list all existing wallets, use the `--list` option. This will display the names and public addresses of all wallets stored.

```bash
python3 wallet.py --list
```

Example output:

```bash
Existing wallets:
- MyWallet: 1A2b3C4D5E6F7G8H9I0J1K2L3M4N5O6P7Q8
```

### 3. **Retrieve the Mnemonic (Secret Words) for a Specific Wallet**

To retrieve the mnemonic (seed phrase) for an existing wallet, use the `--retrieve` option. It will display the mnemonic and also show the wallet’s public address in a QR code format.

```bash
python3 wallet.py --retrieve <WALLET_NAME>
```

Example:

```bash
python3 wallet.py --retrieve MyWallet
```

Example output:

```bash
Mnemonic (secret words) for wallet 'MyWallet':
your mnemonic seed phrase goes here
Public address: 1A2b3C4D5E6F7G8H9I0J1K2L3M4N5O6P7Q8
QR code:
███████████████████████████████████████████████████████████████
███████████████████████████████████████████████████████████████
...
```

### 4. **Print the File Path to a Specific Wallet**

To print the file path to a specific backup, use the `--path` option.

```bash
python3 wallet.py --path <WALLET_NAME>
```

Example:

```bash
python3 .py --path My
```

Example output:

```bash
Path to Wallet 'MyWallet': /home/user/.bitcoinlib/wallets/MyWallet.wallet
```
