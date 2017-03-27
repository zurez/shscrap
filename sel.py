import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from xvfbwrapper import Xvfb
from hasher import dhash
from db import *
from imagereader import image
# from PIL import Image
from util import readFolder
import shutil
rotator=[0,90,180,270,360]
tempDirectory="temp/images"
finalDir="/var/www/FinalPixvera/static/images"
vdisplay = Xvfb()
vdisplay.start()
# To install selenium: pip install selenium

####
# Todo
#	1) net connection lost check (probaly in error with opening home page)
#	2) delete the saved files
#	3) delete the rows
#	4) save in a dict what all combinations of identifiers have been done
#	5) [DONE] remove time.sleep(time_sleep) with explicit check of whether the content fetched is changed with the data on the left. (match with application number)
####

####
# 1)
#	-> from twisted.internet.error import ConnectionLost
#	-> 
#	#!/usr/bin/env python3
#	import httplib2;
#	import signal;
#	import os;
#	import time;
#
#	def handle_server_error (x, y):
#		print ("Now saving all progress");
#		#HERE COMES THE CODE FOR SAVING ALL YOUR PROGRESS
#		#AFTER THE CODE, YOU CAN WRITE os._exit (0) to either quit or time.sleep (10) to pause the program for 10 seconds before continuing execution
#
#	if (__name__ == '__main__'):
#	signal.signal (signal.SIGINT, handle_server_error);
#	http = httplib2.Http ();
#	try:
#		head, content = http.request ('http://example.com');
#		print 'ok'
#	except httplib2.ServerNotFoundError as snf:
#		print ("It seems your internet connection is down. Saving progress and pausing script.");
#		handle_server_error ();
####
# add phantom js

def get_info(identifier, time_sleep=2):
	""" Main function called to get text and image photo_url
	    Identifier is the class name of rows in the page (found by inspect elements); for our case: 'row','alt'
	    time_sleep is the time delay between two calls (two wordmarks), in seconds, default:2, increase if IP Banned or slow net(if same row repeats itself)
		returns list, append it to main list for a particular page
	"""
	print '\t', identifier
	len_script = "return document.getElementsByClassName('"+identifier+"').length"
	iterator_count = driver.execute_script(len_script)
	dict_list = []
	for i in range(iterator_count):
		click_script = "document.getElementsByClassName('"+identifier+"')["+str(i)+"].getElementsByTagName('a')[0].click()"
		driver.execute_script(click_script)
		wait1 = WebDriverWait(driver, 10)
		wait1.until(EC.visibility_of_element_located((By.ID, "ContentPlaceHolder1_LblDetails")))
		application_left_script = "return document.getElementsByClassName('"+identifier+"')["+str(i)+"].getElementsByTagName('span')[6].innerText"
		application_left = driver.execute_script(application_left_script)
		found_it = False
		times = 0
		print '\t\tfetching application data'
		while(not found_it):
			time.sleep(time_sleep)
			times+=1
			application_right_script = "return document.getElementById('ContentPlaceHolder1_PnlDetails').getElementsByTagName('td')[3].innerText"
			application_right = driver.execute_script(application_right_script).split()[0]
			found_it = application_right==application_left
			print '\t\t\tfetch attempt{0}: left=>{1} right=>{2} {3}'.format(times, application_left,application_right,found_it)
		content_script = "return document.getElementById('ContentPlaceHolder1_PnlDetails').getElementsByTagName('td')"
		table_cells = [table_cell.text.encode('ascii','ignore') for table_cell in driver.execute_script(content_script)]
		table_cells_iterator = iter(table_cells)
		tmp_data = {table_cell:next(table_cells_iterator) for table_cell in table_cells_iterator}
		print '\t\t', "[{0} of {1}]".format(i,iterator_count-1), tmp_data['Word Mark']
		try:
			photo_script = "return document.getElementsByClassName('"+identifier+"')["+str(i)+"].getElementsByTagName('img')[0].src"
			tmp_photo = driver.execute_script(photo_script)
		except:
			tmp_photo = ""
		dict_list.append({'text':tmp_data, 'photo':tmp_photo.encode('ascii','ignore'), 'phrase':tell_phrase, 'class':tell_class})
	return dict_list

