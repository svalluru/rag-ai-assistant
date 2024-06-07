from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.redis import Redis
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_openai import OpenAI

redis_url = "redis://default:mypassword@localhost:6379"
index_name = "customerdataidx"
schema_name = "redis_schema.yaml"


embeddings = HuggingFaceEmbeddings()

rds = Redis.from_existing_index(
    embeddings,
    redis_url=redis_url,
    index_name=index_name,
    schema=schema_name)



#Work with a retriever
retriever = rds.as_retriever(search_type="similarity_distance_threshold", search_kwargs={"k": 2, "distance_threshold": 2})

retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

model_service = "http://localhost:62562/v1"

llm = OpenAI(base_url=model_service, 
             api_key="sk-no-key-required",
             streaming=True)

combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)

retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

response = retrieval_chain.invoke({"input": "what is OpenShift AI ?"})

print(response['answer'])

