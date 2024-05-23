import os
import argparse
from glob import glob

import cv2


def resize_rotate(input_images, output_dir):
    """
    Resize all images to 640 x 480 and rotate if necessary
    """

    for image_path in input_images:

        imname = os.path.basename(image_path)

        img = cv2.imread(image_path)

        h, w, _ = img.shape

        if h > w:
            # rotate to landscape
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)


        # resize to 640 x 480
        resized = cv2.resize(img, (640, 480), interpolation=cv2.INTER_CUBIC)

        # write resized image
        cv2.imwrite(os.path.join(output_dir, imname), resized)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help="Path to directory")
    parser.add_argument("output_dir", help="Destination directory")
    args = parser.parse_args()

    if not os.path.exists(args.input_dir):
        print("Invalid input directory")
    if not os.path.exists(args.output_dir):
        print("Invalid output directory")
    else:
        input_images = glob(f"{args.input_dir}/*")
        input_images.sort()

        # check all images for resizing and rotation
        resize_rotate(input_images, args.output_dir)

