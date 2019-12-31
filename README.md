# COCO_Plus
An enhanced COCO API for adding images with annotations or creating new COCO-style datasets.
This API adds more functionalities to the original [COCO API](https://github.com/cocodataset/cocoapi).
These functionalities include:

- Creating new COCO-style dataset
- Adding new samples with annotations
- Adding new classes
- Modifying existing annotations
- Adding new annotations to existing samples

## Installation

### Requirements
- Linux or macOS
- Python>= 3.6
- pycocotools: `pip install cython pycocotools`

### Build COCO_Plus
After having the above dependencies, run:
```bash
git clone https://github.com/mrnabati/cocoapi_plus.git
cd cocoapi_plus
pip install -e .
```