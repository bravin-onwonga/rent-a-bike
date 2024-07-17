#!/usr/bin/python3
"""Handles Mpesa payment"""

import base64
from datetime import datetime
from flask import abort, jsonify, request
from api.v1.views import app_views
import os
import requests
from requests.auth import HTTPBasicAuth

callback_url = "https://491e-197-232-28-159.ngrok-free.app"

payment_callback = {}


@app_views.route('/pay', strict_slashes=False, methods=["POST", "OPTIONS"])
def pay():
    """Initiates M-PESA Express request"""
    if request.method == "OPTIONS":
        return '', 200

    payment_data = request.get_json()

    global payment_callback
    payment_callback = {}

    if not payment_data:
        abort(400, 'Payment information missing')

    amount = payment_data.get('amount')
    phone_number = payment_data.get('phone_number')

    shortcode = os.getenv('SHORT_CODE')

    endpoint = ("https://sandbox.safaricom.co.ke/mpesa/" +
                "stkpush/v1/processrequest")
    access_token = get_access_token()
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    passkey = os.getenv("PASSKEY")
    password = ("174379" + passkey + timestamp).encode('utf-8')
    password = base64.b64encode(password).decode('utf-8')

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url + "/api/v1/callback",
        "AccountReference": "Rent A Bike",
        "TransactionDesc": "Bike Renting Fee"
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    print(response)
    return response.json(), 200


@app_views.route('/callback', strict_slashes=False, methods=['POST'])
def callback():
    """Handles callback from M-Pesa"""

    global payment_callback

    callback_data = request.get_json()

    if not callback_data:
        abort(404, "Not JSON")

    print("callback_data received")
    print()
    print(callback_data)
    payment_callback = callback_data

    print()

    print(payment_callback)

    return jsonify(callback_data), 200


@app_views.route('/check_payment', strict_slashes=False, methods=['GET'])
def check_payment():
    """Checks if callback data is received or not"""
    global payment_callback
    print("Payment callback Updated")
    print(payment_callback)
    return jsonify(payment_callback), 200


def get_access_token():
    """Gets access token for M-Pesa payment"""
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    endpoint = ("https://sandbox.safaricom.co.ke/oauth/v1/" +
                "generate?grant_type=client_credentials")

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
        print("Error:Here ", e)
        return None
