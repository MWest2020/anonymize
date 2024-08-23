from presidio_analyzer import PatternRecognizer

def get_custom_recognizers(custom_word):
    # Define a generic pattern to match the specific custom word, case-insensitive
    regex_pattern = rf"(?i)\b{custom_word}\b"
    
    custom_recognizer = PatternRecognizer(
        supported_entity="CUSTOM_ENTITY",
        patterns=[{
            "name": f"Custom pattern for {custom_word}",
            "regex": regex_pattern,
            "score": 0.85  # Confidence score (can be adjusted)
        }]
    )
    return [custom_recognizer]

def analyze_text_with_api(self, text, custom_word=None):
    print("Sending text to the API for analysis...")
    entities = ["CREDIT_CARD", "PERSON"]
    if custom_word:
        entities.append("CUSTOM_ENTITY")
        print(f"Custom entity '{custom_word}' added to the analysis.")

    request_payload = {
        "text": text,
        "language": "en",
        "entities": entities
    }

    # Debug: Show the payload before sending it
    print("Payload being sent to API:", request_payload)

    response = requests.post(self.ANALYZE_ENDPOINT, json=request_payload)
    if response.status_code == 200:
        print("Text analysis successful.")
        return response.json()
    else:
        print(f"Failed to analyze text. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None