# Code to generate the triagram sequence: Run it in python cmd line so as to generate ['AAA','AAB',...]
# c = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
# [x+y+z for x in c for y in c for z in c]
tell_phrases = ['AAA','AAB']
len1 = len(tell_phrases)-1
tell_classes = range(1,46)
len2 = len(tell_classes)-1

complete_data = []
driver = webdriver.Chrome(executable_path="cd/chromedriver")
#Change path (download url: http://chromedriver.storage.googleapis.com/2.16/chromedriver_linux64.zip, unzip and specfy path here)

for idx1,tell_phrase in enumerate(tell_phrases):
	for idx2,tell_class in enumerate(tell_classes):
		print "[{0} of {1}] [{2} of {3}]".format(idx1,len1,idx2,len2), "opening main page"
		try:
			driver.get('http://ipindiaonline.gov.in/tmrpublicsearch/frmmain.aspx')
			wait = WebDriverWait(driver, 15)

			wait.until(EC.visibility_of_element_located((By.ID, "ContentPlaceHolder1_BtnSearch")))
			print '\t main page opened'
			print '\t', tell_phrase, tell_class
			print '\t', 'entering query strings'
			inputWords = driver.find_element_by_id("ContentPlaceHolder1_TBWordmark")
			inputClass = driver.find_element_by_id("ContentPlaceHolder1_TBClass")
			inputWords.send_keys(tell_phrase)
			inputClass.send_keys(tell_class)
			enter_script = "document.getElementById('ContentPlaceHolder1_BtnSearch').click()"
			driver.execute_script(enter_script)
		except:
			print '\t', 'error with opening home page', '\a'
			continue

		print '\t', 'waiting for content to be loaded'
		try:
			wait1 = WebDriverWait(driver, 15)
			wait1.until(EC.visibility_of_element_located((By.ID, "ContentPlaceHolder1_MGVSearchResult")))
			print '\t', 'search result loaded'
			data = get_info('row') + get_info('alt')	#give time_sleep here if you want to change
		except:
			print '\t', 'No Records Found', '\a'
			try:
				alert = driver.switch_to_alert()
				alert.accept()
			except:
				print '\t', 'couldnt switch to alert'
			continue
		try:
			len3 = len(data)-1
			print '\t', 'saving images'
			# image saved as Word_Mark-Appl_No.png
			for idx3,word_mark in enumerate(data):
				photo_url = word_mark['photo']
				if photo_url:
					photo_name = word_mark['text']['Word Mark']+'-'+word_mark['text']['Appl. No.'].split()[0]
					print '\t\t', "[{0} of {1}]".format(idx3,len3), 'saving', photo_name
					driver.get(photo_url)
					

					driver.save_screenshot(tempDirectory+"/"+photo_name+'.png')
					# Decide here wether to move or delete.
					filepath=tempDirectory+"/"+photo_name+'.png'
					print filepath
					match=0
					for i in rotator:
						img=image(filepath,i)
						hashd=dhash(img)
						validate=len(select(hashd))
						if validate != 0:
							match+=1
							break
					if match ==0:
						print "Original Found"
						for i in rotator:
							img=image(filepath,i)
							hashd=dhash(img)
							insert(hashd)
							newfilepath=finalDir+"/"+photo_name+'.png'
							shutil.move(filepath,newfilepath)
							os.rename(filepath,newfilepath)
					else:
						print "Duplicate Found"


		except:
			print '\t', 'Error with images', '\a'
			continue
		complete_data+=data

driver.quit()
vdisplay.stop()
# Temporary JSON file - overwritten (not appended)
with open('data.txt', 'w') as outfile:
    json.dump(complete_data, outfile)

# HEADER [Phrase search,Class Number,Word Mark,Proprietor,Appl. No.,Appl. Date,Status,Journal No.,Journal Date,Used Since,Valid Upto,Goods & Services Description,Image Url]
# Appending to csv file
with open('data.csv', 'a') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows([[x['phrase'],x['class'],x['text']['Word Mark'],x['text']['Proprietor'],x['text']["Appl. No."].split()[0],x['text']["Appl. Date"],x['text']['Status'],x['text']["Journal No."].split('    ')[0],x['text']["Journal No."].split(':')[-1],x['text']['Used Since'].split('    ')[0],x['text']['Used Since'].split(':')[-1],x['text']['Goods & Services Description'],x['photo']] for x in complete_data])
