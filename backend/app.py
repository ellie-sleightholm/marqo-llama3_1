from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import marqo
from ai_chat import answer
from typing import List
from knowledge_store import MarqoKnowledgeStore
import document_processors
from document_processors import (
    simple_chunker,
    simple_denewliner,
    sentence_chunker,
    sentence_pair_chunker,
)

# Configuration
INDEX_NAME = "knowledge-management"
MARQO_CLIENT_URL = "http://localhost:8882"
KNOWLEDGE_ATTR = "knowledge"
CHUNK_SIZE = 512

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Marqo Client and Knowledge Store
CLIENT = marqo.Client(MARQO_CLIENT_URL)
document_processors.CHUNK_SIZE = CHUNK_SIZE

MKS = MarqoKnowledgeStore(
    CLIENT,
    INDEX_NAME,
    document_chunker=sentence_pair_chunker,
    document_cleaner=simple_denewliner,
)
MKS.reset_index()

def get_document_text(url: str) -> str:
    """Fetch the text content from a webpage given its URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.get_text()

@app.route("/getKnowledge", methods=["POST"])
def get_knowledge():
    """Endpoint to retrieve knowledge based on a query."""
    data = request.get_json()
    q: str = data.get("q")
    limit: int = data.get("limit", 5)
    return Response(
        stream_with_context(answer(q, MKS, limit)),
        mimetype="text/plain",
    )

@app.route("/addKnowledge", methods=["POST"])
def add_knowledge():
    """Endpoint to add a document to the knowledge index."""
    data = request.get_json()
    document = data.get("document")
    if document:
        MKS.add_document(document)
        return {"message": "Knowledge added successfully"}
    return {"error": "No document provided"}, 400

@app.route("/addWebpage", methods=["POST"])
def add_webpage():
    """Endpoint to add a webpage's content to the knowledge index."""
    data = request.get_json()
    url = data.get("URL")
    if url:
        document = get_document_text(url)
        MKS.add_document(document)
        return {"message": "Knowledge added successfully"}
    return {"error": "No URL provided"}, 400

if __name__ == "__main__":
    app.run(debug=True)
