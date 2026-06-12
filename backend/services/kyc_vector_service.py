import os
import json
import logging
from typing import List, Dict, Any, Tuple
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

# Assuming create_documents handles parsing raw articles to LangChain Document objects
from services.utils import create_documents

# Setup logging for production readiness
logging.basicConfig(filename='app.log',filemode='a',level=logging.INFO,format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)


class KYCVectorService:
    """
    A service class to manage vector storage and retrieval for Know Your Customer (KYC)
    and Adverse Media Screening compliance workflows.
    """

    def __init__(
        self,
        embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        persist_directory: str = "./chroma_db",
    ):
        self.embedding_model_name = embedding_model_name
        self.persist_directory = persist_directory

        # Initialize embeddings safely
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model_name
            )
            logger.info(
                f"Successfully initialized embedding model: {self.embedding_model_name}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize HuggingFaceEmbeddings: {e}")
            raise

        # Placeholder for the vector store instance
        self.vector_store = None

    def initialize_vector_store(
        self, collection_name: str = "adverse_articles"
    ) -> Chroma:
        """
        Initializes or connects to an existing Chroma DB collection.
        """
        try:
            self.vector_store = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory,
            )
            logger.info(
                f"Connected to Chroma collection: '{collection_name}' at '{self.persist_directory}'"
            )
            return self.vector_store
        except Exception as e:
            logger.error(f"Failed to initialize Chroma vector store: {e}")
            raise

    def add_articles(self, articles: List[Dict[str, Any]]) -> None:
        """
        Converts raw articles into LangChain documents and inserts them into the vector store.
        """
        if not self.vector_store:
            raise ValueError(
                "Vector store is not initialized. Call 'initialize_vector_store()' first."
            )

        if not articles:
            logger.warning("Empty articles list provided. Skipping insertion.")
            return

        try:
            documents = create_documents(articles)
            self.vector_store.add_documents(documents)
            logger.info(
                f"Successfully stored {len(documents)} document chunks into the vector store."
            )
        except Exception as e:
            logger.error(f"Error while adding documents to vector store: {e}")
            raise

    def get_or_create_collection(
        self, collection_name: str, fallback_articles: list
    ):
        """
        Automatically connects to an existing collection or builds a new one if empty.
        """
        self.initialize_vector_store(collection_name=collection_name)

        # Check if the collection is empty by fetching a count of items
        # langchain_chroma gives access to the underlying client via ._collection
        try:
            vector = self.vector_store
            count=0
            if vector:
                count = vector._collection.count()
        except AttributeError:
            count = 0

        if count == 0 and fallback_articles:
            print(
                f"Collection '{collection_name}' is empty. Indexing fallback articles..."
            )
            self.add_articles(fallback_articles)
        elif count > 0:
            print(
                f"Collection '{collection_name}' already contains {count} vectors. Ready to query."
            )
        else:
            print(
                f"Collection '{collection_name}' is initialized but empty. No raw articles provided."
            )

    def retrieve_similar_articles(
        self, query: str, top_k: int = 20
    ) -> List[Tuple[Any, float]]:
        """
        Searches the vector store for documents similar to the query.

        Returns:
            A list of Tuples containing the Document object and its similarity score.
        """
        if not self.vector_store:
            raise ValueError(
                "Vector store is not initialized. Call 'initialize_vector_store()' first."
            )

        if not query.strip():
            logger.warning("Empty search query received.")
            return []

        try:
            # Chroma returns low scores for high similarity (Distance metric)
            results = self.vector_store.similarity_search_with_score(
                query=query, k=top_k
            )
            return results
        except Exception as e:
            logger.error(f"Error during vector retrieval: {e}")
            raise
