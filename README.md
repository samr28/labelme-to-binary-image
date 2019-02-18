# Labelme to Binary Image

This tool allows you to convert images from the [web version of labelme](http://labelme.csail.mit.edu/) into binary images.

## Usage

```bash
python toBinary.py [FILE] [OBJECT_TYPE] [FLAGS]

FILE = filepath
OBJECT_TYPE = line, robot, barrel

FLAGS:
 -nosave      dont save image
 -preview     show image preview
```

`OBJECT_TYPE` should match the label of the polygon that you are looking for

## Future goals
- Higher level script to automate large jobs
