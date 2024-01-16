import os
import sys 
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from iota_sdk import (ClientOptions, CoinType, StrongholdSecretManager, Utils,
                              Wallet)

load_dotenv()

# A name to associate with the created account.


if len(sys.argv) == 2:
        ACCOUNT_ALIAS = sys.argv[1]

#coin_type = CoinType.SHIMMER
# The node to connect to.
#node_url = os.environ.get('NODE_URL', 'https://api.testnet.shimmer.network')
node_url = os.environ.get('NODE_URL', 'http://35.194.18.16:14265')
#encrypted_password = os.environ.get('STRONGHOLD_PASSWORD').encode('utf-8')
#secret_key = os.environ.get('SECRET_KEY').encode('utf-8')
#cipher = Fernet(secret_key)
#ciphet = Fernet(key)
#decrypted_password = cipher.decrypt(encrypted_password).decode()
#print("DE",decrypted_password)
#try:
STRONGHOLD_PASSWORD = os.environ.get(
        'STRONGHOLD_PASSWORD', 'TangleCR23')

    #The path to store the account snapshot.
STRONGHOLD_SNAPSHOT_PATH = 'vault.stronghold'

# Setup Stronghold secret manager
secret_manager = StrongholdSecretManager(
            STRONGHOLD_SNAPSHOT_PATH, STRONGHOLD_PASSWORD)

# Set up and store the wallet.
client_options = ClientOptions(nodes=[node_url])

wallet = Wallet(
    os.environ['WALLET_DB_PATH'],        
    client_options=client_options,
    coin_type=CoinType.SHIMMER,
    secret_manager=secret_manager
    )

# Generate a mnemonic and store its seed in the Stronghold vault.
# INFO: It is best practice to back up the mnemonic somewhere secure.
#mnemonic = Utils.generate_mnemonic()
#print(f'Mnemonic: {mnemonic}')
#wallet.store_mnemonic(mnemonic)

# Create an account.
account = wallet.create_account(ACCOUNT_ALIAS)
print("Account created:", account.get_metadata())

# Get the first address and print it.
address = account.addresses()[0]
print(f'Address:\n{address.address}')
