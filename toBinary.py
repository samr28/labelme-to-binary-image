import re
import xml.etree.ElementTree as ET
import json
import sys
import argparse
from os import listdir, makedirs
from os.path import isfile, join, exists
from PIL import Image, ImageDraw

savedir = 'masks'

polygons = []
numFound = 0
filename = ''
imageWidth = 0
imageHeight = 0

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
colors = ['black', 'white', 'red', 'green', 'blue']

bgcolor = white
fgcolor = black

# Create an image with the data in the polygons array
def generateImage(filename, preview, save):
    img = Image.new('RGB', (imageWidth, imageHeight), bgcolor)
    pixels = img.load()
    draw = ImageDraw.Draw(img)
    for polygon in polygons:
        draw.polygon(polygon, fill=fgcolor)
    if preview:
        print('Opening preview')
        img.show()
    if save:
        print('Saving image ' + filename)
        img.save(str(join(savedir, filename)))

# Check if a file is either json or xml
def isValidFile(file):
    if bool(re.search(r'\.json', file)) or bool(re.search(r'\.xml', file)):
        return True
    return False

# Reset vars to default values
# Used when loading a new file
def clearVars():
    global polygons, numFound, filename, imageWidth, imageHeight
    polygons = []
    numFound = 0
    filename = ''
    imageWidth = 0
    imageHeight = 0

def parseFile(file, labels):
    clearVars()
    print('Start parsing ' + file)
    if bool(re.search(r'\.json', file)):
        # JSON file passed in
        parseJSON(file, labels)
    elif bool(re.search(r'\.xml', file)):
        # XML file passed in
        parseXML(file, labels)
    elif bool(re.search(r'\.', file)):
        # Invalid file format passed in
        print('Invalid file specified. Make sure that it is either XML or JSON')
        return False
    return True

def parseJSON(file, labels):
    global polygons, numFound, filename, imageWidth, imageHeight
    with open(file) as f:
        data = json.load(f)
    imageHeight = data['imageHeight']
    imageWidth = data['imageWidth']
    for shape in data['shapes']:
        if shape['label'] in labels:
            numFound += 1
            points = []
            for point in shape['points']:
                x = point[0]
                y = point[1]
                points.append((float(x), float(y)))
            polygons.append(points)
    # Remove ".json"
    filename = re.sub(r'\.json', '', file)
    # Remove folders
    filename = re.sub(r'\w*\/', '', file)

# Parse the xml file and fill in the polygons array
def parseXML(file, labels):
    global polygons, numFound, filename, imageWidth, imageHeight
    tree = ET.parse(file)
    root = tree.getroot()
    for child in root:
        if child.tag == 'object':
            objType = child[0].text
            if objType in labels:
                numFound += 1
                for item in child:
                    if item.tag == 'polygon':
                        points = []
                        for item_under_polygon in item:
                            if item_under_polygon.tag == 'pt':
                                x = item_under_polygon[0].text
                                y = item_under_polygon[1].text
                                points.append((float(x), float(y)))
                        polygons.append(points)
        elif child.tag == 'filename':
            filename = child.text
        elif child.tag == 'imagesize':
            imageHeight = int(child[0].text)
            imageWidth = int(child[1].text)

parser = argparse.ArgumentParser(description='Convert LabelMe XML/JSON files to binary images.')

# Required arguments
parser.add_argument('file', metavar='file/folder', type=str, help='path to input file/folder (json/xml/folder)')
parser.add_argument('output', type=str, help='output file type', 
                    choices=['png', 'jpg'])
parser.add_argument('labels', type=str, nargs='+',
                    help='labels to include in the image')

# Optional flags
parser.add_argument('--savedir', required=False, help='directory to save images in (default: masks)')
parser.add_argument('--nosave', required=False, help='dont save image', 
                    action='store_true')
parser.add_argument('--preview', required=False, help='show image preview', 
                    action='store_true')
parser.add_argument('--bgcolor', required=False, help='background color (default: white)', 
                    choices=colors)
parser.add_argument('--fgcolor', required=False, help='foreground/label color (default: black)', 
                    choices=colors)

args = parser.parse_args()

if args.savedir:
    savedir = args.savedir

if not args.nosave:
    if not exists(savedir):
        makedirs(savedir)

if args.bgcolor:
    bgcolor = args.bgcolor

if args.fgcolor:
    fgcolor = args.fgcolor

# List of files to convert
files = []
if isfile(args.file):
    files.append(args.file)
else:
    # Dir passed in
    print('Start parsing items from directory')
    filesInDir = [f for f in listdir(args.file) if isfile(join(args.file, f))]
    for f in filesInDir:
        files.append(str(join(args.file, f)))
for f in files:
    print
    if not isValidFile(f):
        print('Skipping ' + f)
    else:
        parseFile(f, args.labels)
        if numFound == 0:
            print('Skipping ' + str(f) + ' (found 0 labels)')
        else:
            print('Found ' + str(numFound) + ' of ' + str(args.labels))
            print('Generating binary image')
            filename = re.sub(r'\.\w+', '', filename)
            for label in args.labels:
                filename = filename + '-' + label
            filename = filename + '.' + args.output
            generateImage(filename, args.preview, not args.nosave)
