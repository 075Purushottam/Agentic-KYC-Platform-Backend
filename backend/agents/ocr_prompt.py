from services.llm_server import llm_call

def refine_adverse_result(customer_info,context):
    prompt = f'''
            You are an adverse media agent you have to find insight by matching given customer info.

            customer extracted data:
            {customer_info}
            
            extracted context from articles:
            {context}
            
            Results FORMAT JSON:
            Example:
            {{
                "input": [
                    "Customer Name",
                    "Jurisdiction"
                ],
                "checks": [
                    "News Search",
                    "Regulatory Mentions",
                    "Legal Cases"
                ],
                "finding": findings,
                "confidence": ["87%"],
                "risk_impact": ["+25"]
            }}
            '''
    llm_res = llm_call(prompt)
    return llm_res

def ocr_json(ocr_text):
    print("ocr_text",ocr_text)
    prompt = f"""
        OCR Text:
        {ocr_text}
        """
    llm_res = llm_call(prompt)
    # print(llm_res)
    return llm_res
    