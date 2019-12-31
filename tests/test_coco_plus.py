import os
import cv2

from _context import cocoplus


def test_empty_dataset():
    empty_dataset = cocoplus.coco.COCO_PLUS()
    

def main():
    ann_file = '../../../data/datasets/nucoco/v1.0-mini/annotations/instances_val.json'
    ann_file = os.path.abspath(ann_file)
    print("Output annotation file: " , ann_file)
    
    dataset = cocoplus.coco.COCO_PLUS(ann_file)
    for key,val in dataset.imgs.items():
        img_filename = '../../../data/datasets/nucoco/v1.0-mini/val/' + val['file_name']
        img = cv2.imread(img_filename)
        anns = dataset.imgToAnns[val['id']]
        for ann in anns:
            print("Category ID: ", ann['category_id'])

        dataset.showImgAnn(img, anns,bbox_only=True)
        # input('here')

##------------------------------------------------------------------------------
if __name__ == "__main__":
    main()