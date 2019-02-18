import re
import xml.etree.ElementTree as ET
import sys
from PIL import Image, ImageDraw

polygons = []
numFound = 0
filename = ''
imageWidth = 0
imageHeight = 0

allowedFlags = ['-nosave', '-preview']

# Make sure that the array of flags is valid
def checkFlags(flags):
    for flag in flags:
        if flag not in allowedFlags:
            return False
    return True

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
        print('Saving image')
        img.save(str(filename))

# Parse the xml file and fill in the polygons array
def parseXML(file, searchObject):
    global polygons, numFound, filename, imageWidth, imageHeight
    tree = ET.parse(file)
    root = tree.getroot()
    for child in root:
        if child.tag == 'object':
            objType = child[0].text
            if objType == searchObject:
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
      
def main():
    numRequiredArgs = 3
    args = sys.argv
    # Make sure that enough args were provided
    if (len(args) < numRequiredArgs):
        print('Usage: python toBinary.py [FILE] [OBJECT_TYPE] [FLAGS]\n')

        print('FILE = filepath')
        print('OBJECT_TYPE = line, robot, barrel')

        print('\nFLAGS:')
        print(' -nosave      dont save image')
        print(' -preview     show image preview')
        return

    save = True
    preview = False

    # Check for flags
    if len(args) > numRequiredArgs:
        # Parse rest as flags
        flags = args[numRequiredArgs:]
        if not checkFlags(flags):
            print('Invalid flag provided!')
            return
        if '-nosave' in flags:
            save = False
        if '-preview' in flags:
            preview = True

    print('Start parsing xml')
    parseXML(args[1], args[2])
    print('Loaded image: ' + filename + ' (' + str(imageWidth) + 'x' + str(imageHeight) + ')')
    print('Found ' + str(numFound) + ' of object "' + args[2] + '"')
    print('Generating binary image')
    generateImage(filename, preview, save)      
      
if __name__ == "__main__":
    main() 