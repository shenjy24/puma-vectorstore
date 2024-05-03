from pymilvus import FieldSchema, CollectionSchema, DataType, Collection, connections, MilvusClient


def create_collection(client, db_name, collection_name):
    id_field = FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, description="primary id")
    age_field = FieldSchema(name="age", dtype=DataType.INT64, description="age")
    embedding_field = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=128, description="vector")

    # Enable partition key on a field if you need to implement multi-tenancy based on the partition-key field
    position_field = FieldSchema(name="position", dtype=DataType.VARCHAR, max_length=256, is_partition_key=True)

    # Set enable_dynamic_field to True if you need to use dynamic fields.
    schema = CollectionSchema(fields=[id_field, age_field, embedding_field], auto_id=False, enable_dynamic_field=True,
                              description="desc of a collection")

    client.create_collection()
    return Collection(name=collection_name, schema=schema, using=db_name, shards_num=2)


if __name__ == '__main__':
    conn = connections.connect(host="localhost", port=19530)
    mc = MilvusClient(uri="http://localhost:19530")
    create_collection("book", "book1")
