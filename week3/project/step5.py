import requests
import json

def main(endpoint: str):
    """
    Run the requests file for Step 5
    """
    with open("data/requests.json") as requests_file:
        for request in requests_file:
            body = json.loads(request)
            requests.post(endpoint, json=body)

if __name__ == "__main__":
    main("http://localhost:8000/predict")