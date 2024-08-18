from PIL import Image
from presidio_image_redactor import ImageRedactorEngine

# Load the image using PIL (Pillow)
image = Image.open(r"C:\Users\mwest\CONDUCTION\Anonymize\WIN_20240816_21_25_15_Pro.jpg")

# Initialize the ImageRedactorEngine
engine = ImageRedactorEngine()

# Redact the image, replacing sensitive information with pink color
redacted_image = engine.redact(image, (255, 192, 203))

# Save the redacted image to a new file
redacted_image.save(r"C:\Users\mwest\CONDUCTION\Anonymize\WIN_20240816_21_25_15_Pro_redacted.png")

# Uncomment the line below if you want to view the redacted image
# redacted_image.show()
