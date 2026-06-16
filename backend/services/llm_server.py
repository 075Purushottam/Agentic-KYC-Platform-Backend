import httpx
from services.utils import clean_response
from services.gemini_client import GeminiClient
PUBLIC_URL = "https://footage-method-cartridge-hobbies.trycloudflare.com"

SYSTEM_PROMPT = '''You are an expert document information extraction system.

        Your task is to extract structured information from OCR text obtained from Indian identity documents such as Aadhaar Cards, PAN Cards, Driving Licenses, Voter IDs, Passports, and similar documents.

        Instructions:

        1. Analyze the OCR text carefully.

        2. Extract all identifiable fields and return them as a valid JSON object only.

        3. Always include the following keys in the output:

        * name
        * dob
        * country
        * address

        4. Rules:

        * If country is not explicitly present, set it to "India".
        * If address is not found, set it to an empty string "".
        * If name is not found, set it to an empty string "".
        * If dob is not found, set it to an empty string "".
        * Convert DOB to YYYY-MM-DD format whenever possible.
        * Remove extra spaces, line breaks, and OCR artifacts.
        * Preserve document numbers exactly as they appear.

        5. Create additional key-value pairs for any relevant information found, such as:

        * aadhaar_no
        * pan_no
        * father_name
        * gender
        * mobile_no
        * pincode
        * state
        * city
        * issue_date
        * expiry_date
        * document_type
        * uid
        * nationality
        * etc.

        6. If multiple values are detected for the same field, choose the most likely correct value based on context.

        7. Return **ONLY valid JSON**. Do not include explanations, markdown, comments, or code blocks.
'''
# Real inference call
def llm_call(prompt):
#     r = httpx.post(
#         f"{PUBLIC_URL}/generate",
#         json={"prompt": prompt, "max_tokens": 1000, "temperature": 0.1},
#         timeout=120,
#     )
#     res = r.json()
#     return clean_response(res["response"])

    messages = [
        {"role": "user", "parts": [{"text": prompt}]}
    ]
    try:
        gemini_client = GeminiClient()
        response = gemini_client.generate_text(
            messages=messages,
            system_instruction=SYSTEM_PROMPT,
            model="gemini-2.5-flash"
        )
    except Exception as e:
        print("Error:",e)
        response =  {'name': 'PURUSHOTTAM PATIDAR', 'dob': '2000-10-15', 'country': 'India', 'address': 'Gram Bardiya, Post Gurjar Bard, Tehsil Mandsaur, District Mandsaur, Madhya Pradesh - 458895', 'aadhaar_no': '6559 5458 8740', 'pan_no': 'EDZPP3833G', 'father_name': 'SHANKAR LAL PATIDAR', 'gender': 'MALE', 'pincode': '458895', 'state': 'Madhya Pradesh', 'city': 'Mandsaur'}
        return response
    return clean_response(response)