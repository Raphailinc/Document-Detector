"""
Tools to detect a document (paper) in an image and warp it to a flat, top-down view.

Key functions:
- detect_document(image): returns ordered corners of the detected document.
- warp_document(image, corners): performs perspective warp to full image size or custom size.
"""

from .detector import detect_document, order_corners, warp_document

__all__ = ["detect_document", "order_corners", "warp_document"]
