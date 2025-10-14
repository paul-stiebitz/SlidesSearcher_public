#!/usr/bin/env python
from enum import Enum, auto
from functools import cache
import logging
import torch
import os
from typing import Optional
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions
from chromadb.utils.embedding_functions.sentence_transformer_embedding_function import (
    SentenceTransformerEmbeddingFunction,
)
from chromadb import Collection
from tqdm import tqdm

from config import config  # Import project configuration

# Optional import for describing images
# Commented out because descriptions are already pre-generated
# try:
#     from describe_each_pdf import describe_image
# except ModuleNotFoundError:
#     from describe_each_pdf import describe_image

# Detect if CUDA is available, else fall back to CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
logger = logging.getLogger(__name__)  # Module logger


class CollectionStatus(Enum):
    """Enum representing status of a ChromaDB collection operation."""
    COLLECTION_CREATED = auto()       # Collection was created
    COLLECTION_EXISTS = auto()        # Collection already exists
    COLLECTION_CREATION_FAILED = auto()  # Failed to create collection


@cache
def _get_sentence_transformer(
    model_name: str = "all-mpnet-base-v2",
) -> SentenceTransformerEmbeddingFunction:
    """
    Lazy-loads a SentenceTransformer embedding function for ChromaDB.

    Args:
        model_name (str, optional): Name of the embedding model. Defaults to "all-mpnet-base-v2".

    Returns:
        SentenceTransformerEmbeddingFunction: Function to compute embeddings for ChromaDB.
    """
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=model_name
    )


def ensure_collection(
    client: chromadb.ClientAPI, collection_name: str
) -> tuple[CollectionStatus, Optional[Collection]]:
    """
    Get a collection from ChromaDB. If it doesn't exist, create it.

    Args:
        client (chromadb.ClientAPI): The ChromaDB client instance.
        collection_name (str): Name of the collection to fetch or create.

    Returns:
        tuple[CollectionStatus, Optional[Collection]]: Status of operation and the collection instance
        (None if creation failed).
    """
    try:
        # Try to get existing collection
        collection = client.get_collection(
            name=collection_name, embedding_function=_get_sentence_transformer()
        )
        logger.debug(f"Collection '{collection_name}' already exists.")
        return CollectionStatus.COLLECTION_EXISTS, collection

    except Exception:
        # If collection doesn't exist, attempt to create it
        try:
            collection = client.create_collection(
                name=collection_name, embedding_function=_get_sentence_transformer()
            )
            logger.debug(f"Collection '{collection_name}' created successfully.")
            return CollectionStatus.COLLECTION_CREATED, collection
        except Exception as e:
            # Log any errors during creation
            logger.exception(f"Failed to create collection '{collection_name}': {e}")
            return CollectionStatus.COLLECTION_CREATION_FAILED, None


def insert_files_into_db(db_dir: str):
    """
    Creates or opens a ChromaDB database and inserts all PNG slides from the output directory.

    Each image description (.desc.txt) is read and added to a collection called 'all_files'.

    Args:
        db_dir (str): Directory where ChromaDB stores its data.
    """
    print("db_dir")
    print(db_dir)
    db_dir = str(db_dir)
    chroma_client = chromadb.PersistentClient(path=db_dir)  # Persistent ChromaDB client

    # Ensure 'all_files' collection exists
    collection_status, collection = ensure_collection(chroma_client, "all_files")

    # Iterate over presentations
    for folder in tqdm(os.listdir(config.output_dir), desc="Inserting Presentations"):
        # Iterate over slides in each presentation folder
        for file in tqdm(
            os.listdir(config.output_dir / folder), desc="Describing Slides"
        ):
            print(file)
            if ".desc.txt" not in str(file):
                img_path = config.output_dir / folder / file

                # Optionally generate description dynamically
                # output = describe_image(
                #     Path(img_path), model_path=str(config.vision_model_path)
                # )

                # Read pre-generated description
                output = open(str(img_path) + ".desc.txt")
                output = output.read()

                # Add description and metadata to collection
                collection.add(
                    documents=[output],
                    metadatas=[{"image_path": str(img_path), "presentation": str(folder)}],
                    ids=[str(img_path)],
                )


if __name__ == "__main__":
    # Set logging level depending on debug mode in config
    logging.basicConfig(level=logging.DEBUG if config.debug else logging.INFO)
    # Insert all image descriptions into the database
    insert_files_into_db(config.database_dir)
