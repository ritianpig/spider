import requests
from lxml import etree
import random
import time
import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import	WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import string
from PIL import Image
import asyncio
import aiohttp
import re
from datetime import datetime
from io import StringIO
import pymysql
import imghdr
from urllib import request

url = 'https://car.autohome.com.cn'

headers_list = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0']
headers = {
	'User_Agent':random.choice(headers_list)
}

db= pymysql.connect(host="localhost",user="root",
	 	password="129426",db="appware",port=3306)
cur = db.cursor()

start = time.time()
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('user-agent={}'.format(random.choice(headers_list)))
browser = webdriver.Chrome(chrome_options=options)
locator = (By.XPATH,'//html')
r1 = browser.get('https://car.autohome.com.cn')
browser.set_page_load_timeout = 300
browser.set_script_timeout = 300
WebDriverWait(browser,30,0.5).until(EC.presence_of_element_located(locator))
source1 = browser.page_source
one_html = etree.HTML(source1)



async def save_images(name,url,title):
	session = aiohttp.ClientSession()
	response = await session.get(url,headers=headers)
	content = await response.content.read()
	# title = title + '.' + imghdr.what('',content)
	with open('/home/mr/图片/App17/class3/%s/%s'%(name,title),'wb') as f:
		f.write(content)

def save_image(name,title,response):
	data = response.content
	with open('/home/mr/图片/App17/class3/%s/%s'%(name,title),'wb') as f:
			f.write(data)

def to_img(article):
	'''处理文章中的图片显示位置和图片个数，listx为处理过的文章'''
	d = []
	e = []
	for i in article:
		d.append(str(i))
	for k in d:
		if '<Element img' in k:
			k = '[img]'
		e.append(k)

	id1 = [i for i,x in enumerate(e) if x=='[img]']
	for x,y in zip(range(1,len(id1)+1),id1):
		e[y] = '[img%s]'%(str(x))
	article = e
	img_num = len(id1)
	return article,img_num

def save_series_class_article(a,b,c):
	sql_insert_series_class_article = """insert into series_class_article(class_id,article_id,appid) values(%s,%s,%s)"""
	db.ping(reconnect=True)
	cur.execute(sql_insert_series_class_article,(a,b,c))
	db.commit()

def save_series_child_picture(a,b,c,d,e,f,g,h):
	sql_insert_series_child_picture = """insert into series_child_picture(picture_id,title,picture_name,create_date,create_idate,child_class_id,url,img_url) values(%s,%s,%s,%s,%s,%s,%s,%s)"""
	db.ping(reconnect=True)
	cur.execute(sql_insert_series_child_picture,(a,b,c,d,e,f,g,h))
	db.commit()

def save_series_child_class(a,b,c,d,e):
	sql_insert_series_child_class = """insert into series_child_class(child_class_id,class_id,child_id,child_name,appid) values(%s,%s,%s,%s,%s)"""
	db.ping(reconnect=True)
	cur.execute(sql_insert_series_child_class,(a,b,c,d,e))
	db.commit()


def save_series(a,b,c,d,e,f,g,h,i): 
	sql_insert_series = """insert into series(series_id,series_name,series_url,img_url,series_translate,create_idate,appid,create_date,remark) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
	db.ping(reconnect=True)
	cur.execute(sql_insert_series,(a,b,c,d,e,f,g,h,i,))
	db.commit()

def save_series_class(a,b,c,d,e,f,g,h,i,j,k,l,m): 
	sql_insert_series_class = """insert into series_class(class_id,class_name,img_url,class_url,create_idate,create_date,class_title,class_center,class_remark,series_id,appid,price,score) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
	db.ping(reconnect=True)
	cur.execute(sql_insert_series_class,(a,b,c,d,e,f,g,h,i,j,k,l,m))
	db.commit()

def save_series_child(a,b,c,d,e,f): 
	sql_insert_child = """insert into series_child(child_id,child_name,url,img_url,create_date,create_idate) values(%s,%s,%s,%s,%s,%s)"""
	db.ping(reconnect=True)
	cur.execute(sql_insert_child,(a,b,c,d,e,f))
	db.commit()

