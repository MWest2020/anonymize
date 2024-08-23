import requests
import os
import logging

logging.basicConfig(level=logging.DEBUG)

class Anonymizer:
    def __init__(self, anonymizer_url=None, analyzer_url=None):
        self.anonymizer_url = anonymizer_url or "http://localhost:5001"
        self.analyzer_url = analyzer_url or "http://localhost:5002"
        self.ANALYZE_ENDPOINT = f"{self.analyzer_url}/analyze"
        self.ANONYMIZE_ENDPOINT = f"{self.anonymizer_url}/anonymize"
        self.ANONYMIZER_HEALTH_ENDPOINT = f"{self.anonymizer_url}/health"
        self.ANALYZER_HEALTH_ENDPOINT = f"{self.analyzer_url}/health"
        self.TIMEOUT_SECONDS = 30
        self.api_available = self.check_api_health()

    def check_api_health(self):
        anonymizer_healthy = self._check_endpoint_health(self.ANONYMIZER_HEALTH_ENDPOINT, "Anonymizer")
        analyzer_healthy = self._check_endpoint_health(self.ANALYZER_HEALTH_ENDPOINT, "Analyzer")
        return anonymizer_healthy and analyzer_healthy

    def _check_endpoint_health(self, endpoint, service_name):
        try:
            logging.debug(f"Checking {service_name} health at {endpoint}")
            response = requests.get(endpoint, timeout=self.TIMEOUT_SECONDS)
            logging.debug(f"{service_name} response status code: {response.status_code}")
            logging.debug(f"{service_name} response content: {response.text}")
            if response.status_code == 200:
                logging.info(f"{service_name} API is healthy and running.")
                return True
            else:
                logging.warning(f"{service_name} health check returned unexpected status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred during {service_name} health check: {str(e)}")
            return False

    def load_text_file(self, file_path):
        print(f"Loading text from file: {file_path}")
        with open(file_path, 'r') as file:
            content = file.read()
        print("Text loaded successfully.")
        return content

    def save_anonymized_file(self, input_file_path, anonymized_content):
        if anonymized_content is None:
            logging.error("Cannot save anonymized file: Anonymization failed.")
            return

        base_name, ext = os.path.splitext(input_file_path)
        output_file_path = f"{base_name}_anonymized{ext}"
        logging.info(f"Saving anonymized content to: {output_file_path}")
        with open(output_file_path, 'w') as file:
            file.write(anonymized_content)
        logging.info(f"Anonymized file saved to: {output_file_path}")

    def analyze_text(self, text):
        logging.debug(f"Sending text to the Analyzer API at {self.ANALYZE_ENDPOINT}")
        request_payload = {
            "text": text,
            "language": "en"
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

    def anonymize_text_with_api(self, text, custom_word=None):
        if not self.api_available:
            logging.error("Cannot anonymize text: API is not available.")
            return None, []

        # First, analyze the text
        analysis_results = self.analyze_text(text)
        if not analysis_results:
            return None, []

        logging.debug(f"Sending text to the Anonymizer API for anonymization at {self.ANONYMIZE_ENDPOINT}")
        request_payload = {
            "text": text,
            "analyzer_results": analysis_results,
            "anonymizers": {
                "CREDIT_CARD": {
                    "type": "mask",
                    "masking_char": "*",
                    "chars_to_mask": 12,
                    "from_end": False
                },
                "PERSON": {
                    "type": "replace",
                    "new_value": "[PERSON]",
                    "from_end": False
                },
                "LOCATION": {
                    "type": "replace",
                    "new_value": "[LOCATION]",
                    "from_end": False
                },
                "IN_PAN": {
                    "type": "mask",
                    "masking_char": "*",
                    "chars_to_mask": 4,
                    "from_end": True
                }
            }
        }

        if custom_word:
            logging.debug(f"Custom entity '{custom_word}' added to the anonymization.")
            request_payload["anonymizers"]["CUSTOM_ENTITY"] = {
                "type": "replace",
                "new_value": "[CUSTOM_ENTITY]",
                "from_end": False
            }

        logging.debug(f"Anonymizers configuration: {request_payload['anonymizers']}")
        try:
            response = requests.post(self.ANONYMIZE_ENDPOINT, json=request_payload, timeout=self.TIMEOUT_SECONDS)
            logging.debug(f"Anonymizer API response status code: {response.status_code}")
            logging.debug(f"Anonymizer API response content: {response.text}")
            response.raise_for_status()
            logging.info("Text anonymization successful.")
            return response.json()["text"], response.json().get("items", [])
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to anonymize text. Error: {str(e)}")
            logging.error(f"Response: {response.text if 'response' in locals() else 'No response'}")
            return None, []

    def output_replacements(self, replaced_items):
        if replaced_items:
            print("Replaced or anonymized items:")
            for item in replaced_items:
                original_text = item['text']
                anonymized_text = item.get('anonymized_text', item['text'])  # Use 'text' if 'anonymized_text' is not present
                entity_type = item['entity_type']
                operation = item['operator']
                print(f"- '{original_text}' was {operation}d to '{anonymized_text}' (Type: {entity_type})")
        else:
            print("No replacements or anonymizations were made.")

    def anonymize_text_file(self, file_path, custom_word=None):
        content = self.load_text_file(file_path)
        anonymized_content, replaced_items = self.anonymize_text_with_api(content, custom_word=custom_word)
        if anonymized_content:
            self.save_anonymized_file(file_path, anonymized_content)
            if replaced_items:
                self.output_replacements(replaced_items)
            else:
                print("Anonymization completed, but no specific replacements were reported.")
        else:
            logging.error("Anonymization failed. No changes were made.")