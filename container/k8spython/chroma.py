# Enable chromadb to be used with applications

import chromadb
import click
from chromadb.utils import embedding_functions
from .utils import run_async
from chromadb.config import Settings
from chromadb import AsyncClientAPI


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



async def embed_file(file: click.File) -> str:

    # client = await chromadb.AsyncHttpClient(host="localhost", port=8000)
    client = await connect_to_chroma_async("V3tt94YBCELOdbFr0YFONqwee176ZoJz")

    collection = await client.get_or_create_collection(name="my_collection")

    click.echo(f"Collection: {file.name}")
    ben = file.read()

    benstr = ben.decode("utf-8")
    click.echo(f"File: {benstr}")

    # click.echo(f"File: {ben.decode("utf-8")}")

    await collection.add(documents=[benstr], ids=["note000.txt"])

    results = await collection.query(
        query_texts=["This is a query document about hawaii"], # Chroma will embed this for you
        n_results=2 # how many results to return
    )

    click.echo(f"Results: {results}")

    return "thanks"


def embed(file: click.File):
    """
    Load a file into the chromadb as an embedding
    """


    text = "Hello, world!"

    if False:
        default_ef = embedding_functions.DefaultEmbeddingFunction()
        default_embed = default_ef.embed_with_retries([text])
        click.echo(f'Embedding of {text} is {default_embed}')

        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction()
        sentence_embed = sentence_transformer_ef.embed_with_retries([text])
        click.echo(f'Embedding of {text} is {sentence_embed}')

    result = run_async(embed_file(file))
    click.echo(result)


    # collection = client.get_or_create_collection(
    #     name="test", embedding_function=CustomEmbeddingFunction())




    # chromadb.embed(file)
