#!/usr/bin/python3
"""Handles Mpesa payment"""

import base64
from datetime import datetime
from flask import abort, jsonify, request
from api.v1.views import app_views
import os
import requests
from requests.auth import HTTPBasicAuth

callback_url = "https://192e-197-232-80-102.ngrok-free.app"


@app_views.route('/pay', strict_slashes=False)
def pay():
    """Initiates M-PESA Express request"""
    payment_data = {
        'phone': request.args.get('phone'),
        'amount': request.args.get('amount')
        }

    if not payment_data:
        abort(400, 'Payment information missing')

    amount = payment_data.get('amount')
    phone_number = payment_data.get('phone')
    shortcode = os.getenv('SHORT_CODE')

    endpoint = "https://sandbox.safaricom.co.ke/mpesa/stk\
        push/v1/processrequest"
    access_token = get_access_token()
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    passkey = "bfb279f9aa9bdbcf158e97dd71a467\
        cd2e0c893059b10f78e6b72ada1ed2c919"
    password = ("174379" + passkey + timestamp).encode('utf-8')
    password = base64.b64encode(password).decode('utf-8')

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url + "/api/v1/callback",
        "AccountReference": "Rent A Bike",
        "TransactionDesc": "Bike Renting Fee"
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    return response.json()


@app_views.route('/callback', methods=['POST'], strict_slashes=False)
def callback():
    """Handles callback from M-Pesa"""
    data = request.get_json()
    if data.get('ResponseCode') == '0':
        print("Hurray! Payment successful")
        return jsonify(data)
    else:
        return abort(400, "Request Incomplete")


def get_access_token():
    """Gets access token for M-Pesa payment"""
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    endpoint = "https://sandbox.safaricom.co.ke/oauth/v1/gener\
        ate?grant_type=client_credentials"

    try:
        res = requests.get(endpoint,
                           auth=HTTPBasicAuth(consumer_key,
                                              consumer_secret))
        data = res.json()
        return data['access_token']
    except requests.exceptions.HTTPError as err:
        status = err.response.status_code
        if (status >= 400):
            print("Error code:", status)
    except Exception as e:
        print("Error: ", e)
        return None
