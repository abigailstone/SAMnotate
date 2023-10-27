import os
import argparse
from glob import glob
import json

import numpy as np
import matplotlib.pyplot as plt
import torch
import cv2

from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

def show_mask(mask, ax):
    """
    show mask on image 
    https://github.com/facebookresearch/segment-anything/blob/main/notebooks/predictor_example.ipynb
    """
    color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)

def show_image(image, mask):
    """
    display an image and its mask
    """
    plt.figure()
    plt.imshow(image)
    show_mask(mask, plt.gca())
    plt.axis('off')
    plt.show()


def annotate(image):
    """
    Run SegmentAnything annotation and save the masks
    """

    sam_checkpoint = os.path.join("checkpoints", "sam_vit_h_4b8939.pth")
    model_type = "vit_h"
    # device = "cuda"

    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    # sam.to(device=device)

    mask_generator = SamAutomaticMaskGenerator(
        model=sam,
        points_per_side=16,
        # pred_iou_thresh=0.86,
        # stability_score_thresh=0.92,
        # crop_n_layers=1,
        # crop_n_points_downscale_factor=2,
        min_mask_region_area=100
    )

    masks = mask_generator.generate(image)

    labelled_masks = []

    for mask in masks:

        show_image(image, mask['segmentation'])
        label = input("Label: ")

        # label the mask
        labelled = mask
        labelled['name'] = label

        # convert from numpy array to list
        labelled['segmentation'] = labelled['segmentation'].tolist()

        # add to list of masks for this image
        labelled_masks.append(labelled)

    return labelled_masks



def read_image(image_path):
    """
    Read a single input image, run segmentation inference, and 
    dump segments into a .json
    """

    img = cv2.imread(image_path) 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # color conversion for matplotlib

    labels = annotate(img)

    json_path = image_path.split('.')[0] + '.json' 

    with open(json_path, "w") as f:
        json.dump(labels, f, indent=4)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("input_img", help="Path to image")
    args = parser.parse_args()

    if not os.path.exists(args.input_img):
        print("Invalid input image path")
    else:
        read_image(args.input_img)