def save_content_article(a,b,c,d,e,f,g,h,i,j): 
	sql_insert_article = """insert into content_article(article_id,appid,article_name,create_date,create_idate,url,content,imageNum,is_audit,countcollect,countlike) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
	db.ping(reconnect=True)
	cur.execute(sql_insert_article,(a,b,c,d,e,f,g,h,1,i,j))
	db.commit()

def save_content_pciture(a,b,c,d,e,f,g,h):
	sql_insert_picture = """insert into content_picture(picture_id,title,picture_name,create_date,create_idate,url,column_id,article_id,isaudit,label) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
	db.ping(reconnect=True)
	cur.execute(sql_insert_picture,(a,b,c,d,e,f,g,h,1,'<img>'))
	db.commit()


def save_content_picture_compress(a,b,c,d,e,f,g,h,i):
	sql_insert_picture_compress = """insert into content_picture_compress(picture_id,title,picture_name,create_date,create_idate,url,column_id,article_id,isaudit,count_like) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
	db.ping(reconnect=True)
	cur.execute(sql_insert_picture_compress,(a,b,c,d,e,f,g,h,1,i))
	db.commit()


def cat_child_class_id():
	search_child_class_id = "select child_class_id from series_child_class order by child_class_id DESC limit 1"
	cur.execute(search_child_class_id)
	last_child_class_id = cur.fetchone()
	if last_child_class_id is None:
			last_child_class_id = 1
	else:
		last_child_class_id = last_child_class_id[0] + 1
	return last_child_class_id
# 第一步，所有车系链接,获取到的数据，series_id自增，series_name,车系名，series_url,车系
# 对应的链接，img_url(logo图标),series_translate,车系首字母,appid=17，
# 公共数据
appid = 17

car_url = one_html.xpath('//div[@id="cartree"]//ul//a/@href')
print(car_url)
for i,n in zip(car_url,range(1,2000)):
	create_date1 = datetime.now()
	create_idate1 = int(str(create_date1.date()).replace('-',''))
	if 'http' in str(i):
		url = str(i)
	else:
		url = 'https://car.autohome.com.cn' + str(i)
	try:
		r2 = browser.get(url)
		source2 = browser.page_source
		two_html = etree.HTML(source2)
	except:
		print(url,'r2请求错误')

	# 车系变量
	# 系列首字母缩写
	series_translate = two_html.xpath('//div[@id="cartree"]//a[@href="%s"]/ancestor::ul[1]/preceding-sibling::div[1]/text()'%(i))[0]
	# 系列id
	series_id = n
	# 系列名
	series_name = two_html.xpath('//div[@id="cartree"]//a[@href="%s"]/text()[1]'%(i))[0]
	# 系列链接
	series_url = url
	remark = 'test'
	# 系列图片链接
	logo_url = two_html.xpath('//div[@class="carbradn-pic"]/img/@src')[0]
	if 'http' in str(logo_url):
		pass
	else:
		logo_url = 'https:' + str(logo_url)
	try:
		r3 = requests.get(logo_url,headers=headers)
		data = r3.content
		pic_extension = imghdr.what('',data)
		logo_name = series_name + '.' + pic_extension

		try:
			save_image('logo',logo_name,r3)
			print('ok')

			img_url = '/App17/class3/logo/%s'%(logo_name)

			save_series(series_id,series_name,series_url,img_url,series_translate,create_idate1,appid,create_date1,remark)
		except:
			print('保存logo或者series出错')
	except:
		print('请求logo图片出错')


	# 第二步爬去分类信息，汽车型号，型号id，汽车图片....
	try:
		r4 = requests.get(series_url)
		r4.encoding = 'gb2312'
		three_html = etree.HTML(r4.text)
	except:
		print('r4请求错误')

	cars_name = three_html.xpath('//div[@class="list-dl-text"]//a/text()')
	cars_url = three_html.xpath('//div[@class="list-dl-text"]//a/@href')
	for car_name,car_url,num in zip(cars_name,cars_url,range(1000)):
		create_date2 = datetime.now()
		create_idate2 = int(str(create_date2.date()).replace('-',''))

		# 实现child_id自增，通过查询数据库，最后一个id
		search_id = "select class_id from series_class order by class_id DESC limit 1"
		cur.execute(search_id)
		last_id = cur.fetchone()
		if last_id is None:
			last_id = 0
		else:
			last_id = last_id[0]
		
		class_id = last_id + 1
		class_name = three_html.xpath('//div[@class="list-dl-text"]//a[text()="{}"]/../preceding-sibling::div[1]/text()'.format(car_name))[0].replace('：','')
		
		if 'http' in str(car_url):
			car_url = str(car_url)
		else:
			car_url = 'https://car.autohome.com.cn' + str(car_url)

		try:
			r5 = requests.get(car_url,headers=headers,timeout=180)
			r5.encoding='gb2312'
			# source5 = browser.page_source
			four_html = etree.HTML(r5.text)
		except:
			print('r5请求错误')

		# 获取价格price，评分score
		
		try:
			price = four_html.xpath('//span[@class="lever-price red"]/span/text()')[0]
		except:
			price = '暂无'
		try:
			score = four_html.xpath('//span[@class="score-number"]/text()')[0]
		except:
			score = '暂无'

		# 获取汽车型号首个缩略图
		try:
			index_pic = four_html.xpath('//div[@class="list-cont-img"]/a/img/@src')[0]
		except:
			print(car_name,'无缩略图')
		if 'http' in str(index_pic):
			index_pic = str(index_pic)
		else:
			index_pic = 'https:'+str(index_pic)
		try:
			r6 = requests.get(index_pic,headers=headers,timeout=120)
			index_name = car_name + '.' + imghdr.what('',r6.content)
			index_img_url = '/App17/index_img/%s'%(index_name)
		except:
			print('r6获取缩略图失败')

		class_title = 'null'
		class_center = 'null'
		class_remark = 'null'

		try:
			save_image('index_img',index_name,r6)

			save_series_class(class_id,car_name,index_img_url,car_url,create_idate2,create_date2,class_title,class_center,class_remark,series_id,appid,price,score)
		except:
			print('保存index_img,或者seriess_child出错')

		# 获取车型下详细图片信息	
		try:
			first_pic_url = four_html.xpath('//div[@class="header-nav"]//li[2]/a/@href')[0]
		except:
			print(car_name,'没有详细图片')
		if 'http' in str(first_pic_url):
			first_pic_url = str(first_pic_url)
		else:
			first_pic_url = 'https://car.autohome.com.cn' + str(first_pic_url)

		try:
			r7 = requests.get(first_pic_url,headers=headers,timeout=180)
			r7.encoding='gb2312'
			five_html = etree.HTML(r7.text)
		except:
			print('r7请求错误')
		
		try:
			surface_urls = five_html.xpath('//div[@class="uibox-title"]//a[contains(text(),"车身外观")]/../following-sibling::div[1]/ul//li/a/img/@src')

			tasks = []
			loop = asyncio.get_event_loop()
			for surface_img in surface_urls :
				search_id2 = "select picture_id from series_child_picture order by picture_id DESC limit 1"
				cur.execute(search_id2)
				last_id = cur.fetchone()

				if last_id is None:
					last_id = 0
				else:
					last_id = last_id[0]
				picture_id = int(last_id) + 1

				surface_img = str(surface_img)
				
				if 'http' in surface_img:
					pass
				else:
					surface_img = 'https:' + surface_img

				create_date3 = datetime.now()
				create_idate3 = int(str(create_date3.date()).replace('-',''))
				path_time1 = str(time.time()).replace('.','')
				# re_extension = re.search('.*\.(.*)',surface_img,re.S)
				title = car_name + '_' + '外观'
				local_title = str(class_id) + '_' + path_time1 + '.' + 'jpg'
				
				url = '/App17/class3/surface/{}'.format(local_title)
				img_url = url
				child_class_id = cat_child_class_id()
				child_name = '外观'
				save_series_child_picture(picture_id,title,local_title,create_date3,create_idate3,child_class_id,url,img_url)	
				task = asyncio.ensure_future(save_images('surface',surface_img,local_title))
				tasks.append(task)

			last_child_class_id = cat_child_class_id()
			save_series_child_class(last_child_class_id,class_id,1,'外观',appid)

		except:
			print('暂无外观图片')

		try:
			centers = five_html.xpath('//div[@class="uibox-title"]//a[contains(text(),"中控方向盘")]/../following-sibling::div[1]/ul//li/a/img/@src')	
			for center_url in centers :
				search_id = "select picture_id from series_child_picture order by picture_id DESC limit 1"
				cur.execute(search_id)
				last_id = cur.fetchone()

				if last_id is None:
					last_id = 0
				else:
					last_id = last_id[0]
				picture_id = int(last_id) + 1

				center_url = str(center_url)
				
				if 'http' in center_url:
					pass
				else:
					center_url = 'https:' + center_url

				create_date4 = datetime.now()
				create_idate4 = int(str(create_date4.date()).replace('-',''))
				path_time2 = str(time.time()).replace('.','')
				# re_extension = re.search('.*\.(.*)',center_url,re.S)
				title = car_name + '_' + '中控'
				local_title = str(class_id) + '_' + path_time2 + '.' + 'jpg'
				
				url = '/App17/class3/center/{}'.format(local_title)
				img_url = url
				child_class_id = cat_child_class_id()
				child_name = '中控'
				save_series_child_picture(picture_id,title,local_title,create_date3,create_idate3,child_class_id,url,img_url)	
				task = asyncio.ensure_future(save_images('center',center_url,local_title))
				tasks.append(task)

			last_child_class_id = cat_child_class_id()
			save_series_child_class(last_child_class_id,class_id,2,'中控',appid)

		except:
			print('暂无中控图片')

		try:
			chairs = five_html.xpath('//div[@class="uibox-title"]//a[contains(text(),"车厢座椅")]/../following-sibling::div[1]/ul//li/a/img/@src')
			for chair_url in chairs :
				search_id2 = "select picture_id from series_child_picture order by picture_id DESC limit 1"
				cur.execute(search_id2)
				last_id = cur.fetchone()

				if last_id is None:
					last_id = 0
				else:
					last_id = last_id[0]
				picture_id = int(last_id) + 1

				chair_url = str(chair_url)
				
				if 'http' in chair_url:
					pass
				else:
					chair_url = 'https:' + chair_url

				create_date4 = datetime.now()
				create_idate4 = int(str(create_date4.date()).replace('-',''))
				path_time3 = str(time.time()).replace('.','')
				# re_extension = re.search('.*\.(.*)',chair_url,re.S)
				title = car_name + '_' + '座椅'
				local_title = str(class_id) + '_' + path_time3 + '.' + 'jpg'
				
				url = '/App17/class3/chair/{}'.format(local_title)
				img_url = url
				child_class_id = cat_child_class_id()
				child_name = '座椅'
				save_series_child_picture(picture_id,title,local_title,create_date3,create_idate3,child_class_id,url,img_url)	
				task = asyncio.ensure_future(save_images('chair',chair_url,local_title))
				tasks.append(task)

			last_child_class_id = cat_child_class_id()
			save_series_child_class(last_child_class_id,class_id,3,'座椅',appid)

		except:
			print('暂无座椅图片')

		try:
			others = five_html.xpath('//div[@class="uibox-title"]//a[contains(text(),"其它细节")]/../following-sibling::div[1]/ul//li/a/img/@src')

			for others_url in others :
				search_id2 = "select picture_id from series_child_picture order by picture_id DESC limit 1"
				cur.execute(search_id2)
				last_id = cur.fetchone()

				if last_id is None:
					last_id = 0
				else:
					last_id = last_id[0]
				picture_id = int(last_id) + 1

				others_url = str(others_url)
				
				if 'http' in others_url:
					pass
				else:
					others_url = 'https:' + others_url

				create_date4 = datetime.now()
				create_idate4 = int(str(create_date4.date()).replace('-',''))
				path_time4 = str(time.time()).replace('.','')
				# re_extension = re.search('.*\.(.*)',others_url,re.S)
				title = car_name + '_' + '其他细节'
				local_title = str(class_id) + '_' + path_time4 + '.' + 'jpg'
				
				url = '/App17/class3/others/{}'.format(local_title)
				img_url = url
				child_class_id = cat_child_class_id()
				child_name = '其他细节'
				save_series_child_picture(picture_id,title,local_title,create_date3,create_idate3,child_class_id,url,img_url)	
				task = asyncio.ensure_future(save_images('others',others_url,local_title))
				tasks.append(task)

			last_child_class_id = cat_child_class_id()
			save_series_child_class(last_child_class_id,class_id,4,'其他细节',appid)
		except:
			print('暂无其他细节图片')
		# loop.run_until_complete(asyncio.wait(tasks))

		
		# 文章进入链接
		try:
			index_article = four_html.xpath('//div[@class="main-title"]/a/@href')[0]
			index_article = str(index_article)
		except:
			print('获取进入文章链接失败')
		if 'http' in index_article:
			pass
		else:
			index_article = 'https:'+index_article

		try:
			r12 = requests.get(index_article,headers=headers,timeout=180)
			r12.encoding='gb2312'
			six_html = etree.HTML(r12.text)
		except:
			print('r12请求错误')

		try:
			nwes_article = six_html.xpath('//div[@class="athm-title__sub"]/dl//dd[1]/a/@href')[0]
		except:
			nwes_article = ''

		# 存在没有文章的车系，判断一下

		if nwes_article:
			try:
				nwes_article = str(nwes_article)
				if 'http' in nwes_article:
					pass
				else:
					nwes_article = 'https://www.autohome.com.cn' + nwes_article

				try:
					r13 = requests.get(nwes_article,headers=headers,timeout=180)
					r13.encoding = 'gb2312'
					seven_html = etree.HTML(r13.text)
				except:
					print('r13请求错误')

				try:
					last_page_num = six_html.xpath('//div[@class="page"]/a[last()]/preceding-sibling::a[1]//text()')[0]
				except:
					last_page_num = ''
				
				articles_url = []
				re_rule = re.compile('0-\S-0')
				if last_page_num:
					if int(last_page_num) >= 4:
						last_page_num = '4'
					else:
						pass

					for i in range(1,int(last_page_num)+1):
						create_url = re_rule.sub('0-{}-0'.format(i),nwes_article)
						articles_url.append(create_url)
				else:
					articles_url.append(nwes_article)

				all_pages = []
				for page in articles_url:
					try:		
						r14 = requests.get(page)
						r14.encoding = 'utf-8'
						eight_html = etree.HTML(r14.text)
						url = eight_html.xpath('//div[@class="cont-info"]/ul//li//h3/a/@href')
						all_pages += url
					except:
						print('r14请求错误')
				
				print(all_pages)

				for every_page in all_pages:
					search_article_id= "select article_id from content_article order by article_id DESC limit 1"
					cur.execute(search_article_id)
					last_id = cur.fetchone()

					if last_id is None:
						last_id = 0
					else:
						last_id = last_id[0]
					article_id = int(last_id) + 1

					if 'http' in every_page:
						pass
					else:
						every_page = 'https:' + every_page

					try:
						r15 = requests.get(every_page,headers=headers,timeout=180)
						r15.encoding = 'gb2312'
						nine_html = etree.HTML(r15.text)
					except:
						print('获取页面错误：',every_page)
					
					try:

						try:
							article_name = nine_html.xpath('//div[@id="articlewrap"]/h1/text()')[0]
							print(article_name)
						except:
							print('没有aarticle_name',every_page)
							
						countcollect = random.randint(1,400)
						countlike = random.randint(1,1500)

						article = nine_html.xpath('//div[@class="details"]/p/text() | //div[@class="details"]/p//img')

						article_img = nine_html.xpath('//div[@class="details"]/p//img/@src')

						try:
							for pic_url in article_img:

								pic_url = str(pic_url)
								if 'http' in pic_url:
									pass
								else:
									pic_url = 'https:' + pic_url
								# r16 = requests.get(pic_url,headers=headers,timeout=240)

								search_id= "select picture_id from content_picture order by picture_id DESC limit 1"
								cur.execute(search_id)
								last_id = cur.fetchone()

								if last_id is None:
									last_id = 0
								else:
									last_id = last_id[0]
								picture_id = int(last_id) + 1

								create_date7 = datetime.now()
								create_idate7 = int(str(create_date7.date()).replace('-',''))
								# re_extension = re.search('.*\.(.*)',pic_url,re.S)
								path_time5 = str(time.time()).replace('.','')

								picture_name = str(article_id) + '_' + path_time5 +'.' + 'jpg'
								picture_path = '/App17/class3/article/{}'.format(picture_name)
								task = asyncio.ensure_future(save_images('article',pic_url,picture_name))
								tasks.append(task)
								save_content_pciture(picture_id,article_name,picture_name,create_date7,create_idate7,picture_path,3,article_id)
								save_content_picture_compress(picture_id,article_name,picture_name,create_date7,create_idate7,picture_path,3,article_id,countlike)
							loop.run_until_complete(asyncio.wait(tasks))


								# save_image('article',picture_name,r16)
								# save_content_pciture(picture_id,article_name,picture_name,create_date7,create_idate7,picture_path,3,article_id)
								# save_content_picture_compress(picture_id,article_name,picture_name,create_date7,create_idate7,picture_path,3,article_id,countlike)
						except:
							print('保存文章图片失败')

						contents,imageNum = to_img(article)
						create_date8 = datetime.now()
						create_idate8 = int(str(create_date8.date()).replace('-',''))
						re_head = re.compile('\[汽\D+\]')
						re_tail = re.compile('\（文\D+\）')
						re_tail1 = re.compile('\(编\D+\)')
						content_one = ''.join(contents)
						content_two = re_head.sub('',content_one)
						content_three = re_tail.sub('',content_two).replace('[ ]','')
						content = re_tail1.sub('',content_three)
						print(content)

						column_id = 3
						save_content_article(article_id,appid,article_name,create_date8,create_idate8,every_page,content,imageNum,countcollect,countlike)
						save_series_class_article(class_id,article_id,appid)
						
					except:
						print('==========================')
			except:
				print('文章GG')

		else:
			print('没有文章')
		
browser.close()
browser.quit()


# for surface_img,num in zip(surface_urls,range(1,50)):
			# 	search_id1 = "select child_class_id from series_child_class order by child_class_id DESC limit 1"
			# 	cur.execute(search_id1)
			# 	last_id = cur.fetchone()

			# 	if last_id is None:
			# 		last_id = 0
			# 	else:
			# 		last_id = last_id[0]
			# 	child_class_id = int(last_id) + 1

			# 	search_id2 = "select picture_id from series_child_picture order by picture_id DESC limit 1"
			# 	cur.execute(search_id2)
			# 	last_id = cur.fetchone()

			# 	if last_id is None:
			# 		last_id = 0
			# 	else:
			# 		last_id = last_id[0]
			# 	picture_id = int(last_id) + 1

			# 	if 'http' in str(surface_img):
			# 		surface_url = str(surface_img)
			# 	else:
			# 		surface_url = 'https:'+str(surface_img)

			# 	r8 = requests.get(surface_url)
			# 	create_date3 = datetime.now()
			# 	create_idate3 = int(str(create_date3.date()).replace('-',''))
			# 	path_time1 = str(time.time()).replace('.','')
			# 	title = car_name + '_' + '外观'
			# 	local_title = str(class_id) + '_' + path_time1 + '.' + imghdr.what('',r8.content) 

			# 	url = '/App17/class3/surface/{}'.format(local_title)
			# 	img_url = url
			# 	child_id = 1
			# 	child_name = '外观'
			# 	save_image('surface',local_title,r8)
			# 	save_series_child_class(child_class_id,class_id,child_id,child_name,appid)
			# 	save_series_child_picture(picture_id,title,local_title,create_date3,create_idate3,child_class_id,url,img_url)	

		# except:
		# 	print(car_name,'获取外观图片失败')

		# try:
		# 	centure_control = five_html.xpath('//div[@class="uibox-title"]//a[contains(text(),"中控方向盘")]/../following-sibling::div[1]/ul//li/a/img/@src')	
		# 	for control_img,num in zip(centure_control,range(1,50)):
		# 		search_id1 = "select child_class_id from series_child_class order by child_class_id DESC limit 1"
		# 		cur.execute(search_id1)
		# 		last_id = cur.fetchone()

		# 		if last_id is None:
		# 			last_id = 0
		# 		else:
		# 			last_id = last_id[0]
		# 		child_class_id = int(last_id) + 1

		# 		search_id2 = "select picture_id from series_child_picture order by picture_id DESC limit 1"
		# 		cur.execute(search_id2)
		# 		last_id = cur.fetchone()

		# 		if last_id is None:
		# 			last_id = 0
		# 		else:
		# 			last_id = last_id[0]
		# 		picture_id = int(last_id) + 1

		# 		if 'http' in str(control_img):
		# 			control_url = str(control_img)
		# 		else:
		# 			control_url = 'https:'+str(control_img)

		# 		r9 = requests.get(control_url)
		# 		create_date4 = datetime.now()
		# 		create_idate4 = int(str(create_date4.date()).replace('-',''))
		# 		path_time2 = str(time.time()).replace('.','')
		# 		title = car_name + '_' + '中控'
		# 		local_title = str(class_id) + '_' + path_time2 + '.' + imghdr.what('',r9.content) 
		# 		url = '/App17/class3/center/{}'.format(local_title)
		# 		img_url = url
		# 		child_id = 2
		# 		child_name = '中控'
		# 		save_image('center',local_title,r9)
		# 		save_series_child_class(child_class_id,class_id,child_id,child_name,appid)
		# 		save_series_child_picture(picture_id,title,local_title,create_date4,create_idate4,child_class_id,url,img_url)
					
		# except:
		# 	print(car_name,'获取中控图片失败')

		# try:
		# 	chair = five_html.xpath('//div[@class="uibox-title"]//a[contains(text(),"车厢座椅")]/../following-sibling::div[1]/ul//li/a/img/@src')
		# 	for chair_img,num in zip(chair,range(1,50)):
		# 		search_id1 = "select child_class_id from series_child_class order by child_class_id DESC limit 1"
		# 		cur.execute(search_id1)
		# 		last_id = cur.fetchone()

		# 		if last_id is None:
		# 			last_id = 0
		# 		else:
		# 			last_id = last_id[0]
		# 		child_class_id = int(last_id) + 1

		# 		search_id2 = "select picture_id from series_child_picture order by picture_id DESC limit 1"
		# 		cur.execute(search_id2)
		# 		last_id = cur.fetchone()

		# 		if last_id is None:
		# 			last_id = 0
		# 		else:
		# 			last_id = last_id[0]
		# 		picture_id = int(last_id) + 1

		# 		if 'http' in str(chair_img):
		# 			chair_url = str(chair_img)
		# 		else:
		# 			chair_url = 'https:'+str(chair_img)

		# 		r10 = requests.get(chair_url)
		# 		create_date5 = datetime.now()
		# 		create_idate5 = int(str(create_date5.date()).replace('-',''))
		# 		path_time3 = str(time.time()).replace('.','')
		# 		title = car_name + '_' + '座椅'
		# 		local_title = str(class_id) + '_' + path_time3 + '.' + imghdr.what('',r10.content) 
		# 		url = '/App17/class3/chair/{}'.format(local_title)
		# 		img_url = url
		# 		child_id = 3
		# 		child_name = '座椅'
		# 		save_image('chair',local_title,r10)
		# 		# save_series_child_class(child_class_id,class_id,child_id,child_name,appid)
		# 		# save_series_child(child_id,child_name,url,img_url,create_date6,create_idate6)
		# 		save_series_child_picture(picture_id,title,local_title,create_date5,create_idate5,child_class_id,url,img_url)
		# except:
		# 	print(car_name,'获取座椅图片失败')	

		# try:
		# 	others = five_html.xpath('//div[@class="uibox-title"]//a[contains(text(),"其它细节")]/../following-sibling::div[1]/ul//li/a/img/@src')
		# 	for others_img,num in zip(others,range(1,50)):
		# 		search_id1 = "select child_class_id from series_child_class order by child_class_id DESC limit 1"
		# 		cur.execute(search_id1)
		# 		last_id = cur.fetchone()

		# 		if last_id is None:
		# 			last_id = 0
		# 		else:
		# 			last_id = last_id[0]
		# 		child_id = int(last_id) + 1

		# 		search_id2 = "select picture_id from series_child_picture order by picture_id DESC limit 1"
		# 		cur.execute(search_id2)
		# 		last_id = cur.fetchone()

		# 		if last_id is None:
		# 			last_id = 0
		# 		else:
		# 			last_id = last_id[0]
		# 		picture_id = int(last_id) + 1

		# 		if 'http' in str(others_img):
		# 			othres_url = str(others_img)
		# 		else:
		# 			others_url = 'https:'+str(others_img)

		# 		r11 = requests.get(others_url)
		# 		create_date6 = datetime.now()
		# 		create_idate6 = int(str(create_date6.date()).replace('-',''))
		# 		path_time4 = str(time.time()).replace('.','')
		# 		title = car_name + '_' + '细节'
		# 		local_title = str(class_id) + '_' + path_time4 + '.' + imghdr.what('',r11.content) 
		# 		url = '/App17/class3/others/{}'.format(local_title)
		# 		img_url = url
		# 		child_id = 4
		# 		child_name = '细节'
		# 		save_image('others',local_title,r11)
		# 		# save_series_child_class(child_class_id,class_id,child_id,child_name,appid)
		# 		# save_series_child(child_id,child_name,url,img_url,create_date6,create_idate6)
		# 		save_series_child_picture(picture_id,title,local_title,create_date6,create_idate6,child_class_id,url,img_url)
		# except:
		# 	print(car_name,'获取其他细节图片失败')

