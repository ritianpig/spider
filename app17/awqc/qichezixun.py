# # 采集网站:https://www.pcauto.com.cn/chexun/ 太平洋汽车网

import requests
from lxml import etree
import lxml	
import pymysql 
import random
import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.wait import	WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


#连接数据库
db= pymysql.connect(host="localhost",user="root",
 	password="129426",db="appware",port=3306)

cur = db.cursor()

url = 'http://auto.gasgoo.com'

headers_list = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0']
headers = {
	'User_Agent':random.choice(headers_list)
}

# 根据网站特性，构造url池,抓取前300页内容
url_pool = []
for i in range(1,61):
	creat_url = 'http://auto.gasgoo.com/auto-news/C-101-102-103-104-105-106-501-601/%d'%(i)
	url_pool.append(creat_url)
# 构造所有分页url池
Paging = []
for i in url_pool:
	r2 = requests.get(url=i,headers=headers,timeout=60)
	r2.encoding = 'utf-8'
	two_html = etree.HTML(r2.text)
	page_url = two_html.xpath('//div[@class="listLeft"]/div[@class="content"]//h2/a/@href')
	Paging += page_url
	time.sleep(1)
Paging = list(set(Paging))


total_urls = []
for i in Paging:
	if 'http' not in i:
		i = url + i
	else:
		pass
	total_urls.append(i)
print(total_urls)

# 图片下载函数
def save_image(title,image):
	with open(title,'wb') as f:
		f.write(image.content)
		# f.flush()
		f.close()

# 文章img处理函数
def to_img(listx):
	d = []
	e = []

	for i in listx:
		d.append(str(i))
	for k in d:
		if '<Element img' in k:
			k = '[img]'
		e.append(k)

	id1 = [i for i,x in enumerate(e) if x=='[img]']
	for x,y in zip(range(1,len(id1)+1),id1):
		e[y] = '[img%s]'%(str(x))
	listx = e
	l = len(id1)
	return listx,l

for open_url,article_id in zip(total_urls,range(1,100000)):
	try:
		print('开始')
		print(open_url)

		r3 = requests.get(open_url,headers=headers,timeout=60)
		r3.encoding = 'utf-8'
		thrid_html = etree.HTML(r3.text)
		appid = 17
		article_name = thrid_html.xpath('//div[@class="detailed"]/h1//text()')[0]
		create_date = datetime.now()
		create_idate = int(str(create_date.date()).replace('-',''))
		# 内容标题
		article = thrid_html.xpath('//div[@id="ArticleContent"]/div[@class="viewImg"]//a[1]/img | //div[@style="text-align:center"]/img | //div[@id="ArticleContent"]//p//text()')

		contents,imageNum = to_img(article)
		content = ''.join(contents).replace('盖世汽车讯','')
		print(content,imageNum)
		# class_id = 112233

		countcollect = random.randint(1,400)
		countlike = random.randint(1,1500)

		column_id = 1
		# 写入数据库			
		sql_insert_article = """insert into content_article(article_id,appid,article_name,create_date,create_idate,url,content,imageNum,is_audit,countcollect,countlike) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
		db.ping(reconnect=True)
		cur.execute(sql_insert_article,(article_id,appid,article_name,create_date,create_idate,open_url,content,imageNum,1,countcollect,countlike))
		db.commit()

		sql_insert_content_column_article = """insert into content_column_article(column_id,article_id,article_name,imageNum,appid) values(%s,%s,%s,%s,%s)"""
		db.ping(reconnect=True)
		cur.execute(sql_insert_content_column_article,(column_id,article_id,article_name,imageNum,appid))
		db.commit()


		# 图片处理
		images_url = thrid_html.xpath('//div[@id="ArticleContent"]/div[@class="viewImg"]//a[1]/img/@src | //div[@style="text-align:center"]/img/@src')

		image_title = thrid_html.xpath('//div[@id="ArticleContent"]/div[@class="viewImg"]//a[1]/img/@title | //div[@style="text-align:center"]/img/@title')
		print(image_title)
		if not image_title:
			image_title = article_name
		else:
			image_title = image_title[0]

		if images_url:

			for image_url,num,in zip(images_url,range(1000,100000)):
				path_time = str(time.time()).replace('.','')

				print(image_url)
				re_extension = re.search('.*\.(.*)',image_url,re.S)
				path_picture = 'App%d/'%(appid) + 'class%d/'%(column_id) + '%d_'%(article_id) + path_time + '.' +re_extension.group(1)
				picture_name = '%d_'%(article_id) + path_time + '.' +re_extension.group(1)

				if 'http' in image_url:
					print(create_date)
		
					sql_insert_picture = """insert into content_picture(title,picture_name,create_date,create_idate,url,column_id,article_id,isaudit,label) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
					db.ping(reconnect=True)
					cur.execute(sql_insert_picture,(image_title,picture_name,create_date,create_idate,path_picture,column_id,article_id,1,'<img>'))
					db.commit()

					sql_insert_picture_compress = """insert into content_picture_compress(title,picture_name,create_date,create_idate,url,column_id,article_id,isaudit,count_like) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
					db.ping(reconnect=True)
					cur.execute(sql_insert_picture_compress,(image_title,picture_name,create_date,create_idate,path_picture,column_id,article_id,1,countlike))
					db.commit()
					print(picture_name)
					rsp_image = requests.get(image_url,headers,timeout=60)
					save_image(picture_name,rsp_image)
				else:
					image_url = 'http://auto.gasgoo.com' + image_url

					sql_insert_picture = """insert into content_picture(title,picture_name,create_date,create_idate,url,column_id,article_id,isaudit,label) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
					db.ping(reconnect=True)
					cur.execute(sql_insert_picture,(image_title,picture_name,create_date,create_idate,path_picture,column_id,article_id,1,'<img>'))
					db.commit()

					sql_insert_picture_compress = """insert into content_picture_compress(title,picture_name,create_date,create_idate,url,column_id,article_id,isaudit,count_like) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
					db.ping(reconnect=True)
					cur.execute(sql_insert_picture_compress,(image_title,picture_name,create_date,create_idate,path_picture,column_id,article_id,1,countlike))
					db.commit()

					rsp_image = requests.get(image_url,headers,timeout=60)
					save_image(picture_name,rsp_image)
		else:
			print('没有image')
		
		time.sleep(1)

	except:
		print("="*50)
		print('有错误')

db.close()