import os
from chromadb import PersistentClient
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.tools import BaseTool
from langchain_core.documents import Document
from pydantic import Field, PrivateAttr
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.config.settings import settings


class VectorStore(BaseTool):
    """Tool for managing the vector store using ChromaDB."""
    name: str = "vectorstore"
    description: str = settings.VECTORSTORE_DESCRIPTION

    vectorstore: Chroma = Field(default_factory=Chroma)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        local_embeddings = OllamaEmbeddings(model=settings.EMBEDING_MODEL)
        persistent_client = PersistentClient()
        self.vectorstore = Chroma(
            client=persistent_client,
            collection_name="chatbot_collection",
            embedding_function=local_embeddings,
        )

    def _run(self, query: str) -> str:
        """Run the vector store tool.

        Args:
            query: The search query to look up.

        Returns:
            A string containing the search results in XML format.
        """
        try:
            results = self.vectorstore.similarity_search(query, k=3)
            if not results:
                return "No results found."

            return "\n".join([doc.page_content for doc in results])
        except Exception as e:
            return f"Error performing vector store operation: {str(e)}"

    def add_documents_from_folder(self, folder_path: str) -> str:
        """Add all documents from a folder into the vector store.

        Args:
            folder_path: The path to the folder containing documents.

        Returns:
            A string indicating the status of the operation.
        """
        try:
            if not os.path.exists(folder_path):
                return f"Folder '{folder_path}' does not exist."

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=50
            )

            documents = []
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        chunks = text_splitter.split_text(content)
                        for i, chunk in enumerate(chunks):
                            doc = Document(
                                page_content=chunk,
                                metadata={"filename": filename, "chunk_index": i}
                            )
                            documents.append(doc)

            self.vectorstore.add_documents(documents)

            return f"All documents from '{folder_path}' have been added to the vector store."
        except Exception as e:
            return f"Error adding documents to vector store: {str(e)}"
