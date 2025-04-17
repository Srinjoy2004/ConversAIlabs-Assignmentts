from flask import Flask, request, jsonify
import requests
from retell import Retell
from dotenv import load_dotenv
import os

# Initialize Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Load API keys and other required environment variables
RETELL_API_KEY = os.getenv("RETELL_API_KEY")
RETELL_VOICE_ID = os.getenv("RETELL_VOICE_ID")
RETELL_LLM_ID = os.getenv("RETELL_LLM_ID")
VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_VOICE_ID = os.getenv("VAPI_VOICE_ID")  

# Voice mapping configuration
# Maps standardized voice names to their provider-specific IDs
VOICE_MAP = {
    "default": {
        "retell": RETELL_VOICE_ID,
        "vapi": "default"
    },
    "elliot": {
        "vapi": "elliot-rime-ai"
    }
}

# LLM mapping configuration (currently only for Retell)
LLM_MAP = {
    "default": {
        "retell": RETELL_LLM_ID
    }
}

@app.route('/create-agent', methods=['POST'])
def create_agent():
    """
    Unified endpoint to create an AI agent using either Vapi or Retell
    based on the 'provider' field passed in the request body.
    """
    try:
        data = request.json
        provider = data.get("provider")
        voice_key = data.get("voice", "default")
        llm_key = data.get("llm", "default")

        # Validate provider input
        if provider not in ["retell", "vapi"]:
            return jsonify({
                "status": "error",
                "message": "Invalid provider. Choose 'retell' or 'vapi'."
            }), 400

        # Validate requested voice
        if voice_key not in VOICE_MAP:
            return jsonify({
                "status": "error",
                "message": f"Voice key '{voice_key}' is not supported. Available voices: {list(VOICE_MAP.keys())}"
            }), 400

        if provider not in VOICE_MAP[voice_key]:
            return jsonify({
                "status": "error",
                "message": f"Voice key '{voice_key}' is not supported for provider '{provider}'. Available voices for {provider}: {list(VOICE_MAP[voice_key].keys())}"
            }), 400

        # Validate LLM (only applicable for Retell)
        if provider == "retell" and (llm_key not in LLM_MAP or provider not in LLM_MAP[llm_key]):
            return jsonify({
                "status": "error",
                "message": f"LLM key '{llm_key}' is not supported for provider '{provider}'. Available LLMs: {list(LLM_MAP.keys())}"
            }), 400

        # Fetch resolved voice and LLM IDs from the mapping
        voice_id = VOICE_MAP[voice_key][provider]
        llm_id = LLM_MAP.get(llm_key, {}).get(provider)

        # RETELL implementation
        if provider == "retell":
            # Initialize Retell client with API key
            client = Retell(api_key=RETELL_API_KEY)

            # Create agent with voice and LLM info
            agent_response = client.agent.create(
                response_engine={
                    "llm_id": llm_id,
                    "type": "retell-llm"
                },
                voice_id=voice_id,
            )

            return jsonify({
                "status": "success",
                "provider": "retell",
                "id": agent_response.agent_id,
                "voice_id": voice_id,
                "llm_id": llm_id
            })

        # VAPI implementation
        elif provider == "vapi":
            # Prepare headers for Vapi request
            headers = {
                "Authorization": f"Bearer {VAPI_API_KEY}",
                "Content-Type": "application/json"
            }

            # Prepare payload to create Vapi assistant
            payload = {
                "name": "My Assistant",       # You may make this dynamic later
                "voice": voice_id,            # Voice ID as per user input mapping
                "model": "gpt-4"              # Hardcoded model for simplicity
            }

            # Make request to Vapi API
            response = requests.post("https://api.vapi.ai/assistant", headers=headers, json=payload)
            response.raise_for_status()  # Raise exception for HTTP errors
            result = response.json()

            return jsonify({
                "status": "success",
                "provider": "vapi",
                "id": result.get("id"),
                "voice_id": voice_id,
                "details": result
            })

    # Catch specific HTTP errors from external API calls
    except requests.exceptions.HTTPError as http_err:
        return jsonify({
            "status": "error",
            "message": f"HTTP error occurred: {http_err}",
            "details": response.text
        }), response.status_code

    # Generic error handler
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# Entry point to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
