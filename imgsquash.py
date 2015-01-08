# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import time
from PIL import Image

# TODO test for images

batchlen = 10 # max by PIL about 1000 but excessive swapping occurs earlier (ca. 200 on a 4gb ram machine)
resize_width = 1

print "\t"+"reading args..."
image_names = []
for i, a in enumerate(sys.argv):
    if i!=0:
        image_names.append(a)

tmpimg = Image.open(image_names[0])   
height = tmpimg.size[1]
out = Image.new("RGB", (len(image_names)*resize_width, height))

batchcount = len(image_names)/batchlen
print "\t"+"squashing %d images into one" % len(image_names)
prompt = raw_input("\tcontinue? (y/n): ").lower()

if prompt != "y":
    sys.exit("aborted by user")
    
starttime = time.time()

for index in range(0, len(image_names), batchlen):
    # open files
    sys.stdout.write("\r\t"+"batch %d of %d" % ((index/batchlen)+1, batchcount+1))
    images = []
    if index+batchlen < len(image_names):
        end = index+batchlen
    else:
        end = len(image_names)
        
    for i in range(index, end):
        images.append(Image.open(image_names[i]))

    # resize images
    lines = []
    for i in images:
        lines.append(i.resize((resize_width, height), Image.ANTIALIAS))

    # concatenate
    for i, l in enumerate(lines):
        out.paste(l, (((index+i)*resize_width), 0))
        
    now = time.time()
    runtime = now-starttime
    etl = batchcount * runtime / ((index/batchlen)+1)
    sys.stdout.write(" / "+"%02d:%02d / %02d:%02d" % (runtime/60, runtime%60, etl/60, etl%60))
    sys.stdout.flush()

print "\n"+"saving out.png..."
out.save("out.png")
