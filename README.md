# SAMnotate 

Annotation with Meta's [Segment Anything (SAM)](https://segment-anything.com/)

Quick annotation demo/tool for capstone students in the Panetta Lab at Tufts.  Not really recommended for use outside of this very specific purpose.

## Requirements 

You'll need `python >=3.8`, `pytorch >=1.7` and `torchvision > 0.8`. You'll also need `opencv` and `pycocotools`. 

Install the conda environment directly using environment.yml:
```
$ conda env create --name samnotate --file environment.yml 
```
Download a SAM checkpoint from [here](https://github.com/facebookresearch/segment-anything#model-checkpoints). Install the `default` checkpoint and put it in the checkpoints directory of this repo.

If you choose not to use the conda environment, be sure to install Segment Anything in addition to the requirements above: 

```
$ pip install git+https://github.com/facebookresearch/segment-anything.git
```  

## Annotating  


### Resize and Rotate

First, we need to resize our images to a standard size (640 x 480) and check if they need to be rotated. Life will be a lot easier later if they are in a standard format. 

Run `resize_rotate.py` on your directory of freshly-downloaded images like so: 
```
python3 resize_rotate.py /path/to/your/images /path/to/output
``` 
The two command line arguments are the path to your input folder and a path to an empty directory where you want to store your resized images. Don't just over-write your images!!! 

The script will detect if an image needs to be rotated, and will then rotate and resize as necessary.

### Segment Annotations

To get segments, we need to run Segment Anything on each of our images. Use `segments.py` to infer the segments and iterate over each of them for labelling. This should be run on the images that you've already rotated and resized (above).

```
python3 segments.py /path/to/your/image.jpg 
```

This will run Segment Anything on the image, and then display the image with each segment highlighted. Observe which segment is highlighted, and then press `q` to exit the image preview. Enter a label at the prompt in the terminal. After the label is entered, you'll be shown the next segment. Labelling conventions should be as follows:
- Anything that is not a listed food object in the spreadsheet should be marked `0` 
- The food objects that are in the spreadsheet should be labelled with the item in the `Items` column of the spreadsheet. Please label in all lowercase, using underscores in place of spaces. Ignore any special characters (i.e. &) and accents ("sautéed should just be sauteed").   

As above, press any key to move to the next segment. 

The segments will display in descending order! By default, you will only see 10 masks. If an image has a lot of small items and you don't set a label for every food item, increase the maximum number of masks to display using the `--n_masks` (shortcut `-n`) flag: 

```
python3 segments.py /path/to/your/img.jpg -n 20
```

`n_masks` is set to 10 by default, but change it to whatever you'd like. It should be high enough that you label every food item in the image, but low enough that the amount of tedious clicking is reduced. This may vary by image. 

**Note**: If you have a GPU, use the command line flag `--gpu True` This will speed up inference! 
