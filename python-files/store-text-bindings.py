from kafka import KafkaConsumer
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.redis import Redis
#import logging

# To consume kafka messages
consumer = KafkaConsumer('customerdata',
                         bootstrap_servers=['my-cluster-kafka-bootstrap.sri-support-tech-app.svc.cluster.local:9092'],
                         auto_offset_reset='earliest', enable_auto_commit=False)

redis_url = "redis://default:q07rXXlq@my-doc-headless.sri-support-tech-app.svc.cluster.local:15928"
index_name = "customerdataidx"
schema_name = "redis_schema.yaml"

embeddings = HuggingFaceEmbeddings()

for message in consumer:
    str = message.value.decode()
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100000,
    chunk_overlap=10,
    length_function=len,
    is_separator_regex=False,)
    texts = text_splitter.create_documents([str])
    rds = Redis.from_documents(texts,
                           embeddings,
                           redis_url=redis_url,
                           index_name=index_name)
    rds.write_schema("redis_schema.yaml")                           
    rds.add_documents(texts)

#xml += ''.join(kafkadata)
print("before")
#print(xml)
#text_loader_kwargs={'autodetect_encoding': True}
#loader = DirectoryLoader('/Users/svalluru/PycharmProjects/openllm-langchain/kafkafiles', glob="*.txt", show_progress=True, loader_cls=TextLoader, silent_errors=True, loader_kwargs=text_loader_kwargs)
#docs = loader.load()
#print(docs)




