import yaml
import sys
import os

# Step 1: Load the OAS file (assuming it's in YAML format)
def load_oas_file(file_path):
    with open(file_path, 'r') as file:
        oas_content = yaml.safe_load(file)
    return oas_content

# Step 2: Recursive function to replace the target string in the YAML structure
def replace_in_yaml_structure(data, word_to_replace, replacement):
    if isinstance(data, dict):
        return {key: replace_in_yaml_structure(value, word_to_replace, replacement) for key, value in data.items()}
    elif isinstance(data, list):
        return [replace_in_yaml_structure(item, word_to_replace, replacement) for item in data]
    elif isinstance(data, str):
        return data.replace(word_to_replace, replacement)
    else:
        return data

# Step 3: Save the anonymized OAS content to a new file
def save_anonymized_oas(input_file_path, anonymized_content):
    base_name, ext = os.path.splitext(input_file_path)
    output_file_path = f"{base_name}_anonymized{ext}"
    with open(output_file_path, 'w') as file:
        yaml.dump(anonymized_content, file, default_flow_style=False, sort_keys=False)
    print(f"Anonymized OAS file saved to: {output_file_path}")

# Main function to process the OAS file
def anonymize_oas_file(input_file_path, word_to_replace, replacement):
    # Load the OAS file content
    oas_content = load_oas_file(input_file_path)
    
    # Replace the target string in the YAML structure
    anonymized_content = replace_in_yaml_structure(oas_content, word_to_replace, replacement)
    
    # Save the anonymized OAS content to a new file
    save_anonymized_oas(input_file_path, anonymized_content)

# CLI entry point
def main():
    if len(sys.argv) < 3:
        print("Usage: python -m anonymize_yaml <file_path> <word to be replaced> [word to be replaced with(optional)]")
        sys.exit(1)

    file_path = sys.argv[1]
    word_to_replace = sys.argv[2]
    replacement = sys.argv[3] if len(sys.argv) > 3 else "ANONYMIZED"

    anonymize_oas_file(file_path, word_to_replace, replacement)

if __name__ == "__main__":
    main()
