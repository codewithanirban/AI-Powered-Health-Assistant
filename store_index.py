from src.helper import load_pdf_file, text_split, download_hugging_face_embedding
from pinecone import Pinecone, ServerlessSpec
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv
import os
import pinecone

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


extracted_data = load_pdf_file(data='Data/')
text_chunk = text_split(extracted_data)
embeddings = download_hugging_face_embedding()


pc = Pinecone(api_key=PINECONE_API_KEY)
# Initialize Pinecone
# pinecone.init(api_key="PINECONE_API_KEY", environment="us-east-1")

index_name = "medichat"

pinecone.create_index(
    name=index_name,
    dimension=384, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)

# Embed each chunk and upsert the embeddings into your Pinecone index
docsearch = Pinecone.from_documents(
    documents=text_chunk,
    index_name=index_name,
    embedding=embeddings
)

