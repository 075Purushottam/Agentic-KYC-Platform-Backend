import easyocr
import os

def extract_text_from_image(image_path, languages=['en']):
    """
    Extract text from an image using EasyOCR.

    :param image_path: Path to the image file
    :param languages: List of language codes (default: ['en'])
    :return: List of extracted text strings
    """
    # Validate file existence
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    try:
        # Initialize EasyOCR reader
        reader = easyocr.Reader(languages)  # e.g., ['en', 'hi'] for English + Hindi

        # Perform OCR
        results = reader.readtext(image_path)

        # Extract only the text part from results
        extracted_texts = [text for (_, text, _) in results]

        return extracted_texts

    except Exception as e:
        raise RuntimeError(f"Error during OCR processing: {e}")

if __name__ == "__main__":
    # Example usage
    image_file = r"C:\Users\Tirupati\Desktop\agentic-kyc-platform\Agentic-KYC-Platform-Backend\backend\uploads\CASE-1aeb0be3\pancard-images-0.jpg"

    try:
        texts = extract_text_from_image(image_file, languages=['en'])
        print("Extracted Text:")
        for idx, t in enumerate(texts, start=1):
            print(f"{idx}. {t}")
    except Exception as err:
        print(f"Failed: {err}")
