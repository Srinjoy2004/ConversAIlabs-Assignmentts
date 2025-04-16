from flask import Flask, request, jsonify
import requests
from retell import Retell
from dotenv import load_dotenv
import os

app = Flask(__name__)


load_dotenv()

RETELL_API_KEY = os.getenv("RETELL_API_KEY")
RETELL_VOICE_ID = os.getenv("RETELL_VOICE_ID")
RETELL_LLM_ID = os.getenv("RETELL_LLM_ID")
VAPI_API_KEY = os.getenv("VAPI_API_KEY")


@app.route('/create-agent', methods=['POST'])
def create_agent():
    try:
        data = request.json
        provider = data.get("provider")

        if provider == "retell":
            # Retell agent creation
            client = Retell(api_key=RETELL_API_KEY)
            agent_response = client.agent.create(
                response_engine={
                    "llm_id": RETELL_LLM_ID,
                    "type": "retell-llm",
                },
                voice_id=RETELL_VOICE_ID,
            )

            return jsonify({
                "status": "success",
                "provider": "retell",
                "llm_id": RETELL_LLM_ID,
                "agent_id": agent_response.agent_id
            })

        elif provider == "vapi":
            # Vapi assistant creation
            headers = {
                "Authorization": f"Bearer {VAPI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {}  # Add custom payload if needed
            response = requests.post("https://api.vapi.ai/assistant", headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            return jsonify({
                "status": "success",
                "provider": "vapi",
                "assistant_id": result.get("id"),
                "details": result
            })

        else:
            return jsonify({"status": "error", "message": "Invalid provider. Choose 'retell' or 'vapi'."}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
