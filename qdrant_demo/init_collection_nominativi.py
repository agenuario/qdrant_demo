import json
import os.path

from qdrant_client import QdrantClient, models
from tqdm import tqdm

from qdrant_demo.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, TEXT_FIELD_NAME, EMBEDDINGS_MODEL


def upload_embeddings():
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        prefer_grpc=True,
    )

    client.set_model(EMBEDDINGS_MODEL)

    payload_path = os.path.join(DATA_DIR, 'nominativi.json')
    payload = []
    documents = []

    # returns JSON object as a dictionary
    with open(payload_path, encoding='utf-8') as fh:
        data = json.load(fh)
        for obj in data:
            documents.append(obj.pop('descrizione'))
            payload.append(obj)

    client.recreate_collection(
        collection_name='nominativi',
        vectors_config=client.get_fastembed_vector_params(on_disk=True),
        # Quantization is optional, but it can significantly reduce the memory usage
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                quantile=0.99,
                always_ram=True
            )
        )
    )

    # Create a payload index for text field.
    # This index enables text search by the TEXT_FIELD_NAME field.
    client.create_payload_index(
        collection_name='nominativi',
        field_name=TEXT_FIELD_NAME,
        field_schema=models.TextIndexParams(
            type=models.TextIndexType.TEXT,
            tokenizer=models.TokenizerType.WORD,
            min_token_len=2,
            max_token_len=20,
            lowercase=True,
        )
    )

    client.add(
        collection_name='nominativi',
        documents=documents,
        metadata=payload,
        ids=tqdm(range(len(payload))),
        parallel=6,
    )


if __name__ == '__main__':
    upload_embeddings()
