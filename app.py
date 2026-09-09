import os
import time
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
        return data["token"]
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
            
            <!-- Header -->
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
                        <p class="text-slate-400 text-xs">Malipo Salama</p>
                    </div>
                    <span class="bg-amber-50 text-amber-700 text-xs font-bold px-3 py-1 rounded-full">Live</span>
                </div>

                <form action="/lipa" method="POST" class="space-y-6">

                    <!-- Chagua Kiasi -->
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-3">Chagua Kiasi (TZS)</label>
                        <div class="grid grid-cols-3 gap-3">
                            <label class="cursor-pointer">
                                <input type="radio" name="amount" value="500" class="peer sr-only" required>
                                <div class="border-2 border-slate-200 peer-checked:border-amber-500 peer-checked:bg-amber-50 rounded-2xl py-4 text-center font-bold text-slate-700 peer-checked:text-amber-600 transition-all hover:border-amber-300">
                                    500
                                </div>
                            </label>
                            <label class="cursor-pointer">
                                <input type="radio" name="amount" value="1000" class="peer sr-only">
                                <div class="border-2 border-slate-200 peer-checked:border-amber-500 peer-checked:bg-amber-50 rounded-2xl py-4 text-center font-bold text-slate-700 peer-checked:text-amber-600 transition-all hover:border-amber-300">
                                    1,000
                                </div>
                            </label>
                            <label class="cursor-pointer">
                                <input type="radio" name="amount" value="10000" class="peer sr-only">
                                <div class="border-2 border-slate-200 peer-checked:border-amber-500 peer-checked:bg-amber-50 rounded-2xl py-4 text-center font-bold text-slate-700 peer-checked:text-amber-600 transition-all hover:border-amber-300">
                                    10,000
                                </div>
                            </label>
                        </div>
                    </div>

                    <!-- Chagua Mtandao -->
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Chagua Mtandao</label>
                        <select name="network" required
                            class="w-full border border-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-amber-400">
                            <option value="">-- Chagua Mtandao --</option>
                            <option value="MPESA">Vodacom M-Pesa</option>
                            <option value="AIRTEL">Airtel Money</option>
                            <option value="TIGO">Tigo Pesa / Mixx</option>
                            <option value="HALOPESA">Halopesa</option>
                        </select>
                    </div>

                    <!-- Namba ya Simu -->
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Namba ya Simu ya Kulipia</label>
                        <input type="tel" name="phone" placeholder="07XXXXXXXX" required
                            class="w-full border border-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-amber-400"
                            pattern="[0-9]{10}" maxlength="10">
                        <p class="text-xs text-slate-400 mt-1">Andika namba kuanzia 07...</p>
                    </div>

                    <button type="submit"
                        class="w-full bg-slate-900 hover:bg-amber-500 text-white hover:text-slate-900 font-bold py-4 px-6 rounded-2xl transition-all">
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

    phone = request.form.get("phone", "").strip()
    amount = request.form.get("amount", "").strip()

    if not phone:
        return jsonify({"error": "Namba ya simu inahitajika"}), 400
    if not amount:
        return jsonify({"error": "Chagua kiasi"}), 400

    # Badilisha 07... kuwa 2557...
    if phone.startswith("0"):
        phone = "255" + phone[1:]
    elif phone.startswith("+255"):
        phone = phone[1:]
    elif not phone.startswith("255"):
        phone = "255" + phone

    try:
        token = get_clickpesa_token()

        url = "https://api.clickpesa.com/third-parties/payments/initiate-ussd-push-request"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        payload = {
            "amount": amount,
            "currency": "TZS",
            "orderReference": f"ODA{int(time.time())}",
            "phoneNumber": phone
        }

        response = requests.post(url, json=payload, headers=headers, timeout=20)
        data = response.json()

        if response.status_code in [200, 201]:
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
            <div class="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                <span class="text-3xl text-green-600">✓</span>
            </div>
            <h1 class="text-2xl font-bold text-slate-800 mb-2">Ombi la Pesa Limeshushwa!</h1>
            <p class="text-slate-500 text-sm mb-6">
                Angalia simu yako sasa. Ujumbe wa PIN utajitokeza.<br>
                Ingiza namba yako ya siri kukamilisha malipo.
            </p>
            <a href="/" class="inline-block bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold py-3 px-6 rounded-xl">
                Rudi Nyumbani
            </a>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
