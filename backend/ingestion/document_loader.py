"""
Document loader for various file formats
"""
import os
from pathlib import Path
from typing import List, Dict, Any
import json
from utils.logger import logger


class DocumentLoader:
    """Load documents from various file formats"""

    def __init__(self, documents_dir: str = "/app/data/documents"):
        self.documents_dir = Path(documents_dir)

    def load_all_documents(self) -> List[Dict[str, Any]]:
        """
        Load all documents from the documents directory

        Returns:
            List of dicts with 'content' and 'metadata'
        """
        documents = []

        if not self.documents_dir.exists():
            logger.warning(f"Documents directory not found: {self.documents_dir}")
            return documents

        # Recursively find all supported files
        for file_path in self.documents_dir.rglob("*"):
            if file_path.is_file() and self._is_supported_format(file_path):
                try:
                    doc = self._load_file(file_path)
                    if doc:
                        documents.append(doc)
                        logger.debug(f"Loaded: {file_path.name}")
                except Exception as e:
                    logger.error(f"Failed to load {file_path}: {e}")

        logger.info(f"Loaded {len(documents)} documents total")
        return documents

    def _is_supported_format(self, file_path: Path) -> bool:
        """Check if file format is supported"""
        supported_extensions = {".md", ".txt", ".json"}
        return file_path.suffix.lower() in supported_extensions

    def _load_file(self, file_path: Path) -> Dict[str, Any]:
        """Load a single file and return document dict"""
        # Determine document type from directory structure
        relative_path = file_path.relative_to(self.documents_dir)
        parts = relative_path.parts

        doc_type = parts[0] if len(parts) > 1 else "general"

        # Load content based on file type
        if file_path.suffix == ".json":
            content = self._load_json(file_path)
        else:
            content = self._load_text(file_path)

        # Build metadata
        metadata = {
            "source": str(relative_path),
            "filename": file_path.name,
            "type": doc_type,
            "format": file_path.suffix[1:],  # Remove the dot
        }

        return {
            "content": content,
            "metadata": metadata
        }

    def _load_text(self, file_path: Path) -> str:
        """Load text or markdown file"""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _load_json(self, file_path: Path) -> str:
        """Load JSON file and convert to readable text"""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Convert JSON to formatted string
            return json.dumps(data, indent=2)
