import argparse
import os
from bitcoinlib.wallets import Wallet, WalletError, wallets_list
from bitcoinlib.mnemonic import Mnemonic
import qrcode


def get_default_wallet_storage() -> str:
    """Return the default wallet storage directory."""
    return os.path.expanduser("~/.bitcoinlib/wallets")


def create_wallet(wallet_name: str) -> None:
    """Create a new Bitcoin wallet with a mnemonic and store its seed phrase."""
    try:
        # Ensure the wallets directory exists
        storage_dir = get_default_wallet_storage()
        os.makedirs(storage_dir, exist_ok=True)
        print(f"Wallets directory: {storage_dir}")

        # Generate a new mnemonic using the BIP39 standard
        mnemo = Mnemonic()
        mnemonic = mnemo.generate(strength=256)

        # Create the wallet using the generated mnemonic
        wallet = Wallet.create(wallet_name, keys=mnemonic, network='bitcoin')
        print(f"Wallet created: {wallet.name}")

        # Save the mnemonic to a file in the wallets directory
        file_path = os.path.join(storage_dir, f"{wallet_name}_seed.txt")
        with open(file_path, "w") as file:
            file.write("Your Bitcoin Wallet Seed Phrase:\n")
            file.write(mnemonic)
        print(f"Seed phrase stored securely in '{file_path}'.")
        print(f"Address: {wallet.get_key().address}")

    except WalletError as e:
        print(f"Error creating wallet: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def list_wallets() -> None:
    """List all existing wallets without showing QR codes."""
    try:
        wallets = wallets_list()
        if wallets:
            print("Existing wallets:")
            for wallet_data in wallets:
                wallet_name = wallet_data.get('name')
                if wallet_name:
                    try:
                        wallet = Wallet(wallet_name)
                        public_address = wallet.get_key().address
                        print(f"- {wallet_name}: {public_address}")
                    except Exception as e:
                        print(f"  Unable to retrieve address for wallet '{wallet_name}': {e}")
        else:
            print("No wallets found.")
    except Exception as e:
        print(f"Error listing wallets: {e}")


def retrieve_secret_words(wallet_name: str) -> None:
    """Retrieve the secret words (mnemonic phrase) for an existing wallet and show QR code."""
    try:
        storage_dir = get_default_wallet_storage()
        seed_file = os.path.join(storage_dir, f"{wallet_name}_seed.txt")

        if os.path.exists(seed_file):
            with open(seed_file, "r") as file:
                seed_phrase = file.read().strip()
            print(f"Mnemonic (secret words) for wallet '{wallet_name}':\n{seed_phrase}")

            # Generate and display the QR code for the address
            wallet = Wallet(wallet_name)
            public_address = wallet.get_key().address
            print(f"Public address: {public_address}")
            qr = qrcode.QRCode()
            qr.add_data(public_address)
            qr.make(fit=True)
            qr.print_ascii()

        else:
            print(f"No seed file found for wallet '{wallet_name}'. The wallet might not have been created with a mnemonic.")
    except Exception as e:
        print(f"Unexpected error: {e}")


def print_wallet_path(wallet_name: str) -> None:
    """Print the file path to a specific wallet."""
    try:
        storage_dir = get_default_wallet_storage()
        wallet_file = os.path.join(storage_dir, f"{wallet_name}.wallet")

        if os.path.exists(wallet_file):
            print(f"Path to wallet '{wallet_name}': {wallet_file}")
        else:
            print(f"Wallet '{wallet_name}' does not exist at the expected location: {wallet_file}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def main() -> None:
    """Main function to handle commands."""
    parser = argparse.ArgumentParser(
        description="Bitcoin Wallet Manager - Create, manage, and retrieve Bitcoin wallets",
        epilog="Example usage:\n  python wallet.py --create MyNewWallet\n  python wallet.py --list\n  python wallet.py --retrieve MyNewWallet\n  python wallet.py --path MyNewWallet",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--create",
        metavar="WALLET_NAME",
        type=str,
        help="Create a new wallet with the specified name.\n"
             "Example: python wallet.py --create MyWallet"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all existing wallets without QR code.\n"
             "Example: python wallet.py --list"
    )
    parser.add_argument(
        "--retrieve",
        metavar="WALLET_NAME",
        type=str,
        help="Retrieve the mnemonic (secret words) for the specified wallet and show QR code.\n"
             "Example: python wallet.py --retrieve MyWallet"
    )
    parser.add_argument(
        "--path",
        metavar="WALLET_NAME",
        type=str,
        help="Print the file path to the specified wallet.\n"
             "Example: python wallet.py --path MyWallet"
    )

    args = parser.parse_args()

    if args.create:
        create_wallet(args.create)
    elif args.list:
        list_wallets()
    elif args.retrieve:
        retrieve_secret_words(args.retrieve)
    elif args.path:
        print_wallet_path(args.path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
