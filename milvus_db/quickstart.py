import random

from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)


# connect to a server
def connect_server(db_name, host, port):
    connections.connect(db_name=db_name, host=host, port=port)


# create a collection
def create_collection(collection_name):
    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="random", dtype=DataType.DOUBLE),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=8),
    ]
    schema = CollectionSchema(fields, "milvus quickstart")
    return Collection(collection_name, schema)


# insert vector in the collection
def insert_vector(collection):
    entities = [
        [i for i in range(3000)],
        [float(random.randrange(-20, -10)) for _ in range(3000)],
        [[random.random() for _ in range(8)] for _ in range(3000)]
    ]
    return collection.insert(entities)


# build index on the entity
def build_index(collection):
    index = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist", 128}
    }
    collection.create_index("embeddings", index)


# Load the collection to memory and performs a vector similarity search
def search_vector(collection):
    collection.load()
    entities = [
        [i for i in range(3000)],
        [float(random.randrange(-20, -10)) for _ in range(3000)],
        [[random.random() for _ in range(8)] for _ in range(3000)]
    ]
    query = entities[-1][-2:]
    search_params = {
        "metric_type": "L2",
        "params": {"nprobe": 10}
    }
    return collection.search(query, "embeddings", search_params, limit=3, output_fields=["random"])


if __name__ == '__main__':
    # 连接服务器
    connect_server("default", "localhost", 19530)
    # 创建 collection
    col = create_collection("milvus_col")
    # 创建索引
    build_index(col)
