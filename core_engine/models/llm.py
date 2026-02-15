import requests


MODAL_URL = "https://varunsupraja--interview-llm-service-fastapi-app.modal.run/generate"


class LLM:
    def __init__(self):
        pass

    def generate(self, prompt, max_tokens=800):

        response = requests.post(
            MODAL_URL,
            json={"prompt": prompt},
            timeout=300
        )

        if response.status_code != 200:
            raise Exception(response.text)

        result = response.json()["response"]
        print("\n===== MODAL RAW RESPONSE =====\n")
        print(result)
        print("\n==============================\n")
        return result

