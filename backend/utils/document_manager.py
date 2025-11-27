"""
Document management for uploaded content.
"""
from typing import Optional


class DocumentManager:
    """Manages the currently loaded document content."""

    def __init__(self):
        self._content: Optional[str] = None

    @property
    def content(self) -> Optional[str]:
        """Get the current document content."""
        return self._content

    @content.setter
    def content(self, value: Optional[str]) -> None:
        """Set the document content."""
        self._content = value.strip() if value else None

    @property
    def is_loaded(self) -> bool:
        """Check if a document is currently loaded."""
        return self._content is not None and len(self._content) > 0

    @property
    def length(self) -> int:
        """Get the length of the current document."""
        return len(self._content) if self._content else 0

    def clear(self) -> None:
        """Clear the current document."""
        self._content = None

    def get_status(self) -> dict:
        """Get status information about the document."""
        return {
            "document_loaded": self.is_loaded,
            "document_length": self.length
        }


# Global document manager instance
document_manager = DocumentManager()
