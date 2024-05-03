from milvus_model.hybrid import BGEM3EmbeddingFunction
from milvus_model.sparse import BM25EmbeddingFunction
from pymilvus import model


def default_embedding():
    # This will download "all-MiniLM-L6-v2", a light weight model.
    ef = model.DefaultEmbeddingFunction()

    # Data from which embeddings are to be generated
    docs = [
        "Artificial intelligence was founded as an academic discipline in 1956.",
        "Alan Turing was the first person to conduct substantial research in AI.",
        "Born in Maida Vale, London, Turing was raised in southern England.",
    ]

    embeddings = ef.encode_documents(docs)

    # Print embeddings
    print("Embeddings:", embeddings)
    # Print dimension and shape of embeddings
    print("Dim:", ef.dim, embeddings[0].shape)


def bge_m3_embedding():
    # 1. prepare a small corpus to search
    docs = [
        "Artificial intelligence was founded as an academic discipline in 1956.",
        "Alan Turing was the first person to conduct substantial research in AI.",
        "Born in Maida Vale, London, Turing was raised in southern England.",
    ]
    query = "Who started AI research?"

    # BGE-M3 model can embed texts as dense and sparse vectors.
    # It is included in the optional `model` module in pymilvus, to install it,
    # simply run "pip install pymilvus[model]".

    bge_m3_ef = BGEM3EmbeddingFunction(use_fp16=False, device="cpu")

    docs_embeddings = bge_m3_ef(docs)
    query_embeddings = bge_m3_ef([query])


def bm25_embedding():
    # 1. prepare a small corpus to search
    docs = [
        "Artificial intelligence was founded as an academic discipline in 1956.",
        "Alan Turing was the first person to conduct substantial research in AI.",
        "Born in Maida Vale, London, Turing was raised in southern England.",
    ]
    query = "Where was Turing born?"
    bm25_ef = BM25EmbeddingFunction()

    # 2. fit the corpus to get BM25 model parameters on your documents.
    bm25_ef.fit(docs)

    # 3. store the fitted parameters to disk to expedite future processing.
    bm25_ef.save("bm25_params.json")

    # 4. load the saved params
    new_bm25_ef = BM25EmbeddingFunction()
    new_bm25_ef.load("bm25_params.json")

    docs_embeddings = new_bm25_ef.encode_documents(docs)
    query_embeddings = new_bm25_ef.encode_queries([query])
    print("Dim:", new_bm25_ef.dim, list(docs_embeddings)[0].shape)


if __name__ == '__main__':
    default_embedding()
