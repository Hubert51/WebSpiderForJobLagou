import re
import urllib.request
import urllib

# the type of parameter description is string
# the type of return is also string
def parserDescription(description):
	#remove anything thats enclosed inside < >
	description, number = re.subn("<[^>]*>", "", description)
	# remove line breaks,tabs, blank 
	description = description.replace('\n',"")
	description = description.replace(' ',"")
	description = description.replace('\r',"")
	description = description.replace('\t',"")
	# replace meaningless phrase
	description = description.replace("&nbsp;","")
	return description

# driver: chrome object
def setWindowSize(driver):
	screenHeight = "return window.screen.height"
	screenWidth = "return window.screen.width"
	screenHeight = driver.execute_script(screenHeight)
	screenWidth  = driver.execute_script(screenWidth)
	driver.set_window_size(screenWidth,screenHeight)

def getIpFromIpList(lock,ipList):
	lock.acquire()
	ip = ipList[-1]
	ipList.pop(-1)
	lock.release()
	return ip

def appendIp(lock,ipList,ip):
	lock.acquire()
	ipList.append(ip)
	lock.release()

class getProxy():

	def __init__(self):
		self.user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
		self.header = {"User-Agent": self.user_agent}
		self.ipList = []
		# self.dbname="proxy.db"
		# self.now = time.strftime("%Y-%m-%d")

	def getContent(self, num):
		nn_url = "http://list.didsoft.com/get?email=ruijiegeng@gmail.com&pass=jpammp&pid=httppremium"

		req = urllib.request.Request(nn_url, headers=self.header)
		resp = urllib.request.urlopen(req, timeout=10)
		content = resp.read().decode("utf-8")

		rawIpList = str(content).split("\n")
		for ip in rawIpList:
			ip = ip.split("#")[0]
			self.ipList.append(ip)

		# print(content)
		# result_odd = et.xpath('.//tr')
		# # #因为网页源码中class 分开了奇偶两个class，所以使用lxml最方便的方式就是分开获取。
		# # #刚开始我使用一个方式获取，因而出现很多不对称的情况，估计是网站会经常修改源码，怕被其他爬虫的抓到
		# # #使用上面的方法可以不管网页怎么改，都可以抓到ip 和port
		# for i in result_even:
		# 	t1 = i.xpath("./td/text()")[:2]
		# 	try:
		# 		self.ipList.append(t1[0]+":"+t1[1])
		# 		# print("IP:{}\tPort:{}".format(t1[0], t1[1]))

		# 	except:
		# 		continue

		# 	# if self.isAlive(t1[0], t1[1]):

		# 		# self.insert_db(self.now,t1[0],t1[1])
		# for i in result_odd:
		# 	t2 = i.xpath("./td/text()")[:2]
		# 	try:
		# 		self.ipList.append(t1[0]+":"+t2[1])
		# 		# print("IP:{}\tPort:{}".format(t2[0], t2[1]))
		# 	except:
		# 		continue

		# 	# if self.isAlive(t2[0], t2[1]):
		# 		# self.insert_db(self.now,t2[0],t2[1])


if __name__ == '__main__':
	
	p = getProxy()
	p.getContent(1)
