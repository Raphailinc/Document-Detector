# Document Detector & Warper

Поиск листа/документа на фото и его «распрямление» в топ-даун проекцию с помощью OpenCV.

## Что умеет
- Находит самый крупный четырёхугольный контур (документ) на изображении.
- Упорядочивает углы (TL, TR, BR, BL) и делает перспективное преобразование.
- CLI: `python -m algorithm_finding_text input.jpg -o output.jpg`.

## Быстрый старт
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m algorithm_finding_text path/to/photo.jpg -o warped.jpg
```

## API
- `detect_document(image, min_area_ratio=0.2) -> (corners, contour)`
- `warp_document(image, corners, output_size=None) -> warped_image`
- `order_corners(points) -> ordered_points`

## Тесты
```bash
pytest
```

## Заметки
- Используется `opencv-python-headless` (без GUI), поэтому показ изображений не требуется — только чтение/запись файлов.
