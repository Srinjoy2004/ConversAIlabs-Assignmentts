from flask import Flask, request, jsonify
from retell import Retell

app = Flask(__name__)

# Use your actual Retell API key here (or load from .env securely later)
API_KEY = "key_367e624c5c5527a8ea2c8b193a6d"
VOICE_ID = "play-Andrew"  # Your custom voice ID

@app.route('/create-agent', methods=['POST'])
def create_agent():
    try:
        # Initialize Retell client
        client = Retell(api_key=API_KEY)

        # Create LLM first
        # llm_response = client.llm.create()
        # llm_id = llm_response.llm_id
        # Use the given LLM ID directly
        llm_id = "llm_7d9842d7d0d18e2df6796b619047"


        # Create agent using format from docs
        agent_response = client.agent.create(
            response_engine={
                "llm_id": llm_id,
                "type": "retell-llm",
            },
            voice_id=VOICE_ID,
        )

        # Return the agent ID
        return jsonify({
            "status": "success",
            "llm_id": llm_id,
            "agent_id": agent_response.agent_id
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
    
