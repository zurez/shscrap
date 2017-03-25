from xvfbwrapper import Xvfb
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
vdisplay = Xvfb()
vdisplay.start()

# launch stuff inside virtual display here
print "Init"
driver = webdriver.Chrome(executable_path="cd/chromedriver")
print "Starting driver"
driver.get('http://ipindiaonline.gov.in/tmrpublicsearch/frmmain.aspx')
print "Request done"
vdisplay.stop()
