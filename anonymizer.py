import requests
import logging
import os

class Anonymizer:
    def __init__(self, anonymizer_url=None):
        self.anonymizer_url = anonymizer_url or "http://localhost:5001"
        self.ANONYMIZE_ENDPOINT = f"{self.anonymizer_url}/anonymize"
        self.HEALTH_ENDPOINT = f"{self.anonymizer_url}/health"
        self.TIMEOUT_SECONDS = 30
        self.api_available = self.check_api_health()

    def check_api_health(self):
        try:
            logging.debug(f"Checking Anonymizer health at {self.HEALTH_ENDPOINT}")
            response = requests.get(self.HEALTH_ENDPOINT, timeout=self.TIMEOUT_SECONDS)
            logging.debug(f"Anonymizer response status code: {response.status_code}")
            logging.debug(f"Anonymizer response content: {response.text}")
            if response.status_code == 200:
                logging.info("Anonymizer API is healthy and running.")
                return True
            else:
                logging.warning(f"Anonymizer health check returned unexpected status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred during Anonymizer health check: {str(e)}")
            return False

    def anonymize_text(self, text, analysis_results, language='en'):
        if not self.api_available:
            logging.error("Cannot anonymize text: API is not available.")
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
                },
                "LOCATION": {
                    "type": "replace",
                    "new_value": "[LOCATION]",
                },
                "IN_PAN": {
                    "type": "replace",
                    "new_value": "[PAN]",
                }
            },
            "language": language
        }

        logging.debug(f"Anonymizers configuration: {request_payload['anonymizers']}")
        try:
            response = requests.post(self.ANONYMIZE_ENDPOINT, json=request_payload, timeout=self.TIMEOUT_SECONDS)
            logging.debug(f"Anonymizer API response status code: {response.status_code}")
            logging.debug(f"Anonymizer API response content: {response.text}")
            response.raise_for_status()
            logging.info("Text anonymization successful.")
            anonymized_text = response.json()["text"]
            items = response.json().get("items", [])
            
            # Add original text to items
            for item in items:
                start, end = item['start'], item['end']
                item['original_text'] = text[start:end]
            
            return anonymized_text, items
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to anonymize text. Error: {str(e)}")
            logging.error(f"Response: {response.text if 'response' in locals() else 'No response'}")
            return None, []

    def output_replacements(self, replaced_items):
        if replaced_items:
            print("Replaced or anonymized items:")
            for item in replaced_items:
                original_text = item['original_text']
                entity_type = item['entity_type']
                operation = item['operator']
                
                if operation == 'replace':
                    anonymized_text = item['text']
                elif operation == 'mask':
                    anonymized_text = item['text']
                else:
                    anonymized_text = '[UNKNOWN]'
                
                print(f"- '{original_text}' was {operation}d to '{anonymized_text}' (Type: {entity_type})")
        else:
            print("No replacements or anonymizations were made.")

    def save_anonymized_file(self, input_file_path, anonymized_content):
        if anonymized_content is None:
            logging.error("Cannot save anonymized file: Anonymization failed.")
            return

        base_name, ext = os.path.splitext(input_file_path)
        output_file_path = f"{base_name}_anonymized{ext}"
        logging.info(f"Saving anonymized content to: {output_file_path}")
        with open(output_file_path, 'w') as file:
            file.write(anonymized_content)
        print(f"\nAnonymized file saved to: {output_file_path}")