import cv2
import numpy as np


def analyze_document_quality(image_path: str):
    img = cv2.imread(image_path)

    if img is None:
        return {
            "score": 0,
            "status": "FAILED",
            "findings": ["Unable to read image"],
            "confidence": 0
        }

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = gray.shape

    findings = []
    score = 100

    # ------------------------
    # Resolution Check
    # ------------------------
    resolution = w * h

    if resolution < 500000:
        findings.append("Low image resolution")
        score -= 20
    else:
        findings.append("Resolution acceptable")

    # ------------------------
    # Blur Check
    # ------------------------
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    if blur_score < 100:
        findings.append("Image appears blurry")
        score -= 25
    else:
        findings.append("Image sharpness acceptable")

    # ------------------------
    # Brightness Check
    # ------------------------
    brightness = np.mean(gray)

    if brightness < 50:
        findings.append("Image too dark")
        score -= 15

    elif brightness > 220:
        findings.append("Image overexposed")
        score -= 15

    else:
        findings.append("Brightness acceptable")

    # ------------------------
    # Contrast Check
    # ------------------------
    contrast = gray.std()

    if contrast < 35:
        findings.append("Low contrast detected")
        score -= 15

    else:
        findings.append("Contrast acceptable")

    # ------------------------
    # Edge Density
    # ------------------------
    edges = cv2.Canny(gray, 100, 200)

    edge_ratio = np.count_nonzero(edges) / edges.size

    if edge_ratio < 0.02:
        findings.append("Document details may be unclear")
        score -= 10

    else:
        findings.append("Document details visible")

    # ------------------------
    # Border Check
    # ------------------------
    border = 20

    border_pixels = np.concatenate([
        gray[:border, :].flatten(),
        gray[-border:, :].flatten(),
        gray[:, :border].flatten(),
        gray[:, -border:].flatten()
    ])

    if border_pixels.std() < 5:
        findings.append("Possible cropped document")
        score -= 10

    # ------------------------
    # Final Score
    # ------------------------
    score = max(0, min(score, 100))

    if score >= 85:
        status = "EXCELLENT"

    elif score >= 70:
        status = "GOOD"

    elif score >= 50:
        status = "FAIR"

    else:
        status = "POOR"

    return {
        "score": score,
        "status": status,
        "confidence": score,
        "findings": findings,
        "metrics": {
            "resolution": resolution,
            "blur_score": round(blur_score, 2),
            "brightness": round(brightness, 2),
            "contrast": round(contrast, 2),
            "edge_ratio": round(edge_ratio, 4)
        }
    }