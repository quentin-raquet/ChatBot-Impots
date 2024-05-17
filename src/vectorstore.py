import logging
import glob
import os
import requests
from typing import List, Dict
from getpass import getpass
from langchain_community.document_loaders import PyPDFLoader
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_env_or_getpass(env_var_name: str) -> None:
    """
    Get the value of an environment variable or prompt the user to enter it.

    Args:
        env_var_name (str): The name of the environment variable.

    Returns:
        str: The value of the environment variable or the user input.
    """
    if os.getenv(env_var_name) is None:
        os.environ[env_var_name] = getpass(f"Enter the value for {env_var_name}: ")


def download_files_if_not_exists(urls, folder_name="data"):
    """
    Download a file from a URL to a local folder if the folder doesn't already exist.

    Parameters:
    url (str): The URL of the file to download.
    folder_name (str): The local folder where the file should be saved.
    """
    if not os.path.exists(folder_name):
        logging.info(f"Create {folder_name} folder and dowload files")
        os.makedirs(folder_name)
        for url in urls:
            response = requests.get(url)
            with open(folder_name + "/" + url.split("/")[-1], "wb") as f:
                f.write(response.content)


def load_pdfs(folder: str) -> List[str]:
    """
    Load PDF files from a folder and return a list of their contents.

    Args:
        folder (str): The folder path.

    Returns:
        List[str]: The contents of the PDF files.
    """
    logging.info(f"Loading PDFs from folder: {folder}")
    results = []
    pdf_files = glob.glob(folder + "/*.pdf")
    for file in pdf_files:
        loader = PyPDFLoader(file)
        results += loader.load()
    logging.info(f"Loaded {len(results)} PDFs")
    return results


def build_vectorstore(config: Dict[str, str]) -> None:
    """
    Main function to create vectorstore.

    Args:
        config (Dict[str, str]): The configuration dictionary.
    """

    logging.info("Starting vectorestore creation")
    download_files_if_not_exists(config["data_urls"])
    if os.path.exists(config["persist_directory"]):
        logging.info("Vectorstore already exists. Exiting.")
        return
    # Load PDFs
    docs = load_pdfs(config["data_folder"])

    # Get environment variables or prompt user for input
    get_env_or_getpass("MISTRAL_API_KEY")
    get_env_or_getpass("HF_TOKEN")

    # Initialize embeddings
    embeddings = MistralAIEmbeddings(
        model=config["emb_model_id"],
    )
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config["chunk_size"], chunk_overlap=config["chunk_overlap"]
    )
    splits = text_splitter.split_documents(docs)
    # Create vector store
    Chroma.from_documents(
        persist_directory=config["persist_directory"],
        documents=splits,
        embedding=embeddings,
        collection_name=config["collection_name"],
    )
    logging.info("Vectorstore created")
