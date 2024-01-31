# PiSegment
A lightweight Python software for semi-supervised segmentation on images, it can be utilized for tasks such as image segmentation, background extraction, semantic segmentation, colorization, etc. The code, written in pure Python, can be easily integrated with Flask or Django backend for a web app.
# Video


# Results

| Image w annotation    | Segmentation |
| ----------- | ----------- |
|<img src="./imgs/combined_tan.png" alt="org_img" width="250" height="150">   | <img src="./imgs/seg_image_tan.png" alt="segmented" width="250" height="150">    |
|<img src="./imgs/combined_tap.png" alt="org_img" width="250" height="150">   | <img src="./imgs/seg_image_tap.png" alt="segmented" width="250" height="150">    |

| Segment 1   | Segment 2 |
| ----------- | ----------- |
|<img src="./imgs/seg_4_tap.png" alt="org_img" width="250" height="150">   | <img src="./imgs/seg_3_tap.png" alt="segmented" width="250" height="150">    |


# Installation
```
pip install pisegment
```

# Usage
- Command line
```
pisegment --input "path/to/image/tobe/segmented" --mask "path/to/the/generated/annotation"
```

# Tips on using
- By default the denoising filter is on. If your image doesn't have noise, turn if off using `--no_filter` option. You may also use this option if you are already using some different software for denoising. 
```bash
pisegment --input "path/.." --mask "path/.." --no_filter
```
- For fast processing, consider downsizing your image under 256 X 256 to generate the segmented mask, then upscale the segmeted mask to the original size.
- For very complex images, like the 2nd example in the **Results**, the parameter `--sig` plays a crucial role. See the **Jupyter_demo** for the workflow to segment such kind of images.

# How it works

# Param description
