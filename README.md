# Labelme to Binary Image

This tool allows you to convert images from the [web version of labelme](http://labelme.csail.mit.edu/) into binary images.

## Usage

```bash
python toBinary.py [FILE] [OBJECT_TYPE] [OUTPUT_FILE_TYPE] [FLAGS]

FILE = filepath
OBJECT_TYPE = label to capture ex: line, robot, barrel
OUTPUT_FILE_TYPE = jpg, png

FLAGS:
 -nosave      dont save image
 -preview     show image preview
```

`OBJECT_TYPE` should match the label of the polygon that you are looking for

## Screenshots
Original Image from LabelMe:

![Original Image](Example/example.jpg)

`python toBinary.py Example/example.xml line jpg`:
![Original Image](Example/example-line.jpg)

`python toBinary.py Example/example.xml barrel jpg`:
![Original Image](Example/example-barrel.jpg)

## Future goals
- Higher level script to automate large jobs
