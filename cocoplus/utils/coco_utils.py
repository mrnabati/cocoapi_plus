import numpy as np
import copy
import cv2
from shapely.geometry import LineString
from matplotlib.patches import BoxStyle


def xywh_to_xyxy(xywh):
    """
    Convert [x1 y1 w h] box format to [x1 y1 x2 y2] format.
    """
    
    if isinstance(xywh, (list, tuple)):
        # Single box given as a list of coordinates
        assert len(xywh) == 4
        x1, y1 = xywh[0], xywh[1]
        x2 = x1 + np.maximum(0., xywh[2] - 1.)
        y2 = y1 + np.maximum(0., xywh[3] - 1.)
        return (x1, y1, x2, y2)
    elif isinstance(xywh, np.ndarray):
        # Multiple boxes given as a 2D ndarray
        return np.hstack(
            (xywh[:, 0:2], xywh[:, 0:2] + np.maximum(0, xywh[:, 2:4] - 1))
        )
    else:
        raise TypeError('Argument xywh must be a list, tuple, or numpy array.')

##------------------------------------------------------------------------------
def xyxy_to_xywh(xyxy):
    """
    Convert [x1 y1 x2 y2] box format to [x1 y1 w h] format.
    """
    
    if isinstance(xyxy, (list, tuple)):
        # Single box given as a list of coordinates
        assert len(xyxy) == 4
        x1, y1 = xyxy[0], xyxy[1]
        w = xyxy[2] - x1 + 1
        h = xyxy[3] - y1 + 1
        return (x1, y1, w, h)
    elif isinstance(xyxy, np.ndarray):
        # Multiple boxes given as a 2D ndarray
        return np.hstack((xyxy[:, 0:2], xyxy[:, 2:4] - xyxy[:, 0:2] + 1))
    else:
        raise TypeError('Argument xyxy must be a list, tuple, or numpy array.')

##------------------------------------------------------------------------------
def clip_boxes_to_image(boxes, height, width):
    """
    Clip an array of boxes to an image with the given height and width.
    """

    boxes[:, [0, 2]] = np.minimum(width - 1., np.maximum(0., boxes[:, [0, 2]]))
    boxes[:, [1, 3]] = np.minimum(height - 1., np.maximum(0., boxes[:, [1, 3]]))
    return boxes

## -----------------------------------------------------------------------------
def show_class_name(img, pos, class_str, font_scale=0.35):
    """
    Visualizes the class names using cv2
    """

    img = img.astype(np.uint8)
    x0, y0 = int(pos[0]), int(pos[1])
    
    # Compute text size.
    txt = class_str
    font = cv2.FONT_HERSHEY_SIMPLEX
    ((txt_w, txt_h), _) = cv2.getTextSize(txt, font, font_scale, 1)
    
    # Place text background.
    back_tl = x0, y0 - int(1.3 * txt_h)
    back_br = x0 + txt_w, y0
    cv2.rectangle(img, back_tl, back_br, _GREEN, -1)
    
    # Show text.
    txt_tl = x0, y0 - int(0.3 * txt_h)
    cv2.putText(img, txt, txt_tl, font, font_scale, _GRAY, lineType=cv2.LINE_AA)
    return img

## -----------------------------------------------------------------------------
def show_class_name_plt(pos, class_str, ax, bg_color='red', font_size=8):
    """
    Visualizes the class names using matplotlib on a given ax
    """

    x0, y0 = int(pos[0]), int(pos[1])
    # y_lim = ax.get_ylim()[0]
    # x_lim = ax.get_xlim()[1]

    boxstyle = BoxStyle("Round")
    props = {'boxstyle': boxstyle,
            'facecolor': bg_color,
            'alpha': 0.5}
    t = ax.text(abs(x0+2), abs(y0-8), class_str, fontsize=font_size, bbox=props)
    x_t = abs(x0+2)
    y_t = abs(y0-8)

    # r = ax.get_figure().canvas.get_renderer()
    # bb = t.get_window_extent(renderer=r)
    # x_t = min(abs(x0+2), x_lim-bb.width)
    # y_t = min(abs(y0-8), y_lim-bb.height)

    t = ax.text(x_t, y_t, class_str, fontsize=font_size, 
            bbox=dict(facecolor=bg_color, boxstyle='round',  alpha=0.5))


