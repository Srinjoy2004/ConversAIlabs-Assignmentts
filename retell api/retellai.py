from retell import Retell

client = Retell(
    api_key="key_288267825dcdd61334dc46a65057",
)
agent_response = client.agent.create(
    response_engine={
        "llm_id": "llm_e5643608af66a4021effa5909bd4",
        "type": "retell-llm",
    },
    voice_id="elevenlabs",
)
print(agent_response.agent_id)