from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()  

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    cf = fetch_conversion_factor(source_currency, target_currency)
    
    if cf is None:
        return "Sorry, couldn't fetch conversion factor.", 500

    final_amt = round(amount * cf, 2)
    response = {
        'fulfillmentText': f"{amount} {source_currency} is {final_amt} {target_currency}"
    }

    return jsonify(response)

def fetch_conversion_factor(source, target):
    api_key = os.getenv("CURRENCY_API_KEY")
    url = f"https://api.currencyapi.com/v3/latest?apikey={api_key}&base_currency={source}&currencies={target}"
    
    response = requests.get(url)
    try:
        data = response.json()
        return data['data'][target]['value']
    except (KeyError, ValueError) as e:
        print("Error in response:", e)
        return None

if __name__ == "__main__":
    app.run(debug=True)
