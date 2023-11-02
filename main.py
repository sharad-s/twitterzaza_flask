
from flask import Flask, request, jsonify
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
from utils import to_dict
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Get Env vars
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# Initialize Pinecone only once, outside the endpoint, to avoid re-initialization overhead
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)

def get_vector_store():
    embed_model = OpenAIEmbeddings(model="text-embedding-ada-002")
    text_field = "text"
    index_name = PINECONE_INDEX_NAME

    index = pinecone.Index(index_name)

    # Initialize the Pinecone vector store
    vectorstore = Pinecone(
        index, embed_model.embed_query, text_field
    )
    return vectorstore


@app.route('/search', methods=['POST'])
def similarity_search():
    # Extract the query from the POST request
    data = request.json
    query = data.get('query')
    limit = data.get('limit')
    limit = int(limit) if limit else 10
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Get the vector store
    vectorstore = get_vector_store()

    # Perform the similarity search
    sim = vectorstore.similarity_search(query, k=limit)
    res = to_dict(sim)

    return jsonify(res)

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
