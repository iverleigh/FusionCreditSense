# coding: utf-8

from datetime import datetime
import random
import requests
import string
import uuid


def random_chars(count):
    return "".join(random.choice(string.ascii_letters) for x in range(count))


def random_digits(count):
    return "".join(random.choice('0123456789') for x in range(count))


def build_request_url(path, api):
    url = "https://api.preprod.fusionfabric.cloud"

    if path.startswith('/'):
        url += path
    else:
        url += '/' + path

    if url.endswith('/'):
        url += 'v1'
    else:
        url += '/v1'

    if api.startswith('/'):
        url += api
    else:
        url += '/' + api

    return url


def authenticate():
    url = build_request_url('login', 'sandbox/oidc/token')
    print("\nRequesting FFDC Access Token from: {}".format(url))

    data = {
        "grant_type": "client_credentials",
    }
    client_id = "c2775483-dbe1-458c-933b-e12572bd28b8"
    client_secret = "e3aeefeb-fc43-44a6-bbc4-9523e6512d98"

    response = requests.post(url, data=data, auth=(client_id, client_secret), verify=False, allow_redirects=False)
    print(response.status_code)
    if response.status_code != 200:
        print(response.reason)
        print(response.text)
        return None
    response_data = response.json()
    access_token = response_data['access_token']
    request_id = str(uuid.uuid4())
    idempotency_key = uuid.uuid4().hex

    print("access_token: {}".format(access_token))
    print("request_id: {}".format(request_id))
    print("idempotency_key: {}".format(idempotency_key))

    headers = {
        'Authorization': 'Bearer ' + access_token,
        'X-Request-ID': request_id,
        'Idempotency-Key': idempotency_key,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    return headers


def find_customer(first_name, last_name, headers):
    url = build_request_url('retail-banking/customers', 'personal-customers/dedup')

    print("\nSearching for customer details matching first_name {} and last_name {}".format(
        repr(first_name),
        repr(last_name),
    ))

    data = {
        "firstName": first_name,
    }
    if last_name:
        data["lastName"] = last_name

    print("Calling: {}".format(url))
    response = requests.post(url, json=data, headers=headers, verify=False, allow_redirects=False)

    customer = None
    if response.status_code == 200:
        print("Customer found")
        response_data = response.json()
        customer = response_data["items"][0]
    elif response.status_code == 404:
        print("No customer found")
    else:
        print(response.status_code)
        print(response.reason)
        print(response.text)
        raise Exception("Error when searching for customer: {}".format(response.status_code))

    return customer


def register_customer(first_name, last_name, headers):
    print("\nRegistering customer...")

    url = build_request_url('retail-banking/customers', 'personal-customers')
    data = {
        "firstName": first_name,
        "title": "Mr",
        "dateOfBirth": "1980-06-01",
        "gender": "UNDISCLOSED",
        "countryOfResidency": "US",
        "identification": {
            "type": "SOSE",
            "id": random_chars(3) + random_digits(5),
        },
        "kycCheckRequired": "NOT-REQUIRED",
        "addresses": [{
            "addressType": "RESIDENTIAL",
            "country": "US",
            "line1": "Building",
            "line2": "Street",
            "line3": "",
            "line4": "City",
            "line5": "State",
            "postalCode": "12345",
            "buildingNumber": "",
        }],
        "phoneNumbers": [{
            "type": "MOBILE",
            "number": random_digits(8),
        }],
        "emailAddresses": [{
            "type": "HOME",
            "address": "{}{}@{}.example.com".format(first_name, last_name, random_chars(3)),
        }],
        "fatcaDetails": {
            "isUSResident": True,
            "isUSTaxResident": True,
            "tin": random_digits(10),
        },
    }
    if last_name:
        data["lastName"] = last_name

    print("Calling: {}".format(url))
    response = requests.post(url, json=data, headers=headers, verify=False, allow_redirects=False)

    customer = None
    if response.status_code == 201:
        customer = response.json()
        print("Customer registered")
    else:
        print(response.status_code)
        print(response.reason)
        print(response.text)
        raise Exception("Error when registering customer: {}".format(response.status_code))

    return customer


def list_loans(customer_id, headers):
    print("\nRetrieving a list of loans for customer ID {}".format(customer_id))

    url = build_request_url('retail-banking/loans', 'loans/{}/accounts'.format(customer_id))

    print("Calling: {}".format(url))
    response = requests.get(url, headers=headers, verify=False, allow_redirects=False)

    loans = None
    if response.status_code == 200:
        print(response.json())
    elif response.status_code == 400:
        # Looks like the loan doesn't exist
        print("No loans found (code 400)")
    else:
        print(response.status_code)
        print(response.reason)
        print(response.text)
        raise Exception("Error when retrieving customer loans: {}".format(response.status_code))

    return loans


def create_loan(customer_id, loan_amount, account, headers):
    print("\nCreating a new loan for customer ID {}".format(customer_id))

    # For debug
    url = build_request_url('retail-banking/product-information', 'products/loans')
    print("Calling: {}".format(url))
    response = requests.get(url, headers=headers, verify=False, allow_redirects=False)
    print("Available products")
    if response.status_code == 200:
        response_data = response.json()
        for product in response_data["items"]:
            print(product["productId"])
    else:
        print(response.status_code)
        print(response.reason)
        print(response.text)

    start_date = datetime.now().date()

    url = build_request_url('retail-banking/loans', 'loans')
    data = {
        "loanApplicantIds": [{
            "customerId": customer_id,
        }],
        "productCode": "05020DEFAULTUSD",
        "loanRequestAmount": {
            "amount": int(loan_amount),
            "currency": "USD",
        },
        "loanTerm": {
            "calendarPeriod": "MONTH",
            "value": 12,
        },
        "repaymentFrequency": "MONTHLY",
        "repaymentAccount": account,
        "feeCollectionAccount": account,
        "disbursementScheduleRequest": [{
            "disbursementDate": start_date.strftime("%Y-%m-%d"),
            "disbursementAmount": {
                "amount": int(loan_amount),
                "currency": "USD",
            },
            "disbursementType": "TRANSFER",
        }],
    }

    print("Calling: {}".format(url))
    response = requests.post(url, json=data, headers=headers, verify=False, allow_redirects=False)

    loan = None
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.status_code)
        print(response.reason)
        print(response.text)
        raise Exception("Error when creating customer loan: {}".format(response.status_code))

    return loan
