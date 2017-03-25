from xvfbwrapper import Xvfb

vdisplay = Xvfb()
vdisplay.start()

# launch stuff inside virtual display here
print "Init"
vdisplay.stop()
