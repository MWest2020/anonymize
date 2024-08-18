import requests
import os
import yaml
from custom_recognizers import get_custom_recognizers

class Anonymizer:
    ANALYZE_ENDPOINT = "http://127.0.0.1:5002/analyze"
    HEALTH_ENDPOINT = "http://127.0.0.1:5002/health"

    def __init__(self):
        self.check_api_health()

    def check_api_health(self):
        print("Checking API health...")
        response = requests.get(self.HEALTH_ENDPOINT)
        if response.status_code == 200:
            print("API is healthy and running.")
        else:
            print(f"API health check failed. Status code: {response.status_code}")
            raise Exception("API health check failed.")

    def load_text_file(self, file_path):
        print(f"Loading text from file: {file_path}")
        with open(file_path, 'r') as file:
            content = file.read()
        print("Text loaded successfully.")
        return content

    def save_anonymized_file(self, input_file_path, anonymized_content, is_yaml=False):
        base_name, ext = os.path.splitext(input_file_path)
        output_file_path = f"{base_name}_anonymized{ext}"
        print(f"Saving anonymized content to: {output_file_path}")
        with open(output_file_path, 'w') as file:
            file.write(anonymized_content)
        print(f"Anonymized file saved to: {output_file_path}")

    def analyze_text_with_api(self, text):
        print("Sending text to the API for analysis...")
        request_payload = {
            "text": text,
            "language": "en",
            "entities": ["CREDIT_CARD", "GENERIC_ENTITY"]
        }
        response = requests.post(self.ANALYZE_ENDPOINT, json=request_payload)
        if response.status_code == 200:
            print("Text analysis successful.")
            return response.json()
        else:
            print(f"Failed to analyze text. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    def replace_in_text_using_api(self, content, api_results, replacement):
        replaced_words = []
        if api_results:
            print("Processing and replacing text based on API results...")
            for result in sorted(api_results, key=lambda x: x['start'], reverse=True):
                original_word = content[result['start']:result['end']]
                replaced_words.append((original_word, replacement))
                content = content[:result['start']] + replacement + content[result['end']:]
            print("Text processing complete.")
        else:
            print("No API results found. No replacement was made.")
        return content, replaced_words

    def anonymize_text_file(self, file_path, original_word=None, replacement_word=None):
        content = self.load_text_file(file_path)
        replaced_words = []

        if original_word and replacement_word:
            print(f"Replacing '{original_word}' with '{replacement_word}'...")
            anonymized_content = content.replace(original_word, replacement_word)
            replaced_words.append((original_word, replacement_word))
        else:
            api_results = self.analyze_text_with_api(content)
            anonymized_content, replaced_words = self.replace_in_text_using_api(content, api_results, "ANONYMIZED")
        
        self.save_anonymized_file(file_path, anonymized_content)
        self.output_replacements(replaced_words)

    def output_replacements(self, replaced_words):
        if replaced_words:
            print("Replaced or anonymized words:")
            for original, replacement in replaced_words:
                print(f"- '{original}' was replaced with '{replacement}'")
        else:
            print("No replacements or anonymizations were made.")
