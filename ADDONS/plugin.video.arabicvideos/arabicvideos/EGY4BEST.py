# -*- coding: utf-8 -*-
from LIBRARY import *

#website0a = 'https://egy.best'
#website0a = 'https://egy1.best'
#website0a = 'https://egybest1.com'
#website0a = 'https://egybest.vip'
#website0a = 'https://egy4best.com'


headers = { 'User-Agent' : '' }

script_name = 'EGY4BEST'
menu_name='_EG4_'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url,page,text):
	LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==220: MAIN_MENU()
	elif mode==221: FILTERS_MENU(url)
	elif mode==222: TITLES(url,page)
	elif mode==223: PLAY(url)
	elif mode==229: SEARCH(text)
	return

def MAIN_MENU():
	#addDir(menu_name+'اضغط هنا لاضافة اسم دخول وكلمة السر','',125)
	#addDir(menu_name+'تحذير','',226)
	#xbmcgui.Dialog().ok(website0a, html)
	#html_blocks=re.findall('id="menu"(.*?)mainLoad',html,re.DOTALL)
	#block = html_blocks[0]
	#items=re.findall('href="(.*?)".*?i>(.*?)\n',block,re.DOTALL)
	#for url,title in items:
	#	if url!=website0a: addDir(menu_name+title,url,221)
	addDir(menu_name+'بحث في الموقع','',229)
	addDir(menu_name+'الأكثر مشاهدة',website0a+'/trending',222,'','1')
	addDir(menu_name+'الأفلام',website0a+'/movies',221)
	addDir(menu_name+'المسلسلات',website0a+'/tv',221)
	addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	html = openURL_cached(LONG_CACHE,website0a,'',headers,'','EGY4BEST-MAIN_MENU-1st')
	html_blocks=re.findall('class="ba mgb(.*?)class="tam pdb',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	for link,title in items:
		addDir(menu_name+title,link,222,'','1')
	xbmcplugin.endOfDirectory(addon_handle)
	return
	"""
	# egybest1.com
	html_blocks=re.findall('id="menu"(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	#items=re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	items=re.findall('<a href="(.*?)".*?[1/][i"]>(.*?)</a',block,re.DOTALL)
	for link,title in items:
		if 'torrent' not in link: addDir(menu_name+title,link,222)
	html_blocks=re.findall('class="card(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	for link,title in items:
		if 'torrent' not in link: addDir(menu_name+title,link,222)
	"""

def FILTERS_MENU(url):
	html = openURL_cached(LONG_CACHE,url,'',headers,'','EGY4BEST-FILTERS_MENU-1st')
	html_blocks=re.findall('id="main"(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('href="(.*?)".*?</i>(.*?)[\r\n]+',block,re.DOTALL)
	for link,title in items:
		addDir(menu_name+title,link,222,'','1')
	html_blocks=re.findall('class="sub_nav(.*?)id="movies',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('href="(.*?)".+?>(.*?)<',block,re.DOTALL)
	for link,title in items:
		if link=='#': name = title
		else:
			title = title + '  :  ' + 'فلتر ' + name
			addDir(menu_name+title,link,222,'','1')
	xbmcplugin.endOfDirectory(addon_handle)
	return

def TITLES(url,page):
	#xbmcgui.Dialog().ok(str(url), str(page))
	if '/search' in url or '?' in url: url2 = url + '&'
	else: url2 = url + '?'
	#url2 = url2 + 'output_format=json&output_mode=movies_list&page='+page
	url2 = url2 + 'page=' + page
	html = openURL_cached(REGULAR_CACHE,url2,'',headers,'','EGY4BEST-TITLES-1st')
	#name = ''
	#if '/season' in url:
	#	name = re.findall('<h1>(.*?)<',html,re.DOTALL)
	#	if name: name = escapeUNICODE(name[0]).strip(' ') + ' - '
	#	else: name = xbmc.getInfoLabel( "ListItem.Label" ) + ' - '
	if '/season' in url:
		html_blocks=re.findall('class="pda"(.*?)div',html,re.DOTALL)
		block = html_blocks[-1]
	# bring seasons
	elif '/series/' in url:
		html_blocks=re.findall('class="owl-carousel owl-carousel(.*?)div',html,re.DOTALL)
		block = html_blocks[0]
	else:
		html_blocks=re.findall('id="movies(.*?)class="footer',html,re.DOTALL)
		block = html_blocks[-1]
	items = re.findall('<a href="(.*?)".*?src="(.*?)".*?title">(.*?)<',block,re.DOTALL)
	for link,img,title in items:
		"""
		if '/series' in url and '/season' not in link: continue
		if '/season' in url and '/episode' not in link: continue
		#xbmcgui.Dialog().ok(title, str(link))
		title = name + escapeUNICODE(title).strip(' ')
		"""
		title = unescapeHTML(title)
		"""
		title = title.replace('\n','')
		link = link.replace('\/','/')
		img = img.replace('\/','/')
		if 'http' not in img: img = 'http:' + img
		#xbmcgui.Dialog().notification(img,'')
		url2 = website0a + link
		"""
		if '/movie/' in link or '/episode' in link:
			addLink(menu_name+title,link.rstrip('/'),223,img)
		else:
			addDir(menu_name+title,link,222,img,'1')
	count = len(items)
	if (count==16 and '/movies' in url) \
		or (count==16 and '/trending' in url) \
		or (count==19 and '/tv' in url):
		pagingLIST = ['/movies','/tv','/search','/trending']
		page = int(page)
		if any(value in url for value in pagingLIST):
			for n in range(0,1000,100):
				if int(page/100)*100==n:
					for i in range(n,n+100,10):
						if int(page/10)*10==i:
							for j in range(i,i+10,1):
								if not page==j and j!=0:
									addDir(menu_name+'صفحة '+str(j),url,222,'',str(j))
						elif i!=0: addDir(menu_name+'صفحة '+str(i),url,222,'',str(i))
						else: addDir(menu_name+'صفحة '+str(1),url,222,'',str(1))
				elif n!=0: addDir(menu_name+'صفحة '+str(n),url,222,'',str(n))
				else: addDir(menu_name+'صفحة '+str(1),url,222,'','1')
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(url):
	#global headers
	titleLIST,linkLIST = [],[]
	#xbmcgui.Dialog().ok(url, url[-45:])
	# https://egy4best.com/movie/فيلم-the-lion-king-2019-مترجم
	html = openURL_cached(LONG_CACHE,url,'',headers,'','EGY4BEST-PLAY-1st')
	rating = re.findall('<td>التصنيف</td>.*?">(.*?)<',html,re.DOTALL)
	if rating:
		if rating[0] in BLOCKED_VIDEOS:
			LOG_THIS('ERROR',LOGGING(script_name)+'   Adult video   URL: [ '+url+' ]')
			xbmcgui.Dialog().notification('قم بتشغيل فيديو غيره','هذا الفيديو للكبار فقط ولا يعمل هنا')
			return
	# https://egybest.vip/movie/فيلم-the-lion-king-2019-مترجم
	watchURL,downloadURL = '',''
	htmlWatch,htmlDownload = html,html
	watch_download = re.findall('show_dl api" href="(.*?)"',html,re.DOTALL)
	if watch_download:
		for link in watch_download:
			if '/watch/' in link: watchURL = link
			elif '/download/' in link: downloadURL = link
		if watchURL!='': htmlWatch = openURL_cached(LONG_CACHE,watchURL,'',headers,'','EGY4BEST-PLAY-2nd')
		if downloadURL!='': htmlDownload = openURL_cached(LONG_CACHE,downloadURL,'',headers,'','EGY4BEST-PLAY-3rd')
	# https://uploaded.egybest.download/?id=__the_lion_king_2019
	watchitem = re.findall('id="video".*?data-src="(.*?)"',htmlWatch,re.DOTALL)
	if watchitem:
		url2 = watchitem[0]#+'||MyProxyUrl=http://79.165.242.84:4145'
		if 'uploaded.egybest.download' in url2:
			html2 = openURL_cached(LONG_CACHE,url2,'',headers,'','EGY4BEST-PLAY-4th')
			watchlist = re.findall('source src="(.*?)" title="(.*?)"',html2,re.DOTALL)
			if watchlist:
				for link,quality in watchlist:
					linkLIST.append(link+'?name=egy4best__watch__mp4__'+quality)
			else:
				server = url2.split('/')[2]
				linkLIST.append(url2+'?name='+server+'__watch')
		else:
			server = url2.split('/')[2]
			linkLIST.append(url2+'?name='+server+'__watch')
	# https://inflam.cc/VLO1NNdGuy
	# https://facultybooks.org/VLO1NNdGuy
	downloadtable = re.findall('<table class="dls_table(.*?)</table>',htmlDownload,re.DOTALL)
	if downloadtable:
		downloadtable = downloadtable[0]
		downloadlist = re.findall('<td>.*?<td>(.*?)<.*?href="(.*?)"',downloadtable,re.DOTALL)
		if downloadlist:
			for quality,link in downloadlist:
				server = link.split('/')[2]
				linkLIST.append(link+'?name='+server+'__download__mp4__'+quality)
	#selection = xbmcgui.Dialog().select('اختر الفيديو المناسب:', linkLIST)
	#if selection == -1 : return
	import RESOLVERS
	RESOLVERS.PLAY(linkLIST,script_name)
	return

def SEARCH(search):
	if search=='': search = KEYBOARD()
	if search=='': return
	new_search = search.replace(' ','+')
	html = openURL_cached(SHORT_CACHE,website0a,'',headers,'','EGY4BEST-SEARCH-1st')
	token = re.findall('name="_token" value="(.*?)"',html,re.DOTALL)
	if token:
		url = website0a+'/search?_token='+token[0]+'&q='+new_search
		TITLES(url,'1')
	return


