from requests import get
from bs4 import BeautifulSoup as  BS
import tabulate
from pprint import pprint
import os,json
from threading import Thread

url = 'https://www.timeshighereducation.com/student/best-universities/top-50-universities-reputation-2018#survey-answer'
raw = get(url)
soup = BS(raw.text,'html.parser')
table = soup.find('table')
trs = table.findAll('tr')
universities = []
urls = []
for tr in trs:
	if trs.index(tr) != 0:
		urls.append(tr.find('a').get('href'))
	temp = tr.getText().split('\n')
	temp.pop()
	universities.append(temp[:])

# print(tabulate.tabulate(universities[1:],headers = universities[0]))
def getCourses(url,num):
	print('Thread',num,'Started')
	fileName = url[63:] + '.json'
	if os.path.exists(fileName):
		json_data = open(fileName).read()
		data = json.loads(json_data)
		print('Thread',num,'Ended')
		return data
	else:
		raw = get(url)
		soup = BS(raw.text,'html.parser')
		ul = soup.find('ul' , class_ = 'courses-list-group list-group')
		if ul != None:
			lis = ul.findAll('li')
			dic = {}
			courseList = []
			main_dic = {}
			for li in lis:
				if li.find('h3') != None:
					dic['courseName'] = li.find('h3').getText().strip()
				if [x.getText().strip() for x in li.findAll('li')] != []:
					dic['subjects'] = [x.getText().strip() for x in li.findAll('li')]
				if dic.copy() not in courseList:
					courseList.append(dic.copy())
			main_dic[url[63:]] = courseList
			with open(fileName,'w+') as file:
				json.dump(main_dic,file)
			print('Thread',num,'Ended')
			return main_dic

def allCourses(url_list):
	for num,url in enumerate(url_list):
		# getCourses(url,num)
		thread = Thread(target=getCourses,args = (url,num,))
		thread.start()
allCourses(urls)
