import json
import requests
from django.conf import settings

def get_authentication(company, username, password):
    """
    We need to repeatedly authenticate our session with 
    Fusion OpenBanking to ensure that we have access to the 
    system using the appropriate credentials. This happens in
    a specific way and as such a single function is used to streamline
    integration.
    @param company: String representing company name in URL
    @param username: The username to be used
    @param password: The password to be used
    @return the response token for use in validating the session
    """
    url = build_request_url(company, "obtain-auth-token/")
    body = {
        "username": username,
        "password": password
    }
    print("Making request to {url} for user {username}".format(
        url=url, username=username
    ))
    response = requests.post(url, data=body)
    print("Received response: {response} with content {content}".format(
        response=response, content=response.content
    ))
    # Return the response TOKEN for future requests
    return json.loads(response.content)["token"]

def build_request_url(company, endpoint):
    """
    Request URL's have the same basic formula when we're connecting to 
    the Fusion OpenBanking system. This function allows us to easily 
    modify the URL we're requesting in order to reach the appropriate
    endpoint.
    @param company: String representing the company to be used
    @param endpoint: The endpoint we're trying to reach
    @returns a URL string for the desired API endpoint
    """
    return settings.OPENBANKING_URL.format(company=company) + endpoint

def retrieve_serialised_dataset(dataset, keys):
    """
    Retrieving specific data from the open banking system can be 
    repetetive. This removes the need for that repetition by parsing 
    the data in a single consise way.
    @param dataset: The data we retrieved from the API (list of dictionaries)
    @param key: The key we want to retrieve from those objects
    @returns a list of objects with specific data that we need
    """
    values = [ { key: data[key] for key in keys } for data in dataset ]
    return values

def predict_credit_line(transactions):
    """
    Not required
    """
    return True

def send_for_analysis(transactions):
    """
    Transactions need to be sent to the machine learning algorithm in 
    order for them to be processed and a risk assessment score to be 
    provided. This happens at the same time as when we request the 
    data to be parsed onto the screen.
    @param transactions: A list of dictionaries containing transaction data
    @return a JSON object containing the response from the Machine Learning
    algorithm.
    """
    url = "{}/prepare_dataset".format(settings.ML_SERVICE_URL)
    print("Requesting analysis on {count} transactions via {url}".format(
        count=len(transactions),
        url=url
    ))
    response = requests.post(url, json={'transactions': transactions})
    print("Received response {response} from {url}".format(
        response=response.json(),
        url=url
    ))
    # Now we have our data frame, we want to pass it into the Machine Learning
    # algorithm
    url = "{}/pipe_predict".format(settings.ML_SERVICE_URL)
    print("Requesting analysis on {count} transactions via {url}".format(
        count=len(transactions),
        url=url
    ))
    print(response.json())
    response = requests.post(url, json=response.json())
    print("Received response {response} from {url}".format(
        response=response.json(),
        url=url
    ))
    return response.json()