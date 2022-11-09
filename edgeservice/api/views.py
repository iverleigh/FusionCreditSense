import json
from requests import get
import traceback
from decimal import Decimal
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .temp_constants import ACCOUNT_MAPPING
from .utils import (
    get_authentication,
    build_request_url,
    retrieve_serialised_dataset,
    send_for_analysis,
    predict_credit_line,
)
from api import ffdc_utils


class AbstractOpenBankingAPIView(APIView):
    
    def get(self, request, format=None):
        """
        Process a get request to this URL. 
        This is the superclass version of the get request and as such
        is only used for handling things which are required by ALL 
        API views, and not just a select few.
        @param request: HTTPRequest object containing request details
        @param format: The format in which the data is to be returned.
        @returns nothing here as it must be subclassed. Doing it this way prevents
                        incorrect use.
        """
        self.reathorise_token(request)
        # Child classes will override the functionality from here
    
    def reathorise_token(self, request, re_auth=False):
        """
        Process the information provided in the session and the request
        in order to associate a session token with the remote (third party)
        open banking system.
        This is currently configured to work with Finastra's Fusion OpenBanking 
        system but could be configured for use with other OB systems if necessary.
        
        @param request: HTTPRequest object containing request details
        @param re_auth: Has the token expired and therefore we need to 
                                     retrieve a new one?
        """
        # Company has to be set first to perform authorisation
        if request.session.get("company") in (None, "", "None"):
            request.session.update({"company": request.GET.get("company", "")})
        
        if request.session.get("headers") in (None, "", "None") or re_auth:
            # Only re-auth if the session has lost it's token
            token = get_authentication(
                request.session.get("company"), 
                request.GET.get("username"), request.GET.get("password")
            )

            headers = {
                "Authorization": "Token {}".format(token)
            }
    
            # We want to create a new session which passes the authorisation token in
            request.session.update({"headers": headers})
        self.headers = request.session["headers"]
        self.company = request.session["company"]


class GetBanks(AbstractOpenBankingAPIView):
    """
    View to list all the accounts that we have access to
    * Requires token authentication with the open banking system
    """
    def get(self, request, format=None):
        """
        Process a get request to this URL. This will build a request to the
        open banking system and return the available banks.
        @param request: HTTPRequest object containing request details
        @param format: The format in which the data is to be returned.
        @return a HTTPResponse object for interpretation in the screens
        """
        super(GetBanks, self).get(request, format=format)
        url = build_request_url(self.company, "banks/")
        banks_data = json.loads(get(url, headers=self.headers).content)
        if banks_data.get("detail") == "Invalid token":
            self.reathorise_token(request, re_auth=True)
            banks_data = json.loads(get(url, headers=self.headers).content)
        banks = retrieve_serialised_dataset(banks_data["banks"], ["name"])
        return Response(banks)


class GetAccounts(AbstractOpenBankingAPIView):
    """
    View to list all users in the system.
    * Requires token authentication with the open banking system
    """
    
    def get(self, request, format=None):
        """
        Process a get request to this URL. This will build a request to the
        open banking system and return the account data from there.
        @param request: HTTPRequest object containing request details
        @param format: The format in which the data is to be returned.
        @return a HTTPResponse object for interpretation in the screens
        """
        super(GetAccounts, self).get(request, format=format)
        url = build_request_url(self.company, "accounts/")
        account_data = json.loads(get(url, headers=self.headers).content)
        if account_data.get("detail") == "Invalid token":
            self.reathorise_token(request, re_auth=True)
            account_data = json.loads(get(url, headers=self.headers).content)
        accounts = retrieve_serialised_dataset(
            account_data["accounts"], 
            ["reference", "name", "identifier_sort_code", "identifier_account_number"]
        )
        return Response(accounts)


