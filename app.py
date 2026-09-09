import os
import requests
from flask import Flask, jsonify, redirect, request

app = Flask(__name__)

# Soma credentials kutoka Environment Variables (salama zaidi)
CLICKPESA_CLIENT_ID = os.environ.get("CLICKPESA_CLIENT_ID")
CLICKPESA_API_KEY = os.environ.get("CLICKPESA_API_KEY")

# ⚠️ Badilisha URL hii kulingana na documentation ya ClickPesa yako
# (Inaweza kuwa https://api.clickpesa.com/... au endpoint nyingine)
CLICKPESA_API_URL = "https://api.clickpesa.com/third-parties/checkout/generate-link"  # Mfano - thibitisha!

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
        <style>
            body { font-family: 'Plus Jakarta Sans', sans-serif; }
        </style>
    </head>
    <body class="bg-slate-50 min-h-screen flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl shadow-xl shadow-slate-100 max-w-md w-full overflow-hidden border border-slate-100">
            <div class="bg-gradient-to-r from-amber-500 to-yellow-400 p-8 text-center relative overflow-hidden">
                <div class="inline-flex items-center justify-center w-16 h-16 bg-white rounded-2xl shadow-md mb-4">
                    <span class="text-2xl font-bold text-amber-600">R</span>
                </div>
                <h1 class="text-white text-2xl font-bold tracking-tight">RAM KEY Store</h1>
                <p class="text-amber-50 text-sm mt-1">Lango Salama la Malipo ya Mtandaoni</p>
            </div>
            <div class="p-8">
                <div class="flex justify-between items-center border-b border-slate-100 pb-4 mb-6">
                    <div>
                        <h2 class="text-slate-800 font-semibold text-lg">Premium Service Access</h2>
                        <p class="text-slate-400 text-xs mt-0.5">Namba ya Oda: #ODA-1002</p>
                    </div>
                    <span class="bg-amber-50 text-amber-700 text-xs font-bold px-3 py-1 rounded-full border border-amber-100">Live</span>
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
                    <div class="flex justify-between items-baseline pt-4 border-t border-dashed border-slate-100">
                        <span class="text-slate-800 font-bold text-base">Jumla Kuu:</span>
                        <span class="text-amber-500 font-extrabold text-2xl">TZS 5,000</span>
                    </div>
                </div>
                <form action="/lipa" method="POST">
                    <button type="submit" class="w-full bg-slate-900 hover:bg-amber-500 text-white hover:text-slate-900 font-bold py-4 px-6 rounded-2xl transition-all duration-300 transform active:scale-95 shadow-lg flex items-center justify-center gap-2">
                        <span>Lipia Sasa na Mobile Money</span>
                    </button>
                </form>
                <p class="text-center text-slate-400 text-xs mt-6">
                    Imelindwa na kusimbwa kwa usalama na ClickPesa
                </p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/lipa", methods=["POST"])
def lipa():
    if not CLICKPESA_CLIENT_ID or not CLICKPESA_API_KEY:
        return jsonify({"error": "Credentials hazipo. Weka Environment Variables."}), 500

    headers = {
        "X-Client-Id": CLICKPESA_CLIENT_ID,
        "Authorization": f"Bearer {CLICKPESA_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "totalPrice": 5000,
        "orderReference": "ODA-1002",
        "customerName": "Keya Ramadhan",
        "customerEmail": "keyaramadhani0@gmail.com",
        "customerPhone": "2555615864403",
        "description": "Malipo ya huduma kwenye RAM KEY App",
        "callbackUrl": "https://ram-key-payments-production.up.railway.app/asante",  # Badilisha baada ya ku-deploy
    }

    try:
        response = requests.post(CLICKPESA_API_URL, json=payload, headers=headers, timeout=30)
        data = response.json()

        if response.status_code in [200, 201] and "checkoutUrl" in data:
            return redirect(data["checkoutUrl"])
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
        <title>Malipo Yameanzishwa</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-50 min-h-screen flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl shadow-xl p-8 max-w-md w-full text-center border border-slate-100">
            <div class="w-20 h-20 bg-emerald-50 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
            </div>
            <h1 class="text-2xl font-bold text-slate-800 mb-2">Ombi la Pesa Limeshushwa!</h1>
            <p class="text-slate-500 text-sm mb-6">
                Tafadhali angalia simu yako sasa hivi. Ujumbe wa kukutaka uweke Namba ya Siri (PIN) utajitokeza.
            </p>
            <a href="/" class="inline-block bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold py-3 px-6 rounded-xl transition-all text-sm">
                Rudi Nyumbani
            </a>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
