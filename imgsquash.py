import sys
from PIL import Image

# TODO test for images

batchlen = 100 # max by PIL about 1000 but excessive swapping occurs earlier (ca. 200 on a 4gb ram machine)
resize_width = 10 

print "reading args..."
image_names = []
for i, a in enumerate(sys.argv):
    if i!=0:
        image_names.append(a)

tmpimg = Image.open(image_names[0])   
height = tmpimg.size[1]
out = Image.new("RGB", (len(image_names)*resize_width, height))

batchcount = len(image_names)/batchlen
print "squashing %d images into one" % len(image_names)
prompt = raw_input("continue? (y/n): ").lower()

if prompt != "y":
    sys.exit("aborted by user")

for index in range(0, len(image_names), batchlen):
    print "opening files... (batch %d of %d) " % ((index/batchlen), batchcount),
    images = []
    if index+batchlen < len(image_names):
        end = index+batchlen
    else:
        end = len(image_names)
        
    for i in range(index, end):
        images.append(Image.open(image_names[i]))

    print "resizing images... ",
    lines = []
    for i in images:
        lines.append(i.resize((resize_width, height), Image.ANTIALIAS))

    print "concatenating... "
    for i, l in enumerate(lines):
        out.paste(l, (((index+i)*resize_width), 0))

print "saving out.png..."
out.save("out.png")
