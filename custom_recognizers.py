from presidio_analyzer import PatternRecognizer

def get_generic_recognizer(max_length=10):
    # Define a generic pattern to match strings up to `max_length` characters long, case-insensitive
    regex_pattern = r"(?i)\b\w{1," + str(max_length) + r"}\b"
    
    generic_recognizer = PatternRecognizer(
        supported_entity="GENERIC_ENTITY",
        patterns=[{
            "name": f"Generic pattern up to {max_length} chars",
            "regex": regex_pattern,
            "score": 0.5  # Confidence score (can be adjusted)
        }]
    )
    return generic_recognizer

def get_custom_recognizers():
    # Create and return a list of custom recognizers, including the generic one
    generic_recognizer = get_generic_recognizer()
    return [generic_recognizer]