##------------------------------------------------------------------------------
def draw_xywh_bbox(img, bboxes, color=(0,255,0), lineWidth=3, format='BGR', 
                   names=None):

    assert format in ['RGB', 'BGR'], "Format must be either 'BGR' or 'RGB'."
    if names is not None:
        assert len(bboxes) == len(names), "Bboxes and names must have the same length"
        
    if format == 'RGB':
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    for idx, box in enumerate(bboxes):
        box = [int(elem) for elem in box]
        cv2.rectangle(img,(box[0],box[1]), (box[0]+box[2], box[1]+box[3]),
                      color,lineWidth)
        if names is not None:
            show_class_name(img, box[:2], names[idx])

    if format == 'RGB':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img

## -----------------------------------------------------------------------------
def draw_xyxy_bbox(img, bboxes, color=(0,255,0), lineWidth=3, format='BGR', 
                   names=None):

    assert format in ['RGB', 'BGR'], "Format must be either 'BGR' or 'RGB'."
    if names is not None:
        assert len(bboxes) == len(names), "Bboxes and names must have the same length"

    if format == 'RGB':
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    for idx, box in enumerate(bboxes):
        box = [int(elem) for elem in box]
        cv2.rectangle(img, (box[0],box[1]), (box[2],box[3]), color, lineWidth)
        if names is not None:
            img = show_class_name(img, box[:2], names[idx])
    
    if format == 'RGB':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img

## -----------------------------------------------------------------------------
def draw_points(img, points, color=(0,255,0), radius=3, thickness=-1, format='BGR'):

    assert format in ['RGB', 'BGR'], "Format must be either 'BGR' or 'RGB'."
    if format == 'RGB':
        # Change format to BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    for point in points:
        point = [int(elem) for elem in point]
        cv2.circle(img,(point[0], point[1]), radius, color, thickness)

    if format == 'RGB':
        # Change back to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img

