# 抓取美桌网手机壁纸　http://www.win4000.com/
import requests
from lxml import etree
import lxml	
import pymysql 
import random
import time
import re
from datetime import datetime
import asyncio
import aiohttp
from concurrent import futures


def create_base_url():
	base_url_pool = []
	for i in range(1,6):
		creat_stars_url = 'http://www.win4000.com/mobile_2338_0_0_%d.html'%(i)
		creat_holiday_url = 'http://www.win4000.com/mobile_2339_0_0_%d.html'%(i)
		create_love_url = 'http://www.win4000.com/mobile_2343_0_0_%d.html'%(i)
		create_scenery_url = 'http://www.win4000.com/mobile_2341_0_0_%d.html'%(i)
		create_cars_url = 'http://www.win4000.com/mobile_2342_0_0_%d.html'%(i)
		base_url_pool.append(creat_stars_url)
		base_url_pool.append(creat_holiday_url)
		base_url_pool.append(create_love_url)
		base_url_pool.append(create_scenery_url)
		base_url_pool.append(create_cars_url)
	print(base_url_pool)
	return base_url_pool


async def get_url(base_url,centure_url_lilst):
	session = aiohttp.ClientSession()
	resp = await session.get(base_url,headers=headers,timeout=60)
	result = await resp.text()
	await asyncio.sleep(2)
	two_html = etree.HTML(result)
	page_url = two_html.xpath('//div[@class="list_cont Left_list_cont  Left_list_cont2"]//ul[@class="clearfix"]//li/a/@href')
	centure_url_lilst += page_url
	session.close()
	return centure_url_lilst


def get_centure_url():
	centure_url_lilst = []
	try:
		loop = asyncio.get_event_loop()
		tasks = [get_url(str(i),centure_url_lilst) for i in create_base_url()]
		loop.run_until_complete(asyncio.wait(tasks))
	except:
		print('get_centure_url错误')
	finally:
		loop.close()
		return centure_url_lilst


def create_last_url(last_url):
	start = time.time()
	try:
		for i in get_centure_url():
			if 'http' not in str(i):
				lastUrl = 'http://www.win4000.com' + str(i)
			else:
				lastUrl = str(i)
			last_url.append(lastUrl)
	except:
		print('create_last_url错误')
	finally:
		print(last_url)
		return last_url


def save_image(title,image):
	with open(title,'wb') as f:
		f.write(image.content)


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


def save_content_article(a,b,c,d,e,f,g,h,i,j): 
	sql_insert_article = """insert into content_article(article_id,appid,article_name,create_date,create_idate,url,content,imageNum,is_audit,countcollect,countlike) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
	db.ping(reconnect=True)
	cur.execute(sql_insert_article,(a,b,c,d,e,f,g,h,1,i,j))
	db.commit()


def save_content_column_article(a,b,c,d,e): 
	sql_insert_article = """insert into content_column_article(column_id,article_id,article_name,imageNum,appid) values(%s,%s,%s,%s,%s)"""
	db.ping(reconnect=True)
	cur.execute(sql_insert_article,(a,b,c,d,e))
	db.commit()


def save_content_pciture(a,b,c,d,e,f,g):
	sql_insert_picture = """insert into content_picture(title,picture_name,create_date,create_idate,url,column_id,article_id,isaudit,label) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
	db.ping(reconnect=True)
	cur.execute(sql_insert_picture,(a,b,c,d,e,f,g,1,'<img>'))
	db.commit()


def save_content_picture_compress(a,b,c,d,e,f,g,h):
	sql_insert_picture_compress = """insert into content_picture_compress(title,picture_name,create_date,create_idate,url,column_id,article_id,isaudit,count_like) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
	db.ping(reconnect=True)
	cur.execute(sql_insert_picture_compress,(a,b,c,d,e,f,g,1,h))
	db.commit()


def main():
	search_id = "select article_id from content_article order by article_id DESC limit 1"
	cur.execute(search_id)
	last_id = cur.fetchone()

	if last_id is None:
		last_id = 0
	else:
		last_id = last_id[0]
	print(last_id)
	for open_url,article_id in zip(create_last_url([]),range(last_id+1,99999)):
		try:
			print('开始')
			print(open_url)
			r3 = requests.get(open_url,headers=headers,timeout=60)
			r3.encoding='utf-8'
			thrid_html = etree.HTML(r3.text)

			appid = 15
			article_name = thrid_html.xpath('//div[@class="ptitle"]//h1//text()')[0]
			create_date = datetime.now()
			create_idate = int(str(create_date.date()).replace('-',''))
			# 内容标题
			article = thrid_html.xpath('//ul[@id="scroll"]//li//a//img')
			contents,imageNum = to_img(article)
			content = ''.join(contents)
			
			print(content)
			# class_id = 112233
			countcollect = random.randint(1,400)
			countlike = random.randint(1,1500)
			column_id = 6

			save_content_article(article_id,appid,article_name,create_date,create_idate,open_url,content,imageNum,countcollect,countlike)

			save_content_column_article(column_id,article_id,article_name,imageNum,appid)


			# 图片处理
			images_url = thrid_html.xpath('//ul[@id="scroll"]//li//a/@href')
			images_url = list(set(images_url))

			image_title = thrid_html.xpath('//ul[@id="scroll"]//li//a//img/@title')

			if not image_title:
				image_title = article_name
			else:
				image_title = image_title[0]

			if images_url:
				print('处理图片')
				for image_url,num,in zip(images_url,range(1000,100000)):

					r4 = requests.get(image_url,headers=headers,timeout=60)
					r4.encoding = 'utf-8'
					four_html = etree.HTML(r4.text)
					img_url = four_html.xpath('//div[@id="pic-meinv"]/a/img/@src')[0]

					path_time = str(time.time()).replace('.','')

					path_picture = 'App%d/'%(appid) + 'class%d/'%(column_id) + '%d_'%(article_id) + path_time 
					picture_name = '%d_'%(article_id) + path_time

					rsp_image = requests.get(img_url,headers,timeout=60)
					if 'http' in img_url:
						print(picture_name)
						save_image(picture_name,rsp_image)
					else:
						print('没有http')
						image_url = 'http://www.win4000.com' + img_url
						save_image(picture_name,rsp_image)

					save_content_pciture(image_title,picture_name,create_date,create_idate,path_picture,column_id,article_id)
					save_content_picture_compress(image_title,picture_name,create_date,create_idate,path_picture,column_id,article_id,countlike)

			else:
				print('没有image')
			time.sleep(2)

		except:
			print("="*50)
			print('有错误')
	db.close()


if __name__ == '__main__':
	start = time.time()

	# 连接数据库
	db= pymysql.connect(host="localhost",user="root",
	 	password="129426",db="appware",port=3306)
	cur = db.cursor()

	headers_list = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0']
	headers = {
		'User_Agent':random.choice(headers_list)
	}
	main()
	end = time.time()
	print('cost time:',end-start)