class GetFinancialCredibility(AbstractOpenBankingAPIView):
    """
    View to retrieve the customer credibility index for this customer.
    We start by pulling their transactions and then do a request to the machine 
    learning algorithm to retrieve the information about the credibility of the customer.

    * Requires token authentication with the open banking system
    """

    def get(self, request, format=None):
        """
        Process a get request to this URL. This will build a request to the
        open banking system and return a list of all transactions for a specified
        account. It will then go off and pass that data along to the machine 
        learning algorithm.
        @param request: HTTPRequest object containing request details
        @param format: The format in which the data is to be returned.
        @return a HTTPResponse object for interpretation in the screens
        """
        super(GetFinancialCredibility, self).get(request, format=format)
        account_no = request.GET.get("accountNumber")
        sort_code = request.GET.get("sortCode")
        if settings.DEBUG:
            try:
                account_reference = ACCOUNT_MAPPING[(str(account_no), str(sort_code))]['reference']
            except KeyError:
                return Response(
                    {'detail': 'No matching account could be found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            raise NotImplementedError("We need to retrieve the account details from the openbanking system")

        suffix = "accounts/{account_reference}/transactions/".format(
            account_reference=account_reference 
        )
        url = build_request_url(self.company, suffix)
        try:
            trx_data = json.loads(get(url, headers=self.headers).content)
        except Exception:
            return Response(
                {'detail': 'Unable to retrieve transactions'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if trx_data.get("detail") == "Invalid token":
            self.reathorise_token(request, re_auth=True)
            trx_data = json.loads(get(url, headers=self.headers).content)
        
        trxs = trx_data["transactions"]
        # This may need encoding as a JSON response
        response = send_for_analysis(trxs)
        # We want to produce a percentage credibility here
        return Response({
            "account_ref": account_reference, 
            "score": Decimal(response["y_pred"][0] * 100).quantize(Decimal('.1')),
            "credit_line": "${}".format(response["cred_line_pred"][0]),
        })


class PredictCreditSuggestion(AbstractOpenBankingAPIView):
    """
    View to retrieve a prediction on a suggested line of credit for
    a customer.
    We start by pulling their transactions and then do a request to the machine 
    learning algorithm to retrieve the information about the what
    line of credit seems sensible based on their financial literacy.

    * Requires token authentication with the open banking system
    """

    def get(self, request, format=None):
        """
        Process a get request to this URL. This will build a request to the
        open banking system and return a list of all transactions for a specified
        account. It will then go off and pass that data along to the machine 
        learning algorithm.
        @param request: HTTPRequest object containing request details
        @param format: The format in which the data is to be returned.
        @return a HTTPResponse object for interpretation in the screens
        """
        # Not required as a single call to the ML service now return both the
        # credit score and suggested credit line

        # super(PredictCreditSuggestion, self).get(request, format=format)
        # account_reference = request.GET.get("accountReference")
        # 
        # suffix = "accounts/{account_reference}/transactions/".format(
        #     account_reference=account_reference 
        # )
        # url = build_request_url(self.company, suffix)
        # trx_data = json.loads(get(url, headers=self.headers).content)
        # if trx_data.get("detail") == "Invalid token":
        #     self.reathorise_token(request, re_auth=True)
        #     trx_data = json.loads(get(url, headers=self.headers).content)

        # trxs = trx_data["transactions"]
        # This may need encoding as a JSON response
        # response = predict_credit_line(trxs)
        # We want to produce a percentage credibility here
        return Response({"credit_line": "$10,000"})


class FFDCCustomer(AbstractOpenBankingAPIView):
    """
    Interact with FFDC Customer APIs

    Retrieves customer details if they are already registered, or registers
    them if they are not
    """
    def get(self, request, format=None):
        # Retrieve customer details
        name = request.GET.get("name", "")
        name_parts = name.split(" ")
        first_name = name_parts[0]
        last_name = ""
        if len(name_parts) > 1:
            last_name = " ".join(name_parts[1:])

        # Authenticate with FFDC APIs
        headers = ffdc_utils.authenticate()
        if headers is None:
            return Response({"success": False})

        # Attempt to find customer (de-duplication)
        try:
            customer = ffdc_utils.find_customer(first_name, last_name, headers)
        except Exception:
            traceback.print_exc()
            return Response({"success": False, "message": "Error when seraching for customer"})

        if customer is None:
            # Attempt to register customer
            try:
                customer = ffdc_utils.register_customer(first_name, last_name, headers)
            except Exception:
                traceback.print_exc()
                return Response({"success": False, "message": "Error when registering customer"})

        print("Customer: {}".format(customer))

        return Response({"success": True, "customer": customer})


class FFDCLoans(AbstractOpenBankingAPIView):
    """
    Interact with FFDC Loan APIs - currently not working
    """
    def get(self, request, format=None):
        customer_id = request.GET.get("customer_id", "")
        loan_amount = request.GET.get("loan_amount", "").replace("$", "")
        account = request.GET.get("account", "")

        # Authenticate with FFDC APIs
        headers = ffdc_utils.authenticate()
        if headers is None:
            return Response({"success": False})

        # Retrieve a list of current loans
        loans = None
        try:
            loans = ffdc_utils.list_loans(customer_id, headers)
        except Exception:
            traceback.print_exc()
            return Response({"success": False, "message": "Error when seraching for customer loans"})

        loan = None
        if not loans:
            # Create loan
            try:
                loan = ffdc_utils.create_loan(customer_id, loan_amount, account, headers)
            except Exception:
                traceback.print_exc()
                return Response({"success": False, "message": "Error when creating customer loan"})
        else:
            ### TODO
            print("Loans: {}".format(loans))

        return Response({"success": True, "loan": loan})
