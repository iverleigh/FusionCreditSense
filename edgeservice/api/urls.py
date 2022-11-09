from django.urls import include, path
from rest_framework import routers
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('banks', views.GetBanks.as_view()),
    path('accounts', views.GetAccounts.as_view()),
    path('checkhistory', views.GetFinancialCredibility.as_view()),
    path('predictcredit', views.PredictCreditSuggestion.as_view()),
    path('ffdc/customer', views.FFDCCustomer.as_view()),
    path('ffdc/loans', views.FFDCLoans.as_view()),
]
