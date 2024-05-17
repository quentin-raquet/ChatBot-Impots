import warnings
import logging
from typing import List, Dict
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def format_docs(docs: List[str]) -> str:
    """
    Format a list of document contents into a single string.

    Args:
        docs (List[str]): The list of document contents.

    Returns:
        str: The formatted string.
    """
    formatted_docs = "\n\n".join(doc.page_content for doc in docs)
    return formatted_docs


def ask_question(question: str, rag_chain) -> str:
    """
    Ask a question using the RAG (Retrieval-Augmented Generation) pipeline.

    Args:
        question (str): The question to ask.
        rag_chain (HuggingFacePipeline): The RAG pipeline.

    Returns:
        str: The generated answer.
    """
    answer = rag_chain.invoke(question)
    return answer


def build_rag(config: Dict[str, str]) -> None:
    """
    Main function to run the ChatBot.

    Args:
        config (Dict[str, str]): The configuration dictionary.
    """

    logging.info(
        f"Building RAG with embedding model: {config['emb_model_id']} and LLM model: {config['llm_model_id']}"
    )
    # Initialize embeddings
    embeddings = MistralAIEmbeddings(
        model=config["emb_model_id"],
    )

    # Create vector store
    vectorstore = Chroma(
        collection_name=config["collection_name"],
        persist_directory=config["persist_directory"],
        embedding_function=embeddings,
    )

    # Initialize RAG pipeline
    llm = ChatMistralAI(
        name=config["llm_model_id"],
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        random_seed=0,
    )

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": config["k"]})
    prompt = PromptTemplate.from_template(config["template"])
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    logging.info("RAG pipeline created")

    return rag_chain
