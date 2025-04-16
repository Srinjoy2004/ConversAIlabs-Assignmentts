from retell import Retell

client = Retell(
    api_key="key_367e624c5c5527a8ea2c8b193a6d",
)
llm_response = client.llm.create()
print(llm_response.llm_id)