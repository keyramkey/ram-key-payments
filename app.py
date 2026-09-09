import os
import requests
from flask import Flask, jsonify, redirect, request

app = Flask(__name__)

CLICKPESA_CLIENT_ID = os.environ.get("CLICKPESA_CLIENT_ID")
CLICKPESA_API_KEY = os.environ.get("CLICKPESA_API_KEY")

def get_clickpesa_token():
    """Generate JWT token from ClickPesa"""
    url = "https://api.clickpesa.com/third-parties/generate-token"
    headers = {
        "client-id": CLICKPESA_CLIENT_ID,
        "api-key": CLICKPESA_API_KEY
    }
    response = requests.post(url, headers=headers, timeout=15)
    data = response.json()
    
    if response.status_code == 200 and "token" in data:
        return data["token"]  # already includes "Bearer "
    else:
        raise Exception(f"Imeshindwa kupata token: {data}")

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="sw">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Malipo Salama | RAM KEY</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-50 min-h-screen flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl shadow-xl max-w-md w-full overflow-hidden border border-slate-100">
            <div class="bg-gradient-to-r from-amber-500 to-yellow-400 p-8 text-center">
                <div class="inline-flex items-center justify-center w-16 h-16 bg-white rounded-2xl shadow-md mb-4">
                    <span class="text-2xl font-bold text-amber-600">R</span>
                </div>
                <h1 class="text-white text-2xl font-bold">RAM KEY Store</h1>
                <p class="text-amber-50 text-sm mt-1">Lango Salama la Malipo</p>
            </div>
            <div class="p-8">
                <div class="flex justify-between items-center border-b pb-4 mb-6">
                    <div>
                        <h2 class="text-slate-800 font-semibold text-lg">Premium Service Access</h2>
                        <p class="text-slate-400 text-xs">Namba ya Oda: #ODA-1002</p>
                    </div>
                    <span class="bg-amber-50 text-amber-700 text-xs font-bold px-3 py-1 rounded-full">Live</span>
                </div>
                <div class="space-y-4 mb-8">
                    <div class="flex justify-between text-sm">
                        <span class="text-slate-500">Mteja:</span>
                        <span class="text-slate-800 font-medium">Keya Ramadhan</span>
                    </div>
                    <div class="flex justify-between text-sm">
                        <span class="text-slate-500">Simu:</span>
                        <span class="text-slate-800 font-medium">+255 561 586 4403</span>
                    </div>
                    <div class="flex justify-between items-baseline pt-4 border-t border-dashed">
                        <span class="text-slate-800 font-bold">Jumla Kuu:</span>
                        <span class="text-amber-500 font-extrabold text-2xl">TZS 5,000</span>
                    </div>
                </div>
                <form action="/lipa" method="POST">
                    <button type="submit" class="w-full bg-slate-900 hover:bg-amber-500 text-white hover:text-slate-900 font-bold py-4 px-6 rounded-2xl transition-all">
                        Lipia Sasa na Mobile Money
                    </button>
                </form>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/lipa", methods=["POST"])
def lipa():
    if not CLICKPESA_CLIENT_ID or not CLICKPESA_API_KEY:
        return jsonify({"error": "Credentials hazipo"}), 500

    try:
        # 1. Pata Token
        token = get_clickpesa_token()

        # 2. Tuma USSD Push moja kwa moja
        url = "https://api.clickpesa.com/third-parties/payments/initiate-ussd-push-request"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        payload = {
            "amount": "5000",
            "currency": "TZS",
            "orderReference": "ODA1002",          # alphanumeric tu
            "phoneNumber": "2555615864403"        # bila + 
        }

        response = requests.post(url, json=payload, headers=headers, timeout=20)
        data = response.json()

        if response.status_code in [200, 201]:
            # Mafanikio → onyesha ukurasa wa asante ndani ya app yako
            return redirect("/asante")
        else:
            return jsonify({
                "error": "ClickPesa imekataa muamala",
                "sababu": data,
                "status_code": response.status_code
            }), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/asante")
def asante():
    return """
    <!DOCTYPE html>
    <html lang="sw">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Asante</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-50 min-h-screen flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl shadow-xl p-8 max-w-md w-full text-center">
            <h1 class="text-2xl font-bold text-slate-800 mb-2">Ombi la Pesa Limeshushwa!</h1>
            <p class="text-slate-500 text-sm mb-6">
                Angalia simu yako sasa. Ujumbe wa PIN utajitokeza.
            </p>
            <a href="/" class="inline-block bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold py-3 px-6 rounded-xl">
                Rudi Nyumbani
            </a>
        </div>
    </body>
    </html>
    """
