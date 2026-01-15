from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence, Tuple

import cv2
import numpy as np


Point = Tuple[float, float]


@dataclass
class DetectionResult:
    corners: np.ndarray  # shape (4, 2) ordered TL, TR, BR, BL
    warped: np.ndarray
    contour: np.ndarray


def order_corners(pts: np.ndarray) -> np.ndarray:
    """Order 4 points as top-left, top-right, bottom-right, bottom-left."""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def detect_document(image: np.ndarray, *, min_area_ratio: float = 0.2) -> Tuple[np.ndarray, np.ndarray]:
    """
    Detect the largest 4-point contour (document) in the image.
    Returns (ordered_corners, contour). Raises ValueError if not found.
    """
    if image is None or image.size == 0:
        raise ValueError("Image is empty or None")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No contours found")

    h, w = gray.shape
    min_area = h * w * min_area_ratio

    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx) == 4:
            ordered = order_corners(approx.reshape(4, 2).astype("float32"))
            return ordered, approx

    # fallback: bounding box of largest contour
    largest = contours[0]
    x, y, bw, bh = cv2.boundingRect(largest)
    box = np.array([[x, y], [x + bw, y], [x + bw, y + bh], [x, y + bh]], dtype="float32")
    return order_corners(box), largest


def warp_document(
    image: np.ndarray,
    corners: Sequence[Point],
    *,
    output_size: Optional[Tuple[int, int]] = None,
) -> np.ndarray:
    """Warp the document defined by `corners` to a top-down view."""
    pts = np.array(corners, dtype="float32")
    ordered = order_corners(pts)

    (tl, tr, br, bl) = ordered
    width_top = np.linalg.norm(tr - tl)
    width_bottom = np.linalg.norm(br - bl)
    height_right = np.linalg.norm(tr - br)
    height_left = np.linalg.norm(tl - bl)
    max_width = int(max(width_top, width_bottom))
    max_height = int(max(height_right, height_left))

    if max_width == 0 or max_height == 0:
        raise ValueError("Invalid corner geometry for warp")

    if output_size:
        max_width, max_height = output_size

    dst = np.array(
        [
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1],
        ],
        dtype="float32",
    )

    matrix = cv2.getPerspectiveTransform(ordered, dst)
    warped = cv2.warpPerspective(image, matrix, (max_width, max_height))
    return warped


def process_image(path: Path, output: Optional[Path] = None, *, generator: str = "numpy") -> DetectionResult:
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Cannot read image: {path}")
    corners, contour = detect_document(image)
    warped = warp_document(image, corners)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output), warped)
    return DetectionResult(corners=corners, warped=warped, contour=contour)


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Detect document in an image and warp it to top-down view.")
    parser.add_argument("image", type=Path, help="Path to input image.")
    parser.add_argument("-o", "--output", type=Path, help="Path to save the warped image.")
    parser.add_argument("--min-area-ratio", type=float, default=0.2, help="Minimum area ratio for document contour.")
    args = parser.parse_args(argv)

    image = cv2.imread(str(args.image))
    if image is None:
        raise SystemExit(f"Cannot read image: {args.image}")

    corners, contour = detect_document(image, min_area_ratio=args.min_area_ratio)
    warped = warp_document(image, corners)
    print("Corners (TL, TR, BR, BL):")
    for idx, pt in enumerate(corners):
        print(f"{idx}: ({pt[0]:.1f}, {pt[1]:.1f})")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(args.output), warped)
        print(f"Warped image saved to {args.output}")


if __name__ == "__main__":  # pragma: no cover
    main()
