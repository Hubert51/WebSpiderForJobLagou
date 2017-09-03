#coding:utf8
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from .job import *
from .helper import parserDescription
from .helper import getProxy
from .helper import setWindowSize
from .helper import getIpFromIpList
from .helper import appendIp
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


# position: string, company: string, source: string, pathOfChromedriver: string
# jobList: list, ipList: list
# index: integer
# ipList contains proxy ip to get information
# index is an integer which is the index of proxy ip in ipList we will use
def getInfo(position, company, source, jobList,ipList, index,pathOfChromedriver,lock):
	oldIndex = index

	while True:
		try:
			job = position.find_element_by_css_selector("h3").get_attribute("innerHTML")
			salary = position.find_element_by_class_name("money").get_attribute("innerHTML")
			# to get url of job description
			urlOfDescription = position.find_element_by_tag_name("a").get_attribute("href")
			break
		except:
			continue

	# open a new driver to deal url of description
	# driverToGetDescription = webdriver.Chrome(pathOfChromedriver)
	# use while loop will not stop until the proxy ip is valid
	print("Crawling No.{:} job".format(index+1))
	while True:
		try:
			# open a new driver to deal url of description
			chromeOptions = webdriver.ChromeOptions()

			ip = getIpFromIpList(lock,ipList)

			if ip == "approveToUseSelfIp":
				# to use self ip 
				driverToGetDescription =webdriver.Chrome(pathOfChromedriver)
			else:
				# to use proxy ip
				chromeOptions.add_argument('--proxy-server={:}'.format(ip))
				driverToGetDescription = webdriver.Chrome(pathOfChromedriver,chrome_options=chromeOptions)
				# when the page open, it has 35 seconds to load resource. After that, the load process will
				# be set down
				driverToGetDescription.set_page_load_timeout(25)

			try:
				driverToGetDescription.get(urlOfDescription)
			except:
				try:
					description = driverToGetDescription.find_element_by_class_name("job_bt").get_attribute("innerHTML")
					appendIp(lock,ipList,ip)
					break
				except:
					# we won't throw self ip away though something wrong happened
					# we won't use wrong proxy ip in following process.
					if ip == "approveToUseSelfIp":
						ipList.append(ip)

					driverToGetDescription.close()
					print("No.{} job is crawled failed".format(index+1))
					continue

			description = driverToGetDescription.find_element_by_class_name("job_bt").get_attribute("innerHTML")
			appendIp(lock,ipList,ip)
			break

		except:
			if ip == "approveToUseSelfIp":
				ipList.append(ip)
			driverToGetDescription.close()
			print("No.{} job is crawled failed".format(index+1))
			continue
	print("No.{} job is crawled successfully".format(index+1))

	# get content of description
	description = parserDescription(description)

	# close the description window
	driverToGetDescription.close()

	# description=""
	jobObject = Job(job, description,salary,company,source)
	print("Job Storeed\n")
	# print(jobObject.toJson().values())
	jobList.append(jobObject)

# driver: webdriver object
# company: string, source: string, pathOfChromedriver: string
# jobList: list, ipList: list
def handleMultiPage(driver, company, source, jobList,pathOfChromedriver,ipList):
	# to get all of useful inforamtion in one page		

	time.sleep(1)
	# let most useful ip be the end of the list
	ipList = ipList[::-1]
	ipList.append("approveToUseSelfIp")
	# the "con_list_item" class contains salary, title and description page of this job
	positions = driver.find_elements_by_class_name("con_list_item")
	numberOfPosition = len(positions)

	# the list to store threads which will deal all of data in one page at same time.
	threads = []
	# lock the ip list among thread
	lock = threading.Lock()

	for index in range(numberOfPosition):
		# target is function. args is argument for target function
		thread = threading.Thread(target=getInfo,args=(	positions[index],
														company,
														source,
														jobList,
														ipList,
														index,
														pathOfChromedriver,
														lock))
		threads.append(thread)

	for index in range(numberOfPosition):
		threads[index].start()
		time.sleep(4)
	for index in range(numberOfPosition):
		threads[index].join()
	threads.clear()


# companyName: string
def lagouMethod(companyName):
	jobList = []		# to store job object

	# plug-in unit to operate chrome
	path = os.path.realpath(__file__)
	pathOfChromedriver = path.strip("lagou.py")+"chromedriver"
	driver = webdriver.Chrome(pathOfChromedriver)

	setWindowSize(driver)

	# the job information of that company
	url = "https://www.lagou.com/jobs/list_" + companyName + "?labelWords=&fromSearch=true&suginput="
	
	driver.set_page_load_timeout(15)

	# to simulate user request
	while True:
		try:
			driver.get(url)
			# to know the total pages of jobs in this company
			totalNumberOfPage = int(driver.find_element_by_class_name("totalNum").get_attribute("innerHTML"))
			break
		except:
			driver.close()
			continue
	print("Open main page of {:} successfully".format(companyName))

	for index in range(totalNumberOfPage): 
		# to get proxy ip from website.
		# these proxy ip are reset every ten minutes. So I put code inside for loop
		ipObject = getProxy()
		ipObject.getContent(1)
		ipList = ipObject.ipList

		handleMultiPage(driver, companyName, "lagou", jobList,pathOfChromedriver,ipList)

		if index+1 == totalNumberOfPage:
			break
			
		# try two button one by one
		print("Turning the page")
		while True:
			try:
				# js code to scroll down the window
				js = "var q=document.body.scrollTop=100000"  
				driverToGetDescription.execute_script(js)
				elem = driver.find_element_by_class_name("pager_next").click()
				break
			except:
				try:
					js = "var q=document.body.scrollTop=0"  
					driver.execute_script(js) 
					elem = driver.find_element_by_class_name("next_disabled").click()
					break
				except:
					print("button does not work")
					time.sleep(2)
		print("Turn to page {:}".format(index+2))

		time.sleep(2)
	driver.close()
	return jobList

if __name__ == '__main__':
# 	# the company we want to find job
	companyName = input("Please input company name-> ")
	jobList = lagouMethod(companyName)

