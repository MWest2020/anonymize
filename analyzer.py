import requests
import logging

class Analyzer:
    def __init__(self, analyzer_url=None):
        self.analyzer_url = analyzer_url or "http://localhost:5002"
        self.ANALYZE_ENDPOINT = f"{self.analyzer_url}/analyze"
        self.HEALTH_ENDPOINT = f"{self.analyzer_url}/health"
        self.TIMEOUT_SECONDS = 30
        self.api_available = self.check_api_health()

    def check_api_health(self):
        try:
            logging.debug(f"Checking Analyzer health at {self.HEALTH_ENDPOINT}")
            response = requests.get(self.HEALTH_ENDPOINT, timeout=self.TIMEOUT_SECONDS)
            logging.debug(f"Analyzer response status code: {response.status_code}")
            logging.debug(f"Analyzer response content: {response.text}")
            if response.status_code == 200:
                logging.info("Analyzer API is healthy and running.")
                return True
            else:
                logging.warning(f"Analyzer health check returned unexpected status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred during Analyzer health check: {str(e)}")
            return False

    def analyze_text(self, text, language='en'):
        if not self.api_available:
            logging.error("Cannot analyze text: API is not available.")
            return None

        logging.debug(f"Sending text to the Analyzer API at {self.ANALYZE_ENDPOINT}")
        request_payload = {
            "text": text,
            "language": language,
            "entities": ["PERSON", "LOCATION", "EMAIL_ADDRESS", "PHONE_NUMBER", "DATE_TIME", "NRP", "IBAN_CODE", "CREDIT_CARD"],
            "correlation_id": "1",
            "score_threshold": 0.7,
            "return_decision_process": True
        }
        try:
            response = requests.post(self.ANALYZE_ENDPOINT, json=request_payload, timeout=self.TIMEOUT_SECONDS)
            response.raise_for_status()
            logging.info("Text analysis successful.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to analyze text. Error: {str(e)}")
            logging.error(f"Response: {response.text if 'response' in locals() else 'No response'}")
            return None