from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import chromadb
from chromadb.utils import embedding_functions
import os
import json
import sys
from urllib.parse import unquote

# Add the pipeline directory to the system path so config.py can be imported
sys.path.append("./pipeline")
from config import config

# Initialize Flask app
app = Flask(__name__)

# -----------------------------
# Initialize ChromaDB
# -----------------------------
# Create a SentenceTransformer embedding function for query embeddings
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=config.sentence_model_path
)

# Connect to persistent ChromaDB instance
chroma_client = chromadb.PersistentClient(path="./pipeline/db")

# Get the collection "all_files" from ChromaDB
collection = chroma_client.get_collection(
    name="all_files", embedding_function=sentence_transformer_ef
)

# Store the last search results in memory
last_search_ids = []

# -----------------------------
# Flask Routes
# -----------------------------

@app.route('/')
def login():
    """Serve the login page."""
    return render_template('login.html')


@app.route('/index')
def index():
    """Serve the main index page after login."""
    return render_template('index.html')


@app.route('/IMG_DIR/<path:filename>')
def serve_img_dir(filename):
    """
    Serve images from the Files/IMG_DIR directory.

    Args:
        filename (str): path of the requested image (may contain URL-encoded characters)
    
    Returns:
        File: Image file from disk.
    """
    filename = unquote(filename)  # Decode URL-encoded characters (%28, %29 etc.)
    return send_from_directory('Files/IMG_DIR', filename)


@app.route('/search', methods=['POST'])
def search():
    """
    Search the ChromaDB collection for slides matching the query.

    Expects JSON data with a 'query' field:
        {"query": "AI benchmarks"}

    Returns:
        JSON: List of slides and their descriptions.
    """
    data = request.get_json()
    query = data.get('query', '')

    # Query the ChromaDB collection
    results = collection.query(
        query_texts=[query], n_results=config.n_results
    )

    global last_search_ids
    last_search_ids = results["ids"][0]

    # Clean the file paths to be relative to the Files directory
    last_search_ids = [path.replace("./FILES", "") for path in last_search_ids]

    slides = []
    for idx, slide_id in enumerate(last_search_ids):
        try:
            # Read the pre-generated description for each slide
            with open(f"{slide_id}.desc.txt", "r", encoding='latin-1') as f:
                description = f.read()
        except Exception as e:
            description = "No description available"

        # Format image path relative to Files directory for front-end
        image_path = slide_id.replace('Files/', '')
        slides.append({
            'imageUrl': image_path,
            'description': description,
            # Optionally include presentation name metadata
            # 'presentationName': presentation_name,
        })

    return jsonify({'slides': slides})


@app.route('/ask', methods=['POST'])
def ask():
    """
    Answer questions based on the descriptions of slides from the last search.

    Expects JSON data with a 'question' field:
        {"question": "What is AI benchmark performance?"}

    Returns:
        JSON: Answer generated using slide descriptions.
    """
    data = request.json
    question = data.get('question')

    if not last_search_ids:
        # Return error if no previous search has been done
        return jsonify({'answer': "Please search for slides first before asking a question."})

    # Read descriptions of all slides returned by last search
    text_images = []
    for slide_id in last_search_ids:
        try:
            with open(f"{slide_id}.desc.txt", "r", encoding='latin-1') as f:
                text_images.append(f.read())
        except Exception as e:
            # Skip slides if description cannot be read
            continue

    # Construct a prompt for LLM
    prompt = "Here are descriptions of Images:\n\n"
    for idx, desc in enumerate(text_images):
        prompt += f"Description {idx + 1}:\n{desc.strip()}\n\n"
    prompt += f"Here is the Question:\n{question}\n"
    prompt += "Please answer the question using only the context from the descriptions that are relevant to the question."

    # TODO: Implement LLM answer generation
    answer = ""

    return jsonify({'answer': answer})


# -----------------------------
# Run the Flask server
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7680, debug=True)
