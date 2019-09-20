import re
import urllib.request, urllib.parse, urllib.error
import random
import json
import string
from urllib.parse import quote
from bs4 import BeautifulSoup
from pprint import pprint


def google_detail(lat,lon,flag):
	key = 'my_api_key'
	url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+lat+','+lon+'&radius=2000&language=zh-TW&type=restaurant&key={key}'
	
	url = quote(url, safe = string.printable)
	url = urllib.request.urlopen(url)
	content = url.read()
	info = json.loads(content)
	# pprint(info)
	infos = info['results']
	print('---------附近推薦餐廳----------')
	if infos == []:
		print('googleapi unavailable')
		return 0
	for info in infos:
		name = info['name']
		try:
			rating = info['rating']
		except:
			rating = 0
			continue
		try:
			opening = info['opening_hours']['open_now']
		except:
			opening = 0	
			continue
		print(name)
		if opening == True:
			opening = '營業'	
		else:
			opening = '休息'
		print('	是否營業:',opening)
		print('	google評價:',rating)
	print('-------------------------------')

def printweather(doc):
	condition = doc['weather']
	condition = condition[0]['description']
	print('\n	天氣狀況：',condition)
	temp = doc['main']['temp']
	print('	溫度：',temp,'°C\n')

def weather(lat,lng):
	key = "my_api_key"
	url = f'https://api.openweathermap.org/data/2.5/forecast?APPID={key}&units=metric&lon='+str(lng)+'&lat='+str(lat)
	url = quote(url, safe = string.printable)
	url = urllib.request.urlopen(url)
	content = url.read()
	info = json.loads(content)
	info = info['list']
	day = info[0]['dt_txt']
	date = re.findall('^([0-9-]+)',day)
	time = re.findall('^[0-9-]+\s([0-9:]+)',day)
	# print(date)
	print('----------今日天氣',date[0],'----------')
	count = 0
	for look in info:
		day = look['dt_txt']
		d = re.findall('^([0-9-]+)',day)	
		t = re.findall('^[0-9-]+\s([0-9:]+)',day)
		# print(t)
		# print(d)	
		if d == date:
			print(t[0])
			printweather(look)	
		elif t[0] == '09:00:00':
			if count == 0:
				print('明日白天天氣')
				printweather(look)
				count = 1
			elif count == 2:
				print('後天白天天氣')
				printweather(look)
				count = 3
		elif t[0] == '21:00:00':
			if count == 1:
				print('明日夜晚天氣')
				printweather(look)
				count = 2
			elif count == 3:
				print('後天夜晚天氣')
				printweather(look)
				count = 4



			# pprint(look)

	# pprint(info)
	# return info
html = urllib.request.urlopen('https://www.taiwan.net.tw/')
soup = BeautifulSoup(html, 'html.parser')
print('歡迎使用台灣旅遊小幫手！')

###選地區
while True:
	bye = 0
	while True:
		region = input('選擇你想要去的地區(北部、中部、南部、東部、離島)：')
		region = region + '地區'
		try:			
			tags = soup.find_all('a', class_ = "megamenu-btn",title=region)
			tags = tags[0]
			#print(tags)#test
			break
		except:
			print('輸入錯誤')
			continue
	print(region,'：')
	tag = tags['href']#choose the needed information
	url = 'https://www.taiwan.net.tw/'+tag
	#print(url)#test

	###選擇縣市
	sub_html = urllib.request.urlopen(url)
	ssoup = BeautifulSoup(sub_html, 'html.parser')
	stags = ssoup.find_all('a', class_ = "circularbtn")
	index = 1
	r_dic = {}
	i_r = {}
	for stag in stags:	
		stitle = stag['title']
		stag = stag['href']#choose the needed information 
		r_dic[stitle] = r_dic.get(stitle,stag)
		i_r[index] = i_r.get(index,stitle)
		print('	',index,'：',stitle)
		index = index + 1
	while True:
		city = input('由上方選擇你想要去的縣市(輸入縣市前方數字即可)：')
		try:

			city = i_r[int(city)]
			city = r_dic[city]
			# print(city)
			break
		except:
			print('請輸入縣市前方數字！')
			continue



	###給景點
	url = 'https://www.taiwan.net.tw/'+ city
	# print(url)
	sub_html = urllib.request.urlopen(url)
	ssoup = BeautifulSoup(sub_html, 'html.parser')
	stags = ssoup.find_all('a', class_ = "card-link")
	dic = {}
	ii_r = {}
	c = 1 
	for stag in stags:
		stitle = stag['title']
		stag = stag['href']
		dic[stitle] = dic.get(stitle,stag)
		ii_r[c] = ii_r.get(c,stitle)
		#print (c,stitle)#test	
		c = c + 1
	c = c-1

	# print (c,' locations')#test

	###隨機給出20個景點

	while True:
		i = 1
		rnum = []
		rr = {}
		if c <20:
			r = c
		else:
			r = 20
		if c < 10:
			m = c
		else:
			m = 10
		for i in range(0,m):
		 	i = i + 1
		 	
		 	flag = 0 
		 	while flag == 0 :
		 		num = random.randint(1,c)
		 		if num in rnum:
		 			flag = 0
		 		else:
		 			flag = 1
		 	
		 	rnum.append(num)
		 	city = ii_r[num]
		 	# print(site)
		 	rr[i] = rr.get(i,num)
		 	# print(i,',num:',num,' ',city)
		 	site = dic[city]
		bye = 0
		flg = 1
		while bye == 0:
			print('推薦觀光景點：')
			
			for i in range(0,m):
				i = i +1
				num = rr[i]
				city = ii_r[num]
				print ('	',i,'：',city)

			print('選擇推薦景點得到天氣資訊及附近推薦餐廳')
			site = input('(輸入景點前方數字即可/重找其他縣市輸入100/想看其他推薦景點輸入0/結束查詢輸入bye)：')
			try:
				if site == 'bye':
					print('^_____^/掰掰！下次見')
					bye = 1
					break
				if int(site) == 100:
					bye = 3
					break
				if int(site) == 0: 
					bye = 2
					break
			
				site = rr[int(site)]
				# print(site)
				site = ii_r[site]
				# print(site)
				###case_1
			except:
				print('錯誤輸入')
				continue
			url = dic[site]
			url = 'https://www.taiwan.net.tw/'+url
			html = urllib.request.urlopen(url)
			ssoup = BeautifulSoup(html, 'html.parser')
			stags = ssoup.find_all('dt')
				
			count = 1
			for stag in stags:
				if stag.string == '經度/緯度：':
					break
				count = count +1
			stags = ssoup.find_all('dd')
			index = 1
			for stag in stags:
				if index == count:
					stag = stag.string
					# print (stag.string)
					break
				index = index +1
				 
			where = str(stag).split('/')
			# print(where[0],where[1])

			lat = where[1]
			lon = where[0]
			print('flag:',flg)
			weather(lat,lon)
			google_detail(lat,lon,flg)
			if flg == 1:
				flg = 0
			elif flg == 0:
				flg =1
			
			



		if bye == 1:
			break
		if bye == 2:
			continue
		if bye == 3:
			break
	if bye ==1:
		break
	if bye == 3:
		continue

	