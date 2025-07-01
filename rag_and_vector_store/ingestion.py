import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
load_dotenv()

loader = TextLoader('rag_and_vector_store\mediumblog1.txt',  encoding="utf-8")
document = loader.load()
# if you want to load the data from any other third party source (whatsapp messages, mails etc.)
#just implement the specific loader for that source and call load()

print("splitting...")
text_splitter = CharacterTextSplitter(chunk_size=1000,chunk_overlap=0)
texts = text_splitter.split_documents(document)
print(f"created {len(texts)} chunks")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("ingesting...")
PineconeVectorStore.from_documents(texts, embeddings, index_name = os.environ["INDEX_NAME"])

