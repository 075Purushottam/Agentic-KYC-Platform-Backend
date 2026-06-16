from langchain_core.documents import Document
import regex as re
import json
def create_documents(articles):
    docs = []
    for article in articles:

        text = f"""
        Title: {article.title}

        Description:
        {article.description}

        Content:
        {article.content}
        """

        docs.append(
            Document(
                page_content=text,
                metadata={
                    "source": article.source,
                    "url": article.url,
                    "published_at": article.published_at,
                    "title": article.title
                }
            )
        )

    return docs

def clean_response(response):
    print("Response Before Clean:",response)
    response = response.replace("`", "").replace("'", "\'")
    response = re.sub(r'^(json|python)\s*', '', response, flags=re.IGNORECASE)

    if response.startswith("json"): 
        response = response[4:]
    if response.startswith("python"):
        response = response[6:]
    print("response: ",response)
    parsed_response = json.loads(response)
    
    print()
    print("----------------------------------------------------------------------------")
    print("Response After Clean:",parsed_response)
    return parsed_response
