#/home/tangle/iota_fin_venv/bin/python3
from iota_sdk import Utils

# Generate a random BIP39 mnemonic
mnemonic = Utils.generate_mnemonic()
print(f'Mnemonic: {mnemonic}')


