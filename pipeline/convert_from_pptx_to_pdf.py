#!/usr/bin/env python
import logging
import os
from pathlib import Path
import platform
import subprocess
import sys

from pdf2image import convert_from_path  # Converts PDF pages to images
from tqdm import tqdm  # Progress bar for loops

from config import config  # Import project configuration

# Create a logger for this module
logger = logging.getLogger(__name__)


def convert_file(input_file: Path, output_dir: Path) -> None:
    """
    Converts a single PowerPoint (.pptx) file to PDF and stores it in the output directory.

    Args:
        input_file (Path): The PowerPoint file to convert.
        output_dir (Path): Directory where the resulting PDF should be saved.

    Raises:
        OSError: If the OS is unsupported.
        ValueError: If the output_dir exists but is not a directory.
    """
    current_os = platform.system()  # Detect current operating system

    # Validate or create the output directory
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError(
            f"output dir '{output_dir}' passed to convert_file is not directory!"
        )
    elif not output_dir.exists():
        os.mkdir(output_dir)

    # Windows-specific conversion using PowerPoint
    if current_os == "Windows":
        # NOTE: Requires PowerPoint installed on Windows
        from pptxtopdf import convert
        convert(input_file, output_dir)

    # Linux or macOS conversion using LibreOffice
    elif current_os == "Linux" or current_os == "Darwin":
        cmd = "soffice"  # Default LibreOffice command
        if current_os == "Darwin":
            cmd = "/Applications/LibreOffice.app/Contents/MacOS/soffice"  # macOS path

        # Run LibreOffice in headless mode to convert PPTX -> PDF
        subprocess.run(
            [
                cmd,
                "--headless",
                "--convert-to",
                "pdf",
                f"{input_file}",
                "--outdir",
                f"{output_dir}",
            ],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
    else:
        # Unsupported operating system
        raise OSError(
            f"unsupported operating system '{current_os}' in use. Cannot convert PPTX files to pdfs. please do so manually!"
        )


def convert_files_in_dir(
    pptx_dir: Path, output_dir: Path, delete_intermediates: bool = True
) -> None:
    """
    Converts all PowerPoint files in a directory into PNG images for each slide.
    Each presentation gets its own sub-folder in output_dir.

    Args:
        pptx_dir (Path): Directory containing PowerPoint files.
        output_dir (Path): Parent directory to store sub-folders for each presentation.
        delete_intermediates (bool, optional): If True, PDF files are deleted after conversion.
    """
    logger.debug(f"Starting to convert files from {pptx_dir}")

    # Loop through all files in the input directory
    for file in tqdm(os.listdir(pptx_dir), desc="Processing Powerpoints"):
        logger.debug(f"converting file {file}.")
        name, ext = os.path.splitext(file)

        # Skip files that are not PowerPoint presentations
        if ext.lower() not in (".ppt", ".pptx"):
            logger.debug(f"file {file} is not a supported presentation.")
            continue

        input_file = pptx_dir / file

        # Create output sub-folder for this presentation if it doesn't exist
        if not os.path.isdir(output_dir / name):
            logger.debug("Output dir does not exist, creating.")
            os.mkdir(output_dir / name)

        pdf_file_name = name + ".pdf"

        # Convert to PDF if it hasn't been converted yet
        if not (output_dir / name / pdf_file_name).exists():
            logger.debug(f"creating PDF for {file}")
            convert_file(input_file, output_dir / name)
            
            # Convert PDF pages to PNG images (one image per slide)
            convert_from_path(
                output_dir / name / pdf_file_name,
                output_folder=output_dir / name,
                fmt="png",
                size=(800, None),  # Keep width 800px, preserve aspect ratio
            )
        else:
            logger.debug(f"file {file} already was converted to a PDF.")

        # Optionally delete the intermediate PDF file
        if delete_intermediates:
            os.remove(output_dir / name / pdf_file_name)


# Run the script directly
if __name__ == "__main__":
    logging.basicConfig()  # Initialize logging
    convert_files_in_dir(config.pptx_dir, config.output_dir, delete_intermediates=False)