##------------------------------------------------------------------------------
COCO_CATEGORIES = [{'supercategory': 'person', 'id': 1, 'name': 'person'}, 
                  {'supercategory': 'vehicle', 'id': 2, 'name': 'bicycle'}, 
                  {'supercategory': 'vehicle', 'id': 3, 'name': 'car'}, 
                  {'supercategory': 'vehicle', 'id': 4, 'name': 'motorcycle'}, 
                  {'supercategory': 'vehicle', 'id': 5, 'name': 'airplane'}, 
                  {'supercategory': 'vehicle', 'id': 6, 'name': 'bus'}, 
                  {'supercategory': 'vehicle', 'id': 7, 'name': 'train'}, 
                  {'supercategory': 'vehicle', 'id': 8, 'name': 'truck'}, 
                  {'supercategory': 'vehicle', 'id': 9, 'name': 'boat'}, 
                  {'supercategory': 'outdoor', 'id': 10, 'name': 'traffic light'}, 
                  {'supercategory': 'outdoor', 'id': 11, 'name': 'fire hydrant'}, 
                  {'supercategory': 'outdoor', 'id': 13, 'name': 'stop sign'}, 
                  {'supercategory': 'outdoor', 'id': 14, 'name': 'parking meter'}, 
                  {'supercategory': 'outdoor', 'id': 15, 'name': 'bench'}, 
                  {'supercategory': 'animal', 'id': 16, 'name': 'bird'}, 
                  {'supercategory': 'animal', 'id': 17, 'name': 'cat'}, 
                  {'supercategory': 'animal', 'id': 18, 'name': 'dog'}, 
                  {'supercategory': 'animal', 'id': 19, 'name': 'horse'}, 
                  {'supercategory': 'animal', 'id': 20, 'name': 'sheep'}, 
                  {'supercategory': 'animal', 'id': 21, 'name': 'cow'}, 
                  {'supercategory': 'animal', 'id': 22, 'name': 'elephant'}, 
                  {'supercategory': 'animal', 'id': 23, 'name': 'bear'}, 
                  {'supercategory': 'animal', 'id': 24, 'name': 'zebra'}, 
                  {'supercategory': 'animal', 'id': 25, 'name': 'giraffe'}, 
                  {'supercategory': 'accessory', 'id': 27, 'name': 'backpack'}, 
                  {'supercategory': 'accessory', 'id': 28, 'name': 'umbrella'}, 
                  {'supercategory': 'accessory', 'id': 31, 'name': 'handbag'}, 
                  {'supercategory': 'accessory', 'id': 32, 'name': 'tie'}, 
                  {'supercategory': 'accessory', 'id': 33, 'name': 'suitcase'}, 
                  {'supercategory': 'sports', 'id': 34, 'name': 'frisbee'}, 
                  {'supercategory': 'sports', 'id': 35, 'name': 'skis'}, 
                  {'supercategory': 'sports', 'id': 36, 'name': 'snowboard'}, 
                  {'supercategory': 'sports', 'id': 37, 'name': 'sports ball'}, 
                  {'supercategory': 'sports', 'id': 38, 'name': 'kite'}, 
                  {'supercategory': 'sports', 'id': 39, 'name': 'baseball bat'}, 
                  {'supercategory': 'sports', 'id': 40, 'name': 'baseball glove'}, 
                  {'supercategory': 'sports', 'id': 41, 'name': 'skateboard'}, 
                  {'supercategory': 'sports', 'id': 42, 'name': 'surfboard'}, 
                  {'supercategory': 'sports', 'id': 43, 'name': 'tennis racket'}, 
                  {'supercategory': 'kitchen', 'id': 44, 'name': 'bottle'}, 
                  {'supercategory': 'kitchen', 'id': 46, 'name': 'wine glass'}, 
                  {'supercategory': 'kitchen', 'id': 47, 'name': 'cup'}, 
                  {'supercategory': 'kitchen', 'id': 48, 'name': 'fork'}, 
                  {'supercategory': 'kitchen', 'id': 49, 'name': 'knife'}, 
                  {'supercategory': 'kitchen', 'id': 50, 'name': 'spoon'}, 
                  {'supercategory': 'kitchen', 'id': 51, 'name': 'bowl'}, 
                  {'supercategory': 'food', 'id': 52, 'name': 'banana'}, 
                  {'supercategory': 'food', 'id': 53, 'name': 'apple'}, 
                  {'supercategory': 'food', 'id': 54, 'name': 'sandwich'}, 
                  {'supercategory': 'food', 'id': 55, 'name': 'orange'}, 
                  {'supercategory': 'food', 'id': 56, 'name': 'broccoli'}, 
                  {'supercategory': 'food', 'id': 57, 'name': 'carrot'}, 
                  {'supercategory': 'food', 'id': 58, 'name': 'hot dog'}, 
                  {'supercategory': 'food', 'id': 59, 'name': 'pizza'}, 
                  {'supercategory': 'food', 'id': 60, 'name': 'donut'}, 
                  {'supercategory': 'food', 'id': 61, 'name': 'cake'}, 
                  {'supercategory': 'furniture', 'id': 62, 'name': 'chair'}, 
                  {'supercategory': 'furniture', 'id': 63, 'name': 'couch'}, 
                  {'supercategory': 'furniture', 'id': 64, 'name': 'potted plant'}, 
                  {'supercategory': 'furniture', 'id': 65, 'name': 'bed'}, 
                  {'supercategory': 'furniture', 'id': 67, 'name': 'dining table'}, 
                  {'supercategory': 'furniture', 'id': 70, 'name': 'toilet'}, 
                  {'supercategory': 'electronic', 'id': 72, 'name': 'tv'}, 
                  {'supercategory': 'electronic', 'id': 73, 'name': 'laptop'}, 
                  {'supercategory': 'electronic', 'id': 74, 'name': 'mouse'}, 
                  {'supercategory': 'electronic', 'id': 75, 'name': 'remote'}, 
                  {'supercategory': 'electronic', 'id': 76, 'name': 'keyboard'}, 
                  {'supercategory': 'electronic', 'id': 77, 'name': 'cell phone'}, 
                  {'supercategory': 'appliance', 'id': 78, 'name': 'microwave'}, 
                  {'supercategory': 'appliance', 'id': 79, 'name': 'oven'}, 
                  {'supercategory': 'appliance', 'id': 80, 'name': 'toaster'}, 
                  {'supercategory': 'appliance', 'id': 81, 'name': 'sink'}, 
                  {'supercategory': 'appliance', 'id': 82, 'name': 'refrigerator'},
                  {'supercategory': 'indoor', 'id': 84, 'name': 'book'}, 
                  {'supercategory': 'indoor', 'id': 85, 'name': 'clock'}, 
                  {'supercategory': 'indoor', 'id': 86, 'name': 'vase'}, 
                  {'supercategory': 'indoor', 'id': 87, 'name': 'scissors'}, 
                  {'supercategory': 'indoor', 'id': 88, 'name': 'teddy bear'}, 
                  {'supercategory': 'indoor', 'id': 89, 'name': 'hair drier'}, 
                  {'supercategory': 'indoor', 'id': 90, 'name': 'toothbrush'}]