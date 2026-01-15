import numpy as np

from algorithm_finding_text.detector import detect_document, order_corners, warp_document


def synthetic_document(width=400, height=300, pad=50):
    """Create a synthetic image with a white rectangle on black background."""
    img = np.zeros((height, width, 3), dtype=np.uint8)
    cv2 = __import__("cv2")
    cv2.rectangle(img, (pad, pad), (width - pad, height - pad), (255, 255, 255), -1)
    return img


def test_order_corners():
    pts = np.array([[100, 200], [50, 50], [200, 50], [50, 300]], dtype="float32")
    ordered = order_corners(pts)
    # top-left should have smallest sum, bottom-right largest sum
    assert np.allclose(ordered[0], [50, 50])
    assert np.allclose(ordered[2], [50, 300])


def test_detect_document_on_synthetic():
    img = synthetic_document()
    corners, contour = detect_document(img, min_area_ratio=0.05)
    assert corners.shape == (4, 2)
    # corners roughly match padding
    xs, ys = corners[:, 0], corners[:, 1]
    assert xs.min() >= 40 and xs.max() <= 360
    assert ys.min() >= 40 and ys.max() <= 260


def test_warp_document_produces_flat_view():
    img = synthetic_document()
    corners, _ = detect_document(img, min_area_ratio=0.05)
    warped = warp_document(img, corners)
    # Warped image should be mostly white (document) with negligible black border
    white_ratio = (warped > 200).mean()
    assert white_ratio > 0.9
