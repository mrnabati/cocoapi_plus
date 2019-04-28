# COCO_Plus
An enhanced COCO API for adding images with annotations or creating new COCO-style datasets.
This API adds more functionalities to the original [COCO API](https://github.com/cocodataset/cocoapi).
These functionalities include:

- Creating new COCO-style dataset
- Adding new samples with annotations
- Adding new classes
- Modifying existing annotations
- Adding new annotations to existing samples

The original COCO API must be installed before using the COCO_Plus API.

## Installation
- Install [pycocotools](https://github.com/cocodataset/cocoapi) to your Python site-packages
- Clone this repo and import the coco_plus class
  ```python
  from coco_plus import COCO_PLUS
  ```
