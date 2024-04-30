import os
import json
from glob import glob

import numpy as np
import cv2


def merge_masks(masks):

    # grab all the labels
    labels = [d['name'] for d in masks]

    # create empty dict for cleaned up masks
    merged_masks = {}

    print(f"Labels: {np.unique(labels)}")

    for l in np.unique(labels):

        # don't keep 0 masks
        if l != '0':

            new_mask = np.zeros((480, 640))

            for m in masks:
                if m['name'] == l:

                    # get current segmentation
                    seg = np.array(m['segmentation'], np.float64)

                    # merge masks
                    new_mask = cv2.bitwise_or(new_mask, seg)

            merged_masks[l] = new_mask.tolist()

    return merged_masks




def main(src_dir, dst_dir, file_ext):

    image_list = glob(os.path.join(src_dir, f"*{file_ext}"))

    for im_path in image_list:

        # color conversion
        image = cv2.imread(im_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # grab the json that corresponds to the current image
        json_path = im_path.replace(file_ext, '.json')
        assert(os.path.exists(json_path))

        # read your masks into a list of dictionaries
        with open(json_path) as f:
            masks = json.load(f)

        # clean up and merge masks
        final_masks = merge_masks(masks)

        # write file out
        dst_path = os.path.join(dst_dir, json_path.split('/')[-1])
        with open(dst_path, "w") as f:
            json.dump(final_masks, f, indent=4)



if __name__ == "__main__":

    # your file paths here!
    SRC_PATH = '/home/abigail/Data/Nutrition_Phase3/annotated/'
    DST_PATH = '/home/abigail/Data/Nutrition_Phase3/masks/'

    assert(os.path.exists(SRC_PATH))

    if not os.path.exists(DST_PATH):
        os.makedirs(DST_PATH)

    main(SRC_PATH, DST_PATH, '.jpg')
