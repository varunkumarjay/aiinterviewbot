import requests

url = "https://varunsupraja--interview-llm-service-fastapi-app.modal.run/generate"

response = requests.post(
    url,
    json={"prompt": "Explain recursion simply in 3 sentences."},
    timeout=300
)

print("Status:", response.status_code)
print("Response:", response.text)
