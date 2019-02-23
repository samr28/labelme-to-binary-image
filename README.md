# Labelme to Binary Image

This tool allows you to convert images from the [web](http://labelme.csail.mit.edu/) or [desktop](https://github.com/wkentaro/labelme) versions of labelme into binary images.

## Usage

```bash
python toBinary.py [-h] [--nosave] [--preview] file {png,jpg} labels [labels ...]

FILE = path to xml/json input file
OUTPUT_FILE_TYPE = jpg, png
LABELS = space seperated list of label to capture ex: "line robot barrel"

FLAGS:
 --nosave      dont save image
 --preview     show image preview
```

## Screenshots
Original Image from LabelMe:

![Original Image](Example/example.jpg)

`python toBinary.py Example/example.xml jpg line`:
![Original Image](Example/example-line.jpg)

`python toBinary.py Example/example.xml jpg barrel`:
![Original Image](Example/example-barrel.jpg)

## Future goals
- Higher level script to automate large jobs
