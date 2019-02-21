import re
import xml.etree.ElementTree as ET
import sys
import argparse
from PIL import Image, ImageDraw

polygons = []
numFound = 0
filename = ''
imageWidth = 0
imageHeight = 0

# Create an image with the data in the polygons array
def generateImage(filename, preview, save):
    img = Image.new('RGB', (imageWidth, imageHeight), "white")
    pixels = img.load()
    draw = ImageDraw.Draw(img)
    for polygon in polygons:
        draw.polygon(polygon, fill=(0, 0, 0))
    if preview:
        print('Opening preview')
        img.show()
    if save:
        print('Saving image ' + filename)
        img.save(str(filename))

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

parser = argparse.ArgumentParser(description='Convert LabelMe XML files to binary images.')

# Required arguments
parser.add_argument('file', type=str, help='path to xml file')
parser.add_argument('output', type=str, help='output file type', 
                    choices=['png', 'jpg'])
parser.add_argument('labels', type=str, nargs='+',
                    help='labels to include in the image')

# Optional flags
parser.add_argument('--nosave', required=False, help='dont save image', 
                    action='store_true')
parser.add_argument('--preview', required=False, help='show image preview', 
                    action='store_true')

args = parser.parse_args()
print('Start parsing xml')
parseXML(args.file, args.labels)
print('Found ' + str(numFound) + ' of ' + str(args.labels))
if (numFound == 0):
    print('Exiting: did not find any of object')
    sys.exit()
print('Generating binary image')
filename = re.sub('\.\w+', '', filename)
for label in args.labels:
    filename = filename + '-' + label
filename = filename + '.' + args.output
generateImage(filename, args.preview, not args.nosave)
