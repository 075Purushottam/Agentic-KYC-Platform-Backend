from services.llm_server import llm_call

def ocr_json(ocr_text):
    print("ocr_text",ocr_text)
    prompt = f"""You are an expert document information extraction system.

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

        7. Return ONLY valid JSON. Do not include explanations, markdown, comments, or code blocks.

        OCR Text:
        {ocr_text}
        """
    llm_res = llm_call(prompt)
    print(llm_res)
    return llm_res
    