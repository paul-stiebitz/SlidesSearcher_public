SlideSearcher - Intelligent Slide Retrieval Augmented Generation (RAG) Search System

1. Project Overview
    SlideSearcher is an AI-powered system that processes PowerPoint presentations, converts each slide into an image, generates detailed textual descriptions using a vision-language model (e.g., Qwen2.5-VL), stores those descriptions in a ChromaDB vector database, and allows natural-language slide search through a Flask web application.

2. Folder Structure
    Slidesearcher/
    ├─ app.py                           # Flask web application entry point
    ├─ theme.py                         # Custom Gradio/IBM theme definitions
    ├─ pipeline/                        # Data processing and database scripts
    │  ├─ db/                           # ChromaDB vector database files
    │  ├─ config.py                     # Configuration settings and environment variables
    │  ├─ convert_from_pptx_to_pdf.py   # Converts PPTX → PDF → PNG slides
    │  ├─ describe_each_pdf.py          # Generates AI-based descriptions for slides (no multiprocessing)
    │  └─ upload_descriptions_to_db.py  # Uploads slide data into ChromaDB
    ├─ Files/                           # Input and output data
    │  ├─ PPTX_DIR/                     # Place your PowerPoint (.pptx) files here
    │  └─ IMG_DIR/                      # Generated images and description files
    ├─ templates/                       # HTML templates for Flask app
    │  ├─ index.html                    # Main slide search interface
    │  ├─ login.html                    # Login screen
    │  └─ main.html                     # Optional redirect or landing page
    ├─ .gitignore
    └─ README.md

3. Installation & Setup
    1. Create a Micromamba Environment:
    micromamba create -n rag_env python=3.11
    eval "$(micromamba shell hook --shell bash)"
    micromamba activate rag_env

    2. Clone Repository & Install Dependencies:
    git clone <github-repo-link>
    cd Slidesearcher_Public
    pip install Flask chromadb pydantic_settings sentence_transformers pdf2image accelerate torchvision gradio tqdm

    3. System Requirements (macOS):
    brew install --cask libreoffice
    brew install poppler

    4. Configuration
    All settings are handled through pipeline/config.py using the SlideSearcherSettings class.

    Environment variables (prefix: SLIDES_):
    - SLIDES_VISION_MODEL: Vision-language model (default Qwen/Qwen2.5-VL-3B-Instruct)
    - SLIDES_SENTENCE_MODEL: Sentence embedding model (default all-mpnet-base-v2)
    - SLIDES_PPTX_DIR: PowerPoint input directory (default ../Files/PPTX_DIR/)
    - SLIDES_IMG_DIR: Output image/description directory (default ../Files/IMG_DIR/)
    - SLIDES_DB_DIR: Vector database directory (default db/)
    - SLIDES_PORT: Flask port (default 7680)
    - SLIDES_DEBUG: Enable debug mode (default False)

5. Processing Pipeline

    1. Convert PowerPoints to Images:
    python pipeline/convert_from_pptx_to_pdf.py

    2. Generate Slide Descriptions:
    python pipeline/describe_each_pdf.py

    3. Upload Descriptions to ChromaDB:
    python pipeline/upload_descriptions_to_db.py

    4. Launch Flask Web Application:
       python app.py

6. Web Interface
    - index.html: Main interface with search bar, slide gallery, modal preview, and download button.
    - login.html: Login page; default credentials:
        - Username: power
        - Password: power
    - main.html: Optional redirect logic to enforce login.

7. Custom Theme - Defines IBMTheme for Gradio interfaces.
    - Primary color: IBM Blue
    - Fonts: IBM Plex Serif & IBM Plex Mono
    - Layout: Spacious, rounded components, consistent hierarchy.

8. Usage Workflow
    1. Place .pptx files into Files/PPTX_DIR/
    2. Run conversion, description, and upload scripts:
    python pipeline/convert_from_pptx_to_pdf.py
    python pipeline/describe_each_pdf.py
    python pipeline/upload_descriptions_to_db.py
    3. Start Flask application:
    python app.py
    4. Login and search slides via the web interface.

9. VS Code & Quick Commands
    micromamba create -n rag_env python=3.11
    micromamba activate rag_env
    pip install Flask chromadb pydantic_settings sentence_transformers pdf2image accelerate torchvision gradio tqdm
    python pipeline/convert_from_pptx_to_pdf.py
    python pipeline/describe_each_pdf.py
    python pipeline/upload_descriptions_to_db.py
    python app.py

10. Search & Query Logic
    - User enters a natural language query.
    - Query embedded using Sentence Transformer.
    - Similar embeddings retrieved from ChromaDB.
    - Top matching slides and descriptions displayed.

11. Example Output Directory
    Files/
    ├─ PPTX_DIR/
    │  ├─ Sales_Deck.pptx
    │  └─ Training_Manual.pptx
    └─ IMG_DIR/
    ├─ Sales_Deck/
    │  ├─ slide_1.png
    │  ├─ slide_1.png.desc.txt
    │  └─ slide_2.png.desc.txt
    └─ Training_Manual/
        ├─ slide_1.png
        └─ slide_1.png.desc.txt
