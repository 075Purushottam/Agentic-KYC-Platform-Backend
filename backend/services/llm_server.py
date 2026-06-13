import httpx

PUBLIC_URL = "https://pal-henry-acdbentity-execute.trycloudflare.com"

# Real inference call
def llm_call(prompt):
    r = httpx.post(f"{PUBLIC_URL}/generate", json={
        "prompt": prompt,
        "max_tokens": 2000,
        "temperature": 0.1
    }, timeout=120)
    res = r.json()
    return res['response']
