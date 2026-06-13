from paddleocr import PaddleOCR
import os
os.environ["PADDLE_PDX_ENABLE_MKLDNN_BYDEFAULT"] = "0"
# Initialize OCR
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    lang='en',  # Change language if needed
    enable_mkldnn=False,
    det_model_dir=r'C:\Users\Tirupati\.paddlex\official_models\PP-OCRv6_medium_det',
    rec_model_dir=r'C:\Users\Tirupati\.paddlex\official_models\PP-OCRv6_medium_rec'
)

# Run OCR
def ocr_image(image_path):
    image_path = os.path.normpath(image_path)
    print("correct path:",image_path)
    result = ocr.predict(image_path)
    res = ""
    # Print extracted text
    for page in result:
        for line in page['rec_texts']:
            res+=line
    return str(res)

image_path = r"C:\Users\Tirupati\Desktop\agentic-kyc-platform\Agentic-KYC-Platform-Backend\backend\uploads\CASE-1aeb0be3\pancard-images-0.jpg"

print(ocr_image(image_path))
