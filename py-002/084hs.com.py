# # -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time
import re
URL = 'https://084hs.com/Html/60/index-143.html'
sex_url_list = []
PATH = 'D:\\test01\\'
def get_sex_url(URL):
	html = requests.get(URL)
	soup = BeautifulSoup(html.content, 'lxml')
	url = soup.select("#wrap > div.main > div:nth-child(2) > div > div.inner_layer > ul > li:nth-child(1) > div > div > a")
	sex_url = 'https://www.064hs.com' + url[0].get('href')
	print(sex_url)
	return sex_url
def get_video(URL):
	html = requests.get(URL)
	soup = BeautifulSoup(html.content, 'lxml')
	url = soup.select("#wrap > div.main > div.widall > div > div.box > div:nth-child(3) > b > font > script")
	#print(sex_url)
	#return sex_url
def save_file(url):
	try:
		print('************开始下载************')
		file_path = PATH + '1.mp4'
		r = requests.get(url)
		with open(file_path, 'wb') as f:
			f.write(r.content)
		time.sleep(2)
	except:
		print('保存Video失败！')

print(get_video(get_sex_url(URL)))
