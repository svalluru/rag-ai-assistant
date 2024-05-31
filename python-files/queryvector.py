from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.redis import Redis

#redis_url = "redis://default:mypassword@localhost:6379"
redis_url = "redis://default:q07rXXlq@my-doc-headless.sri-support-tech-app.svc.cluster.local:15928"
index_name = "customerdataidx"
schema_name = "redis_schema.yaml"


embeddings = HuggingFaceEmbeddings()

rds = Redis.from_existing_index(
    embeddings,
    redis_url=redis_url,
    index_name=index_name,
    schema=schema_name)

query="what is OpenShift AI ?"

#Make a query to the index
results =rds.similarity_search(query, k=4, return_metadata=True)

#Work with a retriever
retriever = rds.as_retriever(search_type="similarity_distance_threshold", search_kwargs={"k": 4, "distance_threshold": 2})
docs = retriever.invoke(query)
print(docs)
