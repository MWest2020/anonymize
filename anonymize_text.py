import requests
import sys
import os

# Define the API endpoint
ANALYZE_ENDPOINT = "http://127.0.0.1:5002/analyze"
HEALTH_ENDPOINT = "http://127.0.0.1:5002/health"

# Step 0: Check the health of the API
def check_api_health():
    print("Checking API health...")
    response = requests.get(HEALTH_ENDPOINT)
    if response.status_code == 200:
        print("API is healthy and running.")
    else:
        print(f"API health check failed. Status code: {response.status_code}")
        sys.exit(1)

# Step 1: Load the text file
def load_text_file(file_path):
    print(f"Loading text from file: {file_path}")
    with open(file_path, 'r') as file:
        content = file.read()
    print("Text loaded successfully.")
    return content

# Step 2: Analyze text using the API
def analyze_text_with_api(text):
    print("Sending text to the API for analysis...")
    request_payload = {
        "text": text,
        "language": "en",
        "entities": ["CREDIT_CARD"]  # Use the built-in CREDIT_CARD recognizer
    }
    response = requests.post(ANALYZE_ENDPOINT, json=request_payload)
    if response.status_code == 200:
        print("Text analysis successful.")
        return response.json()
    else:
        print(f"Failed to analyze text. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

# Step 3: Replace the detected PII
def replace_in_text_using_api(content, api_results, replacement):
    if api_results:
        print("Processing and replacing text based on API results...")
        for result in sorted(api_results, key=lambda x: x['start'], reverse=True):
            content = content[:result['start']] + replacement + content[result['end']:]
        print("Text processing complete.")
    else:
        print("No API results found. No replacement was made.")
    return content

# Step 4: Save the anonymized text content to a new file
def save_anonymized_text(input_file_path, anonymized_content):
    base_name, ext = os.path.splitext(input_file_path)
    output_file_path = f"{base_name}_anonymized{ext}"
    print(f"Saving anonymized text to: {output_file_path}")
    with open(output_file_path, 'w') as file:
        file.write(anonymized_content)
    print(f"Anonymized text file saved to: {output_file_path}")

# Main function to process the text file
def anonymize_text_file(input_file_path, replacement):
    # Step 0: Check API health
    check_api_health()
    
    # Step 1: Load the text file content
    content = load_text_file(input_file_path)
    
    # Step 2: Analyze the text using the API to detect credit card numbers
    api_results = analyze_text_with_api(content)
    
    # Step 3: Replace the detected PII in the text content based on API results
    anonymized_content = replace_in_text_using_api(content, api_results, replacement)
    
    # Step 4: Save the anonymized text content to a new file
    save_anonymized_text(input_file_path, anonymized_content)

# CLI entry point
def main():
    if len(sys.argv) < 2:
        print("Usage: python -m anonymize_text <file_path> [word to be replaced with(optional)]")
        sys.exit(1)

    file_path = sys.argv[1]
    replacement = sys.argv[2] if len(sys.argv) > 2 else "ANONYMIZED"

    anonymize_text_file(file_path, replacement)

if __name__ == "__main__":
    main()
