# Usage: python bank_data_generator.py <number_of_accounts> <max_num_transactions_per_account>
import os
import sys
import json
import string
import random
import datetime
from decimal import Decimal

KEYS = [
    'status', 
    'merchant_category_code', 
    'description', 
    'reference', 
    'remittance_info', 
    'currency', 
    'value_datetime', 
    'address', 
    'bank_transaction_issuer', 
    'booking_datetime', 
    'transaction_type', 
    'note', 
    'amount', 
    'bank_transaction_code', 
    'merchant_name'
]

POSITIVE_BANK_CODES = [
    "CR", # Automated Credit
    "DD", # Direct Debit
    "SO" # Standing Order
]

BLANKS = [
    "merchant_name",
    "merchant_category_code",
    "remittance_info",
    "address",
    "reference",
]

ISSUERS = ["LBG", "RBS", "TCB", "HFX"]
CHOICES = string.ascii_letters + string.digits
REF_PATTERN = [8, 4, 4, 4, 12]

accounts, transactions_max = sys.argv[1:]


for index in range(int(accounts)):
    reference = []
    for length in REF_PATTERN:
        reference.append(''.join(random.choice(CHOICES) for x in range(length)))
    reference = '-'.join(reference)

    counter = random.randint(3, int(transactions_max))
    print("Preparing {counter} transactions for account {reference}".format(
        counter=counter,
        reference=reference,
    ))

    account_transactions = []    
    for i in range(counter):
        trx = {}
        trx.update({key: "" for key in BLANKS})
        trx.update({
            "note": "{}{}{}".format(
                random.choice(string.ascii_uppercase),
                random.choice(string.ascii_uppercase),
                random.randint(1, 10),
            ),
            "status": "BOOKED",
            "bank_transaction_issuer": ISSUERS[random.randint(0, len(ISSUERS) - 1)],
            "description": "{}{}{}".format(
                random.choice(string.ascii_uppercase),
                random.choice(string.ascii_uppercase),
                random.randint(1, 10)
            ),
            "transaction_type": "Debit",
            "currency": "GBP",
            "value_datetime": None,
        })

        date = datetime.date(2020, random.randint(1,12), random.randint(1, 29))
        time = "{hours}:{minutes}:{seconds}".format(
            hours="{}".format(datetime.timedelta(hours=random.randrange(23))),
            minutes="{}".format(datetime.timedelta(minutes=random.randrange(60))),
            seconds="{}".format(datetime.timedelta(seconds=random.randrange(60)))
        )
        trx["booking_datetime"] = "{}T{}".format(date, time)

        if random.choice([True, False, False, False]):
            code = POSITIVE_BANK_CODES[random.randint(0, len(POSITIVE_BANK_CODES) - 1)]
        else:
            code = "{}{}".format(
                random.choice(string.ascii_uppercase),
                random.choice(string.ascii_uppercase)
            )
        trx["bank_transaction_code"] = code

        if random.choice([True, False, False, False, False]):
            prefix = ""
        else:
            prefix = "-"

        part_1 = float(Decimal(random.randrange(10, 1500))/100)
        part_2 = float(Decimal(random.randrange(10, 1500)))
        amount_value = "{prefix}{amount}".format(
            prefix=prefix,
            amount=part_1 + part_2
        )

        trx["amount"] = amount_value
        account_transactions.append(trx)
    
    # Now we write the transactions to a file
    with open(os.path.join("FAKE_BANK", "{reference}.json".format(reference=reference)), "w") as file_handler:
        file_handler.write(json.dumps(account_transactions))

