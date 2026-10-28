# Document Detector

[![CI](https://github.com/Raphailinc/Document-Detector/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphailinc/Document-Detector/actions/workflows/ci.yml)

[English](README.md) · [Русский](README.ru.md)

A focused computer-vision project that locates a document-shaped quadrilateral and transforms it into a top-down view.

## What it does

- Detect a large four-corner contour using OpenCV.
- Order corners consistently before applying a perspective transform.
- Use the same functions from Python or a command-line entry point.
- Test geometry with generated image fixtures.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m algorithm_finding_text input.jpg -o output.jpg
```

## Checks

```bash
python -m pytest
```

## Scope and implementation notes

This is contour-based image processing. It performs document detection and warping, not OCR. Results depend on contrast, document visibility and the scene background.
