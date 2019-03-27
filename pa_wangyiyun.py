import requests
from bs4 import BeautifulSoup
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

'''
爬取歌曲思路:
来源于网络，此为更改后的程序
1. 先爬取网易云某网页，取源代码，取其中的歌曲ID组
2. 请求单歌曲页面，下载歌曲
'''
def getHtml(url,headers):
	#try:
		r = requests.get(url,headers = headers)
		r.raise_for_status()
		r.encoding = 'utf-8'
		return r.text
	#except:
	#	print('爬取失败')
	#	return ''

def htmlParser(html):
	#try:
		id_list = []
		soup = BeautifulSoup(html,'html.parser')
		li = soup.select('.f-hide li a')
		for i in li:
			id_list.append(i['href'].split('=')[-1])
		return id_list
	#except:
	#	print('获得id出错')
	#	return ''

def get_name_singer(html):
	name_sig_list = []
	soup = BeautifulSoup(html,'html.parser')
	name = soup.select('.f-ff2')
	singer = soup.select('p.des.s-fc4 span a')
	name_sig_list.append(name[0].text)
	name_sig_list.append(singer[0].text)
	return name_sig_list

def getMusic(lst,nslst,headers):

		urls = []
		for id in lst:
			urls.append('http://music.163.com/song/media/outer/url?id='+id+'.mp3')
		for i in range(len(urls)):
			#try:
				# allow_redirects=False的意义为拒绝默认的301/302重定向从而可以通过
				# .headers['Location’]拿到重定向的URL
				url = requests.get(urls[i],headers = headers,allow_redirects=False).headers['Location']
				r = requests.get(url)

				if os.path.exists('./music') == False:
					os.mkdir("./music")

				#with open('./music/' + nslst[i][1].strip() + ',' + nslst[i][0].strip() + '.mp3','wb') as f:#用此行下载的歌曲是歌手加歌曲名
				with open('./music/' + nslst[i][0].strip() + '.mp3','wb') as f:
					f.write(r.content)
					print('第{}首音乐下载成功'.format(i+1))
			#except :
			#	print('第{}首音乐下载失败'.format(i+1))

def main():
	urlls = []
	name_singer_list = []
	url = 'https://music.163.com/playlist?id=2649779495'
	# url = 'https://music.163.com/#/discover/toplist?id=3778678'
	headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
	}
	# 获取网页含有歌曲ID 的源代码
	html = getHtml(url,headers)
	# 获取网页ID列表
	idlist = htmlParser(html)
	for id in idlist:
		urlls.append('https://music.163.com/song?id='+id)#原有,下载的音乐不能播放
		# 网易云歌曲一般会有一个外链，专门用于下载音乐音频的，外链 URL 如下：
		#urlls.append('http://music.163.com/song/media/outer/url?id=' + id)
	# 获取单歌曲的源代码
	for url in urlls:
		html = getHtml(url,headers)
		name_singer_list.append(get_name_singer(html))
	# print(name_singer_list)
	getMusic(idlist,name_singer_list,headers)
main()
