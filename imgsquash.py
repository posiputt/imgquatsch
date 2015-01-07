import sys
from PIL import Image

# TODO test for images

print "opening files..."
images = []
for i, a in enumerate(sys.argv):
    if i != 0:
    	images.append(Image.open(a))

print "resizing images..."
height = images[0].size[1]
lines = []
for i in images:
    lines.append(i.resize((1, height)))

print "concatenating..."
out = Image.new("RGB", (len(lines), height))
for i, l in enumerate(lines):
    out.paste(l, (i, 0))

print "saving out.png..."
out.save("out.png")
