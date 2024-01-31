# PiSegment
A light weight python software for semi-supervised segmentation on images. It can be used for image segmentation, background extraction, semantic segmentation,colorization etc. The code being written in pure python can be easly integrated with Flask of Django
backend for a web app.

# Video

# Results

| Image     | Mask |
| ----------- | ----------- |
|<img src="./data/lincoln.png" alt="org_img" width="320" height="390">   | <img src="./data/mask.png" alt="mask" width="320" height="390">    |


# Installation
```
pip install pisegment
```

# Usage
- Command line
```
pisegment --input "path/to/image/tobe/segmented" --mask "path/to/the/generated/annotation"

# pisegment --input "path..." --mask "path..." --ps 3 --k 4 --k_ 10 --sig 1.00e-2 --no_filter
```

# Tips on using

# How it works

# Param description
