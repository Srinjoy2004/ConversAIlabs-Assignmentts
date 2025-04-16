from retell import Retell

client = Retell(
    api_key="key_367e624c5c5527a8ea2c8b193a6d",
)
voice_response = client.voice.retrieve(
    "11labs-Adrian",
)
print(voice_response.provider)