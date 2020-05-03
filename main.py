# import logging 
# import reddis 
import requests
import json
import re 
import os 
import redis


def  month_to_num(shortMonth):
	return{
	        'Jan' : '01',
	        'Feb' : '02',
	        'Mar' : '03',
	        'Apr' : '04',
	        'May' : '05',
	        'Jun' : '06',
	        'Jul' : '07',
	        'Aug' : '08',
	        'Sep' : '09', 
	        'Oct' : '10',
	        'Nov' : '11',
	        'Dec' : '12'
	}[shortMonth]


# def is_saved(gu,red):
# 	try:
# 		response = red.get(gu)
# 		if response is None:
# 			return False
# 		return True
# 	except Exception as e:
# 		raise e
# 		# return ? 


def main():
	url = 'http://farsi.khamenei.ir/rss'
	# url = 'https://www.varzesh3.com/rss'
	# 'description'
	needed_inf = ['title','link','guid','pubDate','category']
	dic = { i:[""] for i in needed_inf }
	all_news = {}
	try:
		response = requests.get(url)
		response.raise_for_status()
		print(response.status_code)
	except Exception as err : 
		print(err)
	else: 





		# splitting news from each other
		x = re.split("<item>|</item>",response.text)



		for i in range(0,len(x)):
			print("next!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			
			# if x[i] is news it has guid !
			if "guid" in x[i] : 
				for inf in needed_inf: 
					tmp = re.findall("<{}>[\S\s]*</{}>".format(inf,inf),x[i])
					if tmp != [] :
						tmp = tmp[0] 
						
						# delet tags from string of  each info !
						dic[inf]= tmp[tmp.index("<{}>".format(inf))+len(inf)+2: tmp.index("</{}>".format(inf))]
						# if "pubDate" in dic :
						# 	st = dic["pubDate"]
						# 	print(st)
						# 	print(st[5:7])
						# 	print(st[8:11])
						# 	print(st[12:16])


				# save information of each news as dictionary and the key is guid !
				all_news[dic["guid"]] = dic
				dic = {}
		
		# file_address ="myfile.json"
		# file = open(file_address,"w")
		# json.dump(all_news,file,indent = 6)
		# file.close
		# print(all_news)
		red = redis.Redis()


		for gu in all_news: 
			if(red.exists(gu)):
				break;


			date = all_news[gu]["pubDate"]
			# print(date)
			month = month_to_num(date[8:11])
			# print(month)
			day,year = date[5:7],date[12:16]


			
			try :
				path ="/py_report/{}/{}/{}/".format(year,month,day)
			except Exception as ex: 
				pass




			try :
				if not os.path.exists(path):
					os.makedirs(path)
			except Exception as ex : 
				pass





			try :
				file = open(path+"{}.json".format(gu),"w")
				json.dump(all_news[gu],file,indent = 6)
				file.close()

			except Exception as ex : 
				pass 

			if not red.set(gu,gu):
				print("not saved in database !!!!")

		


main()








