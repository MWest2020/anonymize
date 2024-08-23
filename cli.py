import argparse
from .anonymizer import Anonymizer

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Anonymize text using Presidio Analyzer and Anonymizer APIs.")
        self.parser.add_argument("file_path", help="Path to the file to be processed.")
        self.parser.add_argument("-D", "--directory", help="Path to the directory containing text files to be processed.")
        self.parser.add_argument("-R", "--replace", metavar="custom_word", help="Specify a word to be treated as PII and replaced in the file.")
        self.parser.add_argument("--anonymizer-url", default="http://localhost:5001", help="Custom Anonymizer API URL")
        self.parser.add_argument("--analyzer-url", default="http://localhost:5002", help="Custom Analyzer API URL")

    def run(self):
        args = self.parser.parse_args()
        anonymizer = Anonymizer(anonymizer_url=args.anonymizer_url, analyzer_url=args.analyzer_url)

        if not anonymizer.api_available:
            print("Warning: One or both APIs are not available. Anonymization features may not work correctly.")
            return

        if args.directory:
            self.anonymize_directory(args.directory, args.replace, anonymizer)
        elif args.file_path:
            self.process_text(args, anonymizer)
        else:
            print("Please specify a file or directory to process.")

    def process_text(self, args, anonymizer):
        anonymizer.anonymize_text_file(args.file_path, custom_word=args.replace)

    def anonymize_directory(self, directory_path, custom_word, anonymizer):
        print(f"Processing directory: {directory_path}")
        files = [f for f in os.listdir(directory_path) if f.endswith(".txt")]
        total_files = len(files)
        
        print(f"Found {total_files} file(s) to process.\n")
        
        for index, filename in enumerate(files, start=1):
            file_path = os.path.join(directory_path, filename)
            print(f"Processing file {index}/{total_files}: {file_path}")
            anonymizer.anonymize_text_file(file_path, custom_word=custom_word)
            self.print_progress(index, total_files)

    def print_progress(self, current, total):
        percent = (current / total) * 100
        bar_length = 40
        block = int(round(bar_length * percent / 100))
        progress_bar = "#" * block + "-" * (bar_length - block)
        print(f"\rProgress: [{progress_bar}] {percent:.2f}% ({current}/{total})", end="\r")
        
        if current == total:
            print("\nProcessing complete!")