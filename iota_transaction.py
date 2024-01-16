import os

from dotenv import load_dotenv

from iota_sdk import SendParams, Wallet

load_dotenv()

# This example sends a transaction.

wallet = Wallet(os.environ['WALLET_DB_PATH'])

account = wallet.get_account('TestCR23')

# Sync account with the node
response = account.sync()

if 'STRONGHOLD_PASSWORD' not in os.environ:
    raise Exception(".env STRONGHOLD_PASSWORD is undefined, see .env.example")

wallet.set_stronghold_password(os.environ["STRONGHOLD_PASSWORD"])

params = [SendParams(
    address="rms1qry52gw8sq9xrx6jj833szff0kkaqfdlyx5kum52nwc6y47ezh7pylprqr3",
    amount=1000000,
)]

transaction = account.send_with_params(params)
print(f'Block sent: {os.environ["EXPLORER_URL"]}/block/{transaction.blockId}')
