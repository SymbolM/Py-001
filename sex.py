# # -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
#import threading
import requests
import time
#import sys
import re
import os

Video_Type = input('请输入选项：1.在线视频 2.国产自拍 3.中文字幕 4.亚洲无码 5.欧美 6.制服 7.卡通 8.乱伦 9.名优 10.熟女 :\n ==>')
Page = input('输入下载页码（1-100）：\n ==>')
URL = 'https://qqchub520.com/vodshow/' + Video_Type + '--------' + Page + '---.html'

def get_sex_url(URL):
	html = requests.get(URL)
	soup = BeautifulSoup(html.content, 'lxml')
	url = soup.select("div.column .col_24 .col_5_1 a ")
	sex_url_list = []
	for i in url:
		sex_url = 'https://www.qqchub520.com' + i.get('href')
		sex_url_list.append(sex_url)
	return sex_url_list
def get_m3u8_url(num):
	m3u8_url = 'https://rzlkq.com/' + num[0] + '/1000kb/hls/index.m3u8'
	return m3u8_url
def get_video_url_list(m3u8_url):
	html = requests.get(m3u8_url)
	#print(html.text)
	list = re.findall(r'[\w]+''[0-9]*' + '.ts', html.text)
	#print(list)
	video_url_list = []
	for i in list:
		i = m3u8_url[:-10] + i
		video_url_list.append(i)
	return video_url_list
def get_video(video_url,key):
	video = requests.get(video_url).content  # .decode("UTF-8")
	cryptor = AES.new(key, AES.MODE_CBC, key)
	plain_text = cryptor.decrypt(video)
	return plain_text.rstrip(b'\0')
def get_key(num):
	key_url = 'https://rzlkq.com/' + num[0] + '/1000kb/hls/key.key'
	key = requests.get(key_url).content
	return key
def get_sex_title(URL):
	html = requests.get(URL)
	soup = BeautifulSoup(html.content, 'lxml')
	url = soup.select("div.column .col_24 .col_5_1 h2 ")
	#print(url)
	sex_title_list = []
	for i in range(0,len(url)):
		sex_title = url[i].text
		#print(sex_title)
		sex_title_list.append(sex_title)
	return sex_title_list
def get_number(sex_url):
	html = requests.get(sex_url)
	soup = BeautifulSoup(html.content, 'lxml')
	a = soup.select('.play-content > script')[0].text
	b = re.findall(r'\\/[0-9]+\\/', a)[0]
	num = re.findall(r'[0-9]+', b)
	return num
def save_file(video_url_list,key,num,FileName,PATH):
	cc = len(video_url_list)
	Down_Video_Flag = 0
	print('************开始下载************')
	print(FileName)
	for j in video_url_list:
		try:
			Down_Video_Flag = Down_Video_Flag + 1
			dd = float((Down_Video_Flag / cc) * 100)
			print('====>  ' + '%.2f'% dd + '%已下载' )
			file_path = PATH + '\\' + j[-8:]
			with open(file_path, 'ab+') as f:
				data = get_video(j,key)
				f.write(data)
			time.sleep(5)
		except:
			print('保存Video失败！')
			print(Down_Video_Flag)
			print(num)
		try:
			cmd = 'copy /b' + ' ' + PATH + '\\' + '*.ts' + ' ' + PATH + '\\' + 'new' + '.ts'  ####合并ts文件为MP4文件操作####
			cmd3 = 'ren' + ' ' + PATH + '\\' + 'new.ts' + ' ' + FileName + '.mp4'
			cmd2 = 'del' + ' ' + PATH + '\\' + '*.ts'
			os.system(cmd)
			os.system(cmd3)
			os.system(cmd2)
		except OSError as resean:
			print('合并文件失败！' + str(resean))
def main():
	title_list = get_sex_title(URL)
	list = get_sex_url(URL)
	title_list_flag = 0
	list_flag = 0
	for i in list:
			FileName = title_list[title_list_flag]
			PATH = 'D:\Download\\' + FileName
			try:
				os.mkdir(PATH)
			except FileExistsError as  fanhui:
				print('当前文件已下载！\n' + str(fanhui) )
				if title_list_flag < 20:
					title_list_flag = title_list_flag + 1
				if list_flag < 20:
					list_flag = list_flag + 1
				else:
					print('当前页面已经下载完成！')
			else:
				save_file(get_video_url_list(get_m3u8_url(get_number(i))),get_key(get_number(i)),get_number(i),FileName,PATH)
				if title_list_flag < 20:
					title_list_flag = title_list_flag + 1
				if list_flag < 20:
					list_flag = list_flag + 1
				else:
					print('当前页面已经下载完成！')

main()