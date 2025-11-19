from typing import Any
from multiprocessing import Lock
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import numpy as np

load_dotenv(dotenv_path=find_dotenv())

def get_embeddinds(texts: list[str]) -> list[np.array]:
    client = OpenAI()

    embeddings: CreateEmbeddingResponse = client.embeddings.create(
        model='Qwen/Qwen3-Embedding-0.6B', input=texts
    )
    numpy_arrays: list[Any] = []
    for emb in embeddings.data:
        numpy_arrays.append(np.array(emb.embedding))
    return embeddings

if __name__ == "__main__":
    embeddings: list[Any] = get_embeddinds(texts=["мужчина"])
    print(embeddings)