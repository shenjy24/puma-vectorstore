import json
import random

from pymilvus import MilvusClient


def prepare_data(client, collection):
    # Insert randomly generated vectors
    colors = ["green", "blue", "yellow", "red", "black", "white", "purple", "pink", "orange", "brown", "grey"]
    data = [{"id": i, "vector": [random.uniform(-1, 1) for _ in range(5)],
             "color": f"{random.choice(colors)}_{str(random.randint(1000, 9999))}"} for i in range(1000)]
    res = client.insert(collection_name=collection, data=data)
    print(res)


# 向量查询
def vector_search(client, collection, data, fields=None, filter=None, limit=5):
    res = client.search(
        collection_name=collection, data=data, limit=limit,
        search_params={"metric_type": "IP", "params": {}},
        output_fields=fields,   # 指定返回的字段
        filter=filter           # 过滤数据
    )
    return json.dumps(res, indent=4)


if __name__ == '__main__':
    # 1. Set up a Milvus client
    mc = MilvusClient(uri="http://localhost:19530")
    collection_name = "milvus_col"
    # 准备数据
    # prepare_data(collection_name)

    # single vector search
    search_params1 = [
        [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, -0.26286205330961354, 0.9029438446296592]]
    search_result1 = vector_search(mc, collection_name, search_params1, ["color"], 'color like "red%"')
    print(search_result1)

    # bulk vector search
    # search_params2 = [
    #     [0.19886812562848388, 0.06023560599112088, 0.6976963061752597, 0.2614474506242501, 0.838729485096104],
    #     [0.3172005263489739, 0.9719044792798428, -0.36981146090600725, -0.4860894583077995, 0.95791889146345]
    # ]
    # search_result2 = vector_search(mc, collection_name, search_params2)
    # print(search_result2)
