import requests

# Sample text to analyze
text1 = "I suspect John Doe, in the Dining Room, with the candlestick"

# Step 1: Create the payload for the request
request_payload = {
    "text": text1,
    "language": "en",
    "entities": ["PERSON"]
}

# Step 2: Make the request to the Presidio analyzer service
response = requests.post("http://127.0.0.1:5002/analyze", json=request_payload)

# Step 3: Handle the response
if response.status_code == 200:
    results = response.json()
    print("Results:")
    print(results)

    # Step 4: Print identified PII entities
    print("Identified these PII entities:")
    for result in results:
        print(f"- {text1[result['start'] : result['end']]} as {result['entity_type']}")
else:
    print(f"Failed to analyze text. Status code: {response.status_code}")
    print(f"Response: {response.text}")
