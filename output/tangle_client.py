import os

from dotenv import load_dotenv

from iota_sdk import (RemainderValueStrategy, TaggedDataPayload,
                      TransactionOptions, Wallet, utf8_to_hex)

load_dotenv()

# This example sends a transaction with a tagged data payload.
bl = 'testcr1'
wallet = Wallet(os.environ[bl])
ac = 'TestCR'
account = wallet.get_account(ac)

# Sync account with the node
response = account.sync()

if 'STRONGHOLD_PASSWORD' not in os.environ:
    raise Exception(".env STRONGHOLD_PASSWORD is undefined, see .env.example")

wallet.set_stronghold_password(os.environ["STRONGHOLD_PASSWORD"])

params = [{
    "address": "moon about angle reduce door rifle crane alter leader exit poem practice album find elite bitter wonder picnic face spread armed quantum wash pony",
    "amount": "100",
}]

transaction = account.send_with_params(params, TransactionOptions(remainder_value_strategy=RemainderValueStrategy.ReuseAddress,
                                                                  note="my first tx", tagged_data_payload=TaggedDataPayload(utf8_to_hex("tag"), utf8_to_hex("data"))))
print(transaction)
print(f'Block sent: {os.environ["EXPLORER_URL"]}/block/{transaction.blockId}')