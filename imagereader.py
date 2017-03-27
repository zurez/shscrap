from PIL import Image

def image(filepath,angle=0):

	image=Image.open(filepath)
	if angle != 0:
		image=image.rotate(angle)
	return image

