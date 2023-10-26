# SAMnotate 

 
Annotation with Meta's Segment Anything (SAM) 


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