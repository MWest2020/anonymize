import argparse
from anonymizer import Anonymizer

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Anonymize text and YAML using Presidio Analyzer.")
        self.parser.add_argument("file_path", nargs='?', help="Path to the file (text or YAML) to be processed.")
        self.parser.add_argument("-D", "--directory", help="Path to the directory containing text files to be processed.")
        self.parser.add_argument("-R", "--replace", nargs=2, metavar=("original_word", "replacement_word"),
                                 help="Replace a specific word with another in the file.")
        self.parser.add_argument("-Y", "--yaml", action="store_true", help="Specify if the input is a YAML file.")
    
    def run(self):
        args = self.parser.parse_args()
        anonymizer = Anonymizer()

        if args.directory:
            self.anonymize_directory(args.directory, args.replace, args.yaml, anonymizer)
        elif args.file_path:
            if args.yaml:
                if args.replace:
                    original_word, replacement_word = args.replace
                    anonymizer.anonymize_yaml_file(args.file_path, original_word, replacement_word)
                else:
                    anonymizer.anonymize_yaml_file(args.file_path)
            else:
                if args.replace:
                    original_word, replacement_word = args.replace
                    anonymizer.anonymize_text_file(args.file_path, original_word, replacement_word)
                else:
                    anonymizer.anonymize_text_file(args.file_path)
        else:
            print("Please specify a file or directory to process.")

    def anonymize_directory(self, directory_path, replace_args, is_yaml, anonymizer):
        print(f"Processing directory: {directory_path}")
        files = [f for f in os.listdir(directory_path) if (is_yaml and f.endswith(".yml")) or (f.endswith(".txt"))]
        total_files = len(files)
        
        print(f"Found {total_files} file(s) to process.\n")
        
        for index, filename in enumerate(files, start=1):
            file_path = os.path.join(directory_path, filename)
            print(f"Processing file {index}/{total_files}: {file_path}")
            if is_yaml and filename.endswith(".yml"):
                if replace_args:
                    original_word, replacement_word = replace_args
                    anonymizer.anonymize_yaml_file(file_path, original_word, replacement_word)
                else:
                    anonymizer.anonymize_yaml_file(file_path)
            elif filename.endswith(".txt"):
                if replace_args:
                    original_word, replacement_word = replace_args
                    anonymizer.anonymize_text_file(file_path, original_word, replacement_word)
                else:
                    anonymizer.anonymize_text_file(file_path)
            
            # Progress indicator
            self.print_progress(index, total_files)

    def print_progress(self, current, total):
        percent = (current / total) * 100
        bar_length = 40
        block = int(round(bar_length * percent / 100))
        progress_bar = "#" * block + "-" * (bar_length - block)
        print(f"\rProgress: [{progress_bar}] {percent:.2f}% ({current}/{total})", end="\r")
        
        if current == total:
            print("\nProcessing complete!")
