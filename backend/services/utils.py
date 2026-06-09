from langchain_core.documents import Document

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
