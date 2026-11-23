
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def get_kpis():
    response = requests.get(f"{API_URL}/api/kpis")
    response.raise_for_status()
    return response.json()


def get_monthly_revenue():
    response = requests.get(f"{API_URL}/api/monthly-revenue")
    response.raise_for_status()
    return response.json()


def get_top_products():
    response = requests.get(f"{API_URL}/api/top-products")
    response.raise_for_status()
    return response.json()


def get_top_countries():
    response = requests.get(f"{API_URL}/api/top-countries")
    response.raise_for_status()
    return response.json()


def get_customer_analysis():
    response = requests.get(f"{API_URL}/api/customer-analysis")
    response.raise_for_status()
    return response.json()


# Get Year and Country Filter Options
def get_filter_options():
    response = requests.get(
        f"{API_URL}/api/filter-options"
    )
    response.raise_for_status()
    return response.json()


# Get Filtered Dashboard Data
def get_dashboard_data(year=None, country=None):

    params = {}

    if year is not None:
        params["year"] = year

    if country is not None:
        params["country"] = country

    response = requests.get(
        f"{API_URL}/api/dashboard-data",
        params=params
    )

    response.raise_for_status()
    return response.json()
