# Anonymize Text Application

This application provides a way to anonymize sensitive information in text files using Microsoft's Presidio Analyzer. It supports both detecting and anonymizing predefined entities (like credit card numbers) and custom entities through regex-based recognizers. Additionally, it allows for direct word replacement within a text file.

## Features

- API-Based Anonymization: Automatically detect and anonymize entities such as credit card numbers and other custom entities.
- Customizable Word Replacement: Replace specific words in a text file with a specified replacement word.
- Modular Design: The application is designed with modularity in mind, separating the CLI, core functionality, and custom recognizers into different files.

## Instalaltion

1. Clone the repository

```bash
git clone https://github.com/MWest2020/anonymize.git
cd anonymize-text
```

2. Set up the environment:

- Ensure you have Python 3.7 or higher installed. We tested and developed with 3.11

> *__WARNING__*: Presidio doesn't work with Python > 3.11, yet

- Install the required packages:

```bash
Copy code
pip install -r requirements.txt
```

- Make sure you have the Presidio Analyzer Docker containers running.

3. Set up Docker:

- Pull and run the Presidio Analyzer and Presidio Anonymizer Docker containers:

```bash
docker run -d -p 5002:3000 mcr.microsoft.com/presidio-analyzer:latest
docker run -d -p 5001:3000 mcr.microsoft.com/presidio-anonymizer:latest
```

## Usage

### Running the CLI

The command-line interface (CLI) provides two main functionalities:

1. Default Anonymization: Analyze text using Presidio Analyzer to detect both native (e.g., credit card numbers) and custom entities, and anonymize them.
2. Direct Word Replacement: Replace a specific word with another in the text file.

### Basic Command

1. Default Anonymization:

```bash
python -m anonymize_text <file_path>
```

- Description: This command will analyze the specified text file, detect entities, and anonymize them by replacing them with the default word "ANONYMIZED".

2. Direct Word Replacement (Single File):

```bash
python -m anonymize_text <file_path> -R <original_word> <replacement_word>
```

- Description: This command will directly replace the occurrences of <original_word> with <replacement_word> in the specified text file.

3. Batch Anonymuzation (Directory)

```bash
python -m anonymize_text -D <directory_path>
```

- Description: This command will analyze all text files within the specified directory, detect entities, and anonymize them by replacing them with the default word "ANONYMIZED".

4. Batch Word Replacement(Directory)

```bash
python -m anonymize_text -D <directory_path> -R <original_word> <replacement_word>
```

- Description: This command will directly replace the occurrences of <original_word> with <replacement_word> in all text files within the specified directory.

## Customizing Recognizers

You can extend the application's functionality by adding custom recognizers in the custom_recognizers.py file. This allows for the detection and anonymization of custom patterns not covered by the built-in recognizers.

> __Note__ We will update this very soon with databse support.

## Troubleshooting

- API Health Check Failed:

  - If the API health check fails, ensure that the Presidio Analyzer Docker containers are running and accessible at <http://127.0.0.1:5002>.
- No Entities Detected:

  - If no entities are detected, check that the text file contains entities that match the patterns defined in the custom recognizers or that fall under the built-in recognizers' capabilities.

## Summary

- __New Feature__: Added support for batch processing of all text files in a directory using the `-D` or `--directory` flag.
- __Updated CLI__: Now supports both single file and directory processing, making it more versatile.
- __Documentation__: Updated the `README.md` to reflect the new functionality and provide clear instructions on how to use the tool.

This approach ensures that your tool can easily scale to handle multiple files at once, making it more efficient for users who need to anonymize large sets of text files.
