import argparse
import os
import logging
from .analyzer import Analyzer
from .anonymizer import Anonymizer

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Anonymize text using Presidio Analyzer and Anonymizer APIs.")
        self.parser.add_argument("file_path", help="Path to the file to be processed.")
        self.parser.add_argument("-D", "--directory", help="Path to the directory containing text files to be processed.")
        self.parser.add_argument("-R", "--replace", metavar="custom_word", help="Specify a word to be treated as PII and replaced in the file.")
        self.parser.add_argument("--anonymizer-url", default="http://localhost:5001", help="Custom Anonymizer API URL")
        self.parser.add_argument("--analyzer-url", default="http://localhost:5002", help="Custom Analyzer API URL")
        self.parser.add_argument("--language", default="en", choices=["en", "nl"], help="Language of the text (en for English, nl for Dutch)")
        self.parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    def run(self):
        args = self.parser.parse_args()
        
        # Set up logging
        log_level = logging.DEBUG if args.debug else logging.INFO
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

        analyzer = Analyzer(analyzer_url=args.analyzer_url)
        anonymizer = Anonymizer(anonymizer_url=args.anonymizer_url)

        if not analyzer.api_available or not anonymizer.api_available:
            logging.warning("One or both APIs are not available. Anonymization features may not work correctly.")
            return

        if args.directory:
            self.anonymize_directory(args.directory, args.replace, analyzer, anonymizer, args.language)
        elif args.file_path:
            self.process_text(args, analyzer, anonymizer)
        else:
            logging.error("Please specify a file or directory to process.")

    def process_text(self, args, analyzer, anonymizer):
        content = self.load_text_file(args.file_path)
        if content is None:
            return

        analysis_results = analyzer.analyze_text(content, language=args.language)
        if analysis_results:
            anonymized_content, replaced_items = anonymizer.anonymize_text(content, analysis_results, language=args.language)
            if anonymized_content:
                anonymizer.save_anonymized_file(args.file_path, anonymized_content)
                anonymizer.output_replacements(replaced_items)
            else:
                logging.error("Anonymization failed. No changes were made.")
        else:
            logging.error("Analysis failed. No changes were made.")

    def load_text_file(self, file_path):
        logging.info(f"Loading text from file: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            logging.info("Text loaded successfully.")
            return content
        except FileNotFoundError:
            logging.error(f"File not found at {file_path}")
            return None
        except Exception as e:
            logging.error(f"Error loading file: {str(e)}")
            return None

    def anonymize_directory(self, directory_path, custom_word, analyzer, anonymizer, language):
        logging.info(f"Processing directory: {directory_path}")
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    logging.info(f"\nProcessing file: {file_path}")
                    self.process_text(argparse.Namespace(file_path=file_path, replace=custom_word, language=language), analyzer, anonymizer)

