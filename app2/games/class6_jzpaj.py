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
import imghdr
from aiohttp import TCPConnector

def create_base_url():
	
	base_url_pool = []
	for i in range(1,25):
		creat_url = 'https://shouyou.3dmgame.com/zt/24643_gl_all_%d'%(i)
		base_url_pool.append(creat_url)
	return base_url_pool


async def get_url(base_url,centure_url_lilst):
	session = aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False))
	resp = await session.get(base_url,headers=headers,timeout=60)
	result = await resp.text()
	await asyncio.sleep(2)
	two_html = etree.HTML(result)
	page_url = two_html.xpath('//div[@class="info"]//li/span/a/@href')
	centure_url_lilst += page_url
	session.close()
	return centure_url_lilst


def get_centure_url():
	centure_url_lilst = []
	try:
		loop = asyncio.get_event_loop()
		tasks = [get_url(str(i),centure_url_lilst) for i in create_base_url()]
		loop.run_until_complete(asyncio.wait(tasks))
		# loop.close()
		# return centure_url_lilst
	except:
		print('get_centure_url错误')
	finally:
		return centure_url_lilst


def create_last_url(last_url):
	start = time.time()
	try:
		for i in get_centure_url():
			if 'http' not in str(i):
				lastUrl = 'https://shouyou.3dmgame.com' + str(i)
			else:
				lastUrl = str(i)
			last_url.append(lastUrl)
	except:
		print('create_last_url错误')
	finally:
		return last_url


# def save_image(title,image):
# 	with open(title,'wb') as f:
# 		f.write(image.content)

async def save_images(url,title):
	session = aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False))
	response = await session.get(url,headers=headers)
	content = await response.content.read()
	with open(title,'wb') as f:
		f.write(content)


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
			r3 = requests.get(open_url,headers=headers,timeout=60,verify=False)
			r3.encoding='utf-8'
			thrid_html = etree.HTML(r3.text)

			appid = 2
			article_name = thrid_html.xpath('//div[@class=" news_warp_top"]/h1/text()')[0]
			create_date = datetime.now()
			create_idate = int(str(create_date.date()).replace('-',''))
			# 内容标题

			article = thrid_html.xpath('//div[@class="news_warp_center"]//p//text() | //div[@class="news_warp_center"]//img')
			if article:
				contents,imageNum = to_img(article)
				content = ''.join(contents)
				# class_id = 112233
				print(content)
				countcollect = random.randint(1,400)
				countlike = random.randint(1,1500)

				column_id = 2

				save_content_article(article_id,appid,article_name,create_date,create_idate,open_url,content,imageNum,countcollect,countlike)

				save_content_column_article(column_id,article_id,article_name,imageNum,appid)


				# 图片处理
				images_url = thrid_html.xpath('//div[@class="news_warp_center"]//img/@src')
				images_url = list(set(images_url))

				image_title = thrid_html.xpath('//div[@class="news_warp_center"]//img/@title')

				if not image_title:
					image_title = article_name
				else:
					image_title = image_title[0]

				if images_url:
					print('处理图片')
					tasks = []
					loop = asyncio.get_event_loop()
					for image_url in images_url:
						image_url = str(image_url)

						if 'http' in image_url:
							pass
						else:
							image_url = 'https://shouyou.3dmgame.com' + image_url
						r4 = requests.get(image_url,headers=headers,timeout=120,verify=False)
						print(r4.status_code)
						if r4.status_code == 200:
							extention = imghdr.what('',r4.content)
							path_time = str(time.time()).replace('.','')
							
							picture_name = '%d_'%(article_id) + path_time + '.' + extention
							path_picture = '/App%d/'%(appid) + 'class%d/'%(column_id) + picture_name
							print(picture_name)

							if image_url == images_url[0]:
								save_content_picture_compress(image_title,picture_name,create_date,create_idate,path_picture,column_id,article_id,countlike)
							save_content_pciture(image_title,picture_name,create_date,create_idate,path_picture,column_id,article_id)
							task = asyncio.ensure_future(save_images(image_url,picture_name))
							tasks.append(task)
						else:
							print('*********************图片错误***************')
							article_delete = 'delete from content_article where article_id=%d'%(article_id)
							cur.execute(article_delete)
							compress_delete = 'delete from content_picture_compress where article_id=%d'%(article_id)
							cur.execute(compress_delete)
							db.commit()
							print('++++++++++++++++++数据删除成功++++++++++++++++++++')
					loop.run_until_complete(asyncio.wait(tasks))

					
				else:
					print('没有image')
					article_delete = 'delete from content_article where article_id=%d'%(article_id)
					cur.execute(article_delete)
					db.commit()
					print('!!!!!!!!!!!!!!!!!!数据删除成功!!!!!!!!!!!!!!!!!!!')
		
			else:
				print('====================没有article====================')
		except:
			print("="*50)
			print('有错误')
			article_delete = 'delete from content_article where article_id=%d'%(article_id)
			cur.execute(article_delete)
			compress_delete = 'delete from content_picture_compress where article_id=%d'%(article_id)
			cur.execute(compress_delete)
			db.commit()
			print('OOOOOOOOOOOOOOPPPPPPPPP数据删除成功OOOOOOOOOOOOOOOOOPPPPPPPP')
		

			time.sleep(2)
	loop.close()
	db.close()


if __name__ == '__main__':
	start = time.time()

	# 连接数据库
	db= pymysql.connect(host="localhost",user="root",
	 	password="129426",db="appware",port=3306)
	cur = db.cursor()

	url = 'http://news.yule.com.cn/yingshi/'
	headers_list = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0']
	headers = {
		'User_Agent':random.choice(headers_list)
	}

	requests.packages.urllib3.disable_warnings()
	main()
	end = time.time()
	print('cost time:',end-start)