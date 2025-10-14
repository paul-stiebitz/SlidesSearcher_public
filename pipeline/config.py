from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SlideSearcherSettings(BaseSettings):
    """
    All configurations for the slidesearche application. Automatically parsed from the environment.
    """

    # Configuration dict for environment parsing
    model_config = SettingsConfigDict(
        env_prefix="SLIDES_",        # Prefix for environment variables
        case_sensitive=False,        # Environment variables are not case-sensitive
        env_parse_none_str=True,     # Convert "None" string to Python None
    )

    # Path to the vision-language model used for slide/image analysis
    vision_model_path: Path = Field(
        alias="SLIDES_VISION_MODEL", 
        default="Qwen/Qwen2.5-VL-3B-Instruct"
    )

    # Path or identifier for the sentence transformer model for embeddings
    sentence_model_path: str = Field(
        alias="SLIDES_SENTENCE_MODEL", 
        default="all-mpnet-base-v2"
    )

    # Directory containing PowerPoint (.pptx) files
    pptx_dir: Path = Field(
        alias="SLIDES_PPTX_DIR", 
        default="../Files/PPTX_DIR/"
    )

    # Directory to store intermediate PDF files
    pdf_dir: Path = Field(
        alias="SLIDES_PDF_DIR", 
        default="../Files/PDF_DIR/"
    )

    # Directory to store slide images (PNG)
    output_dir: Path = Field(
        alias="SLIDES_IMG_DIR", 
        default="../Files/IMG_DIR/"
    )

    # Directory for ChromaDB database
    database_dir: Path = Field(
        alias="SLIDES_DB_DIR", 
        default="db/"
    )

    # Number of results to return from search
    n_results: int = 16

    # Port to run the web server on
    server_port: int = Field(
        alias="SLIDES_PORT", 
        default=7680
    )

    # Debug mode flag
    debug: bool = False


# Create a config instance that can be imported and used across the project
config = SlideSearcherSettings()
