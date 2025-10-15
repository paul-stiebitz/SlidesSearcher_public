# SlideSearcher – Intelligent Slide Retrieval Augmented Generation (RAG) System

This repository demonstrates how to set up an **AI-powered slide retrieval system** that processes PowerPoint presentations, generates detailed AI-based slide descriptions, and enables **semantic search** through a **Flask web interface**. It integrates **vision-language models**, **sentence embeddings**, and a **vector database (ChromaDB)** to deliver a complete Retrieval-Augmented Generation (RAG) pipeline for slides.

---

## 📦 Key Components
- **Flask** – Web application for interactive slide search  
- **Micromamba + Python** – Lightweight environment management  
- **ChromaDB** – Vector database for embedding and retrieval  
- **Qwen2.5-VL (Hugging Face)** – Vision-language model for slide description  
- **Sentence Transformers (Hugging Face)** – Text embeddings for semantic search  
- **PDF2Image + LibreOffice** – PowerPoint to PNG conversion pipeline  
- **Gradio + IBMTheme** – Custom UI design integration  

---

## 🧰 Prerequisites
Install required system packages (example for macOS):

```bash
brew install --cask libreoffice
brew install poppler
```

For Linux systems (Power or x86):

```bash
sudo dnf install git poppler-utils libreoffice
```

Clone the project repository:

```bash
git clone https://github.com/HenrikMader/SlidesSearcher_public.git
cd Slidesearcher_Public
```

---

## 🐍 Environment Setup

### 1. Install Micromamba
```bash
cd ~
curl -Ls https://micro.mamba.pm/api/micromamba/linux-ppc64le/latest | tar -xvj bin/micromamba
eval "$(micromamba shell hook --shell bash)"
micromamba --version
```

### 2. Create a Python Environment
```bash
micromamba create -n rag_env_slides python=3.11
micromamba activate rag_env_slides
```

### 3. Install Dependencies

Install project dependencies via pip:
```bash
pip install Flask chromadb pydantic_settings sentence_transformers pdf2image accelerate torchvision gradio tqdm transformers
```

Check installed packages:
```bash
pip list
```

---

## 🗃️ Build the Vector Database
Navigate to the project directory:
```bash
cd ~/Slidesearcher_Public
rm -rf pipeline/db
```

Convert PowerPoints to image slides:
```bash
python pipeline/convert_from_pptx_to_pdf.py
```

Generate AI-based slide descriptions:
```bash
python pipeline/describe_each_pdf.py
```

Upload the slide embeddings and descriptions to ChromaDB:
```bash
python pipeline/upload_descriptions_to_db.py
```

This process will create or update your vector database in `pipeline/db/`.

---

## ⚙️ Run the Web Application
Start the Flask web interface:
```bash
python app.py
```

Access the web UI in your browser:
```
http://<IP_of_your_machine>:7680
```

Login credentials:
- **Username:** power  
- **Password:** power  
(Login credentials can be changed inside templates/login.html file)

---

## 🧩 Manage the Vector Database
To rebuild or refresh the database, re-run the ingestion scripts:
```bash
python pipeline/convert_from_pptx_to_pdf.py
python pipeline/describe_each_pdf.py
python pipeline/upload_descriptions_to_db.py
```

The database automatically indexes each slide image and its AI-generated description for fast semantic retrieval.

---

## 🔍 Query the Slide Search System
Once the web app is running, you can:
- Enter **natural language queries** (e.g., “Show slides about sales trends”)
- SlideSearcher will:
  1. Embed your query using Sentence Transformers  
  2. Retrieve top similar embeddings from ChromaDB  
  3. Display matching slides and their AI-generated descriptions  

Example workflow:
1. Place `.pptx` files into `Files/PPTX_DIR/`
2. Run the ingestion scripts
3. Start Flask:  
   ```bash
   python app.py
   ```
4. Access the web app and start searching.

---

## 🌐 Web Interface Overview
- **index.html** – Main search UI with gallery, modal preview, and download options  
- **login.html** – Secure login interface  
- **main.html** – Optional redirect or post-login landing page  

Default port: `7680`

---

## 🎨 Custom Theme (IBMTheme)
Defines a unified Gradio-based interface theme:
- **Primary color:** IBM Blue  
- **Fonts:** IBM Plex Serif & IBM Plex Mono  
- **Layout:** Rounded cards, clear spacing, modern hierarchy  

---

## 📁 Folder Structure
```
Slidesearcher/
├─ app.py                           # Flask web app entry point
├─ theme.py                         # IBM Gradio theme definitions
├─ pipeline/                        # Processing and database scripts
│  ├─ db/                           # ChromaDB files
│  ├─ config.py                     # Configuration settings
│  ├─ convert_from_pptx_to_pdf.py   # Converts PPTX → PDF → PNG
│  ├─ describe_each_pdf.py          # AI-based slide descriptions
│  └─ upload_descriptions_to_db.py  # Uploads to ChromaDB
├─ Files/
│  ├─ PPTX_DIR/                     # Input PowerPoints
│  └─ IMG_DIR/                      # Output images/descriptions
├─ templates/
│  ├─ index.html
│  ├─ login.html
│  └─ main.html
└─ README.md
```

---

## 🗂️ Example Output Directory
```
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
```

---

## 🤗 Model Sources (Hugging Face)
SlideSearcher retrieves models directly from the [Hugging Face Hub](https://huggingface.co/):

- **Vision Model:** `Qwen/Qwen2.5-VL-3B-Instruct`  
- **Sentence Embedding Model:** `all-mpnet-base-v2`  

You can replace these models in `pipeline/config.py` using your preferred Hugging Face repositories.

---

## 🔗 Additional Resources
- [ChromaDB Documentation](https://docs.trychroma.com/)  
- [Hugging Face Models](https://huggingface.co/models)  
- [IBM Plex Typeface](https://www.ibm.com/plex/)  
- [Qwen2.5-VL Model Card](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)

