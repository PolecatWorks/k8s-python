# Enable chromadb to be used with applications

from typing import List
import chromadb
import click
from chromadb.utils import embedding_functions
from .utils import run_async
from chromadb.config import Settings
from chromadb import AsyncClientAPI
from .config import ChromaConfig
from dataclasses import dataclass


async def connect_to_chroma_async(api_token: str, host: str = "localhost") -> AsyncClientAPI:
    """
    Connect to ChromaDB instance asynchronously with authentication token

    Args:
        api_token (str): Authentication token
        host (str): ChromaDB host URL

    Returns:
        AsyncClient: Authenticated async ChromaDB client
    """


    ngs = Settings(
        chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
        chroma_client_auth_credentials=api_token,
        anonymized_telemetry=False,
        allow_reset=True,
        chroma_server_ssl_enabled=False,
    )

    # admin = chromadb.AdminClient(settings=ngs)



    # Initialize async client with authentication
    # TODO: Fix auth. had to disable auth to allow it to work
    client = await chromadb.AsyncHttpClient(
        host='127.0.0.1',
        port=8000,
        settings=ngs,
        headers={
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        # headers={
        #     "Authorization": f"Bearer {api_token}"
        # },
        # settings=Settings(
        #     chroma_client_auth_provider="token",
        #     chroma_client_auth_credentials=api_token,
        #     allow_reset=True,
        #     anonymized_telemetry=False,
        #     chroma_server_ssl_enabled=False,
        # )
    )

    return client


@dataclass
class DocDefinition():
    text: str
    ids: str


def files_to_docdefinitions(files: List[click.File]) -> List[DocDefinition]:
    """
    Convert a list of files to a list of DocDefinition objects

    Args:
        files (List[click.File]): List of files

    Returns:
        List[DocDefinition]: List of DocDefinition objects
    """
    return [DocDefinition(ids=file.name, text=file.read().decode("utf-8")) for file in files]


def embed(config: ChromaConfig,  collection_name: str, files: List[click.File]) -> List[str]:
    """
    Load a file into the chromadb as an embedding
    """

    if False:
        default_ef = embedding_functions.DefaultEmbeddingFunction()
        default_embed = default_ef.embed_with_retries([text])
        click.echo(f'Embedding of {text} is {default_embed}')

        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction()
        sentence_embed = sentence_transformer_ef.embed_with_retries([text])
        click.echo(f'Embedding of {text} is {sentence_embed}')

    async def embed_files():

        client = await connect_to_chroma_async(config.apikey, config.url)
        docDefs = files_to_docdefinitions(files)

        collection = await client.get_or_create_collection(name=collection_name)

        ids = [doc.ids for doc in docDefs]
        await collection.add(documents=[doc.text for doc in docDefs], ids=ids)

        return ids

    return run_async(embed_files())


def query(config: ChromaConfig,  collection_name: str, text: str, count: int) -> List[str]:
    """
    search for top n items in collection
    """

    async def query_text():

        client = await connect_to_chroma_async(config.apikey, config.url)

        collection = await client.get_or_create_collection(name=collection_name)

        results = await collection.query(query_texts=[text], n_results=count)

        return results

    return run_async(query_text())
