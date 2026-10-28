# Document Detector

[![CI](https://github.com/Raphailinc/Document-Detector/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphailinc/Document-Detector/actions/workflows/ci.yml)

[English](README.md) · [Русский](README.ru.md)

Проект компьютерного зрения: поиск четырёхугольного контура документа и перспективное преобразование к виду сверху.

## Возможности

- Поиск крупного контура с четырьмя углами через OpenCV.
- Упорядочивание углов перед преобразованием.
- Использование одинаковых функций из Python и CLI.
- Проверка геометрии на синтетических изображениях.

## Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m algorithm_finding_text input.jpg -o output.jpg
```

## Проверки

```bash
python -m pytest
```

## Условия запуска и границы проекта

Здесь выполняются поиск документа и коррекция перспективы. Распознавания текста (OCR) нет. Результат зависит от контраста, видимости границ и фона.
