
import numpy as np
import copy
import cv2
from shapely.geometry import LineString


def xywh_to_xyxy(xywh):
    """Convert [x1 y1 w h] box format to [x1 y1 x2 y2] format."""
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
    """Convert [x1 y1 x2 y2] box format to [x1 y1 w h] format."""
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
    """Clip an array of boxes to an image with the given height and width."""
    boxes[:, [0, 2]] = np.minimum(width - 1., np.maximum(0., boxes[:, [0, 2]]))
    boxes[:, [1, 3]] = np.minimum(height - 1., np.maximum(0., boxes[:, [1, 3]]))
    return boxes

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
            vis_class(img, box[:2], names[idx])

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
            img = vis_class(img, box[:2], names[idx])
    
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
