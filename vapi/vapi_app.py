from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your actual Vapi API Key
VAPI_API_KEY = "285d859c-f5cd-412d-a73e-4048f792948d"

@app.route('/create-vapi-assistant', methods=['POST'])
def create_vapi_assistant():
    try:
        headers = {
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json"
        }

        # Sending empty JSON to match what works on Vapi's docs website
        payload = {}

        response = requests.post("https://api.vapi.ai/assistant", headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()

        return jsonify({
            "status": "success",
            "provider": "vapi",
            "assistant_id": data.get("id"),
            "details": data
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
