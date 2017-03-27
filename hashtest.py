from hasher import dhash
from db import *
from imagereader import image
# from PIL import Image
from util import readFolder
folder="/var/www/FinalPixvera/static/images"
rotator=[90,180,270,360]
files=readFolder(folder)
for i in files:
	img=image(folder+"/"+i)
	hashd=dhash(img)
	ret=select(hashd)
	if len(ret) != 0: 
		# print "Duplicate"
		pass
	else:
		print "Original"
	# print i
