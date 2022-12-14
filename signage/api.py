

import requests
from requests.auth import HTTPBasicAuth

api_key = 'bce660b85f82672a1f80'
secret_key = '553abed2cdc21939a67c5eb229d1805a'
redirect_url = "http://127.0.0.1:8000/"

get_products_endpoint = 'https://payments.pabbly.com/api/v1/products'
create_plans_endpoint = 'https://payments.pabbly.com/api/v1/plan/create'
list_plans_endpoint = "https://payments.pabbly.com/api/v1/plans/"
verify_hostpage_endpoint = 'https://payments.pabbly.com/api/v1/verifyhosted'


product_id = "6323c05faa64707d65153561"


def create_host_plan(plan_name, price):
    basic = HTTPBasicAuth(api_key, secret_key)
    product_id = "6323c05faa64707d65153561"
    plan_code = "signage_" + plan_name.replace(" ", "_")
    data = {
            "product_id": product_id,
            "plan_name": plan_name,
            "plan_code": plan_code,
            "plan_type": "flat_fee",
            "billing_cycle": "lifetime",
            "billing_cycle_num": "2",
            "price": price,
            "billing_period": "y",
            "billing_period_num": "1",
            "plan_active": "true",
            "plan_description": "",
            "redirect_url": "http://127.0.0.1:8000/success",
            "currency_code": "USD",
            "meta_data": 
            {
                "value1":"{value_details}", 
                "value2":"{value_details}", 
                "value3":"{value_details}"
            }
        }
    response = requests.post(create_plans_endpoint, auth=basic, data=data)
    print(response.json())
    return response.json()

def fetch_plans_list():
    
    
    url = f"{list_plans_endpoint}{product_id}"
    basic = HTTPBasicAuth(api_key, secret_key)
    response = requests.get(url, auth=basic)
    

    return response.json()


def sync_plans():
    pass

def verify_hosted_page(hostedpage):
    basic = HTTPBasicAuth(api_key, secret_key)
    
    data = {
        "hostedpage": hostedpage
            
    }
    response = requests.post(verify_hostpage_endpoint, auth=basic, data=data)
    print(response.json())
    return response.json()

def check_subscription_status(subscription_id):
    basic = HTTPBasicAuth(api_key, secret_key)


    check_subscription_endpoint = f"https://payments.pabbly.com/api/v1/subscription/{subscription_id}"
    
    response = requests.post(check_subscription_endpoint, auth=basic)
    print(response.json())
    return response.json()

def fetch_all_subscriptions():
    basic = HTTPBasicAuth(api_key, secret_key)
    list_subscriptions_endpoint = "https://payments.pabbly.com/api/v1/subscriptions"

    response = requests.get(list_plans_endpoint, auth=basic)
    print(response.json())

    return response.json()


if __name__ == "__main__":
    check_subscription_status("634841861b32b359198bf9d0")