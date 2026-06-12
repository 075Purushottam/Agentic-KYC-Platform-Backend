from services.kyc_vector_service import KYCVectorService
from services.retrieve_articles import extract_articles


def search(customer_details):

    normalized_articles = extract_articles(customer_details)
    query = f"""
                Person Name: {customer_details['name']}
                Coutry: {customer_details['country']}
                Organisation
                Scam
                Fruad
            """

    service = KYCVectorService(persist_directory="./chroma_db")

    service.get_or_create_collection(
        collection_name="vijay_mallya", fallback_articles=normalized_articles
    )

    results = service.retrieve_similar_articles(query)
    titles = []
    for result in results:
        titles.append(result[0].metadata["title"])

    return titles
