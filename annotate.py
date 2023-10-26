import os
import argparse  
from glob import glob 

import numpy as np
import cv2  

from rectangle import annotation_window
from segments import get_segments


def annotate(input_images):
    """
    Main annotation driver
    """
    
    for image_path in input_images:  

        img = cv2.imread(image_path) 
        img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_CUBIC)

        bbox = annotation_window(img) 

        get_segments(img, np.array(bbox))    


if __name__ == "__main__": 

    parser = argparse.ArgumentParser()  
    parser.add_argument("input_dir", help="Path to directory")
    args = parser.parse_args() 

    if not os.path.exists(args.input_dir):
        print("Invalid input directory") 
    
    else: 
        input_images = glob(f"{args.input_dir}/*")  

    annotate(input_images[:10])


    
