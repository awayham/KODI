# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='HALACIMA'
headers = { 'User-Agent' : '' }
menu_name='_HLA_'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url,page,text):
	LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if mode==80: MENU()
	elif mode==81: ITEMS(url)
	elif mode==82: PLAY(url)
	elif mode==84: ITEMS('/category/','','newly',page)
	elif mode==85: ITEMS('/category/','','featured',page)
	elif mode==86: ITEMS('/category/','','views',page)
	elif mode==88: TERMINATED_CHANGED()
	elif mode==89: SEARCH(text)
	return

def TERMINATED_CHANGED():
	message = 'هذا الموقع تغير بالكامل ... وبحاجة الى اعادة برمجة من الصفر ... والمبرمج حاليا مشغول ويعاني من وعكة صحية ... ولهذا سوف يبقى الموقع مغلق الى ما شاء الله'
	xbmcgui.Dialog().ok('الموقع تغير بالكامل',message)

def MENU():
	addDir(menu_name+'بحث في الموقع','',89)
	addDir(menu_name+'المضاف حديثا','',84,'','0')
	addDir(menu_name+'افلام ومسلسلات مميزة','',85,'','0')
	addDir(menu_name+'الاكثر مشاهدة','',86,'','0')
	html = openURL_cached(LONG_CACHE,website0a,'',headers,'','HALACIMA-MENU-1st')
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	html_blocks = re.findall('dropdown(.*?)nav',html,re.DOTALL)
	block = html_blocks[1]
	items = re.findall('<a href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	#xbmcgui.Dialog().ok(block,str(items))
	ignoreLIST = ['مسلسلات انمي']
	for link,title in items:
		title = title.strip(' ')
		if not any(value in title for value in ignoreLIST):
			addDir(menu_name+title,link,81)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def ITEMS(url,html='',type='',page='0'):
	page = int(page)
	global headers
	if type=='':
		if html=='': html = openURL_cached(REGULAR_CACHE,url,'',headers,'','HALACIMA-ITEMS-1st')
		html_blocks = re.findall('main-content(.*?)pagination',html,re.DOTALL)
		if html_blocks: block = html_blocks[0]
		else: block = ''
	else:
		if page==0: url2 = website0a + '/ajax/getItem'
		else: url2 = website0a + '/ajax/loadMore'
		headers2 = headers
		headers2['Content-Type'] = 'application/x-www-form-urlencoded'
		payload = { 'Ajax' : '1' , 'item' : type , 'offset' : page*50 }
		data = urllib.urlencode(payload)
		block = openURL_cached(REGULAR_CACHE,url2,data,headers2,'','HALACIMA-ITEMS-2nd')
	items = re.findall('<a href="(.*?)".*?data-original="(.*?)".*?class="content">(.*?)<',block,re.DOTALL)
	allTitles,allLinks,allEpisodes,allImages = [],[],[],[]
	for link,img,title in items:
		episodeNo = '99999'
		title = title.replace('\n','')
		if 'حلقة' in title and 'موسم' not in title:
			episode = re.findall('حلقة (\d+)',title,re.DOTALL)
			if episode: episodeNo = episode[0]
		if 'الحلقة' in title and '/category/' in url and 'برامج-وتلفزة' not in url:
			episode = re.findall('(.*?) الحلقة \d+',title,re.DOTALL)
			if episode: title = episode[0]
			episode = re.findall('(.*?)/download-view-online/(.*?)-الحلقة.*?.html',link,re.DOTALL)
			if episode:
				link = episode[0][0]+'/series/'+episode[0][1]+'.html'
				link = link.replace('مشاهدة-','')
				link = link.replace('Game-of-Thrones-الموسم-الثامن','Game-of-Thrones-الموسم-8')
				link = link.replace('مسلسل-الهيبة-الجزء-الثالث','الهيبة-الموسم-3')
				link = link.replace('كلبش-الجزء-الثالث','كلبش-الجزء-3')
				#title = link.replace(episode2[0][0],'')
				title = '_MOD_'+title
		elif 'فيلم' in title and '/series/' in link and '/category/' in url:
			title = link
			title = title.replace('-',' ')
			title = title.replace('.html','')
			title = title.replace(website0a+'/series/','')
		title = title.strip(' -')
		title = title.strip(' ')
		title = unescapeHTML(title)
		if title not in allTitles:
			allTitles.append(title)
			allLinks.append(link)
			allEpisodes.append(episodeNo)
			allImages.append(img)
	z = zip(allTitles,allLinks,allEpisodes,allImages)
	#z = set(z)
	z = sorted(z, reverse=True, key=lambda key: int(key[2]))
	for title,link,episodeNo,img in z:
		if '/download-view-online/' in link: addLink(menu_name+title,link,82,img)
		else: addDir(menu_name+title,link,81,img)
	html_blocks = re.findall('pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('<li><a href="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			title = title.replace('الصفحة ','')
			addDir(menu_name+'صفحة '+title,link,81)
	if type=='lastRecent': addDir(menu_name+'صفحة المزيد','',84,'',str(page+1))
	elif type=='pin': addDir(menu_name+'صفحة المزيد','',85,'',str(page+1))
	elif type=='views': addDir(menu_name+'صفحة المزيد','',86,'',str(page+1))
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(url):
	linkLIST = []
	global headers
	html = openURL_cached(LONG_CACHE,url,'',headers,'','HALACIMA-PLAY-1st')
	html_blocks = re.findall('class="download(.*?)div',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)"',block,re.DOTALL)
	for link in items:
		if 'http' not in link: link = 'http:' + link
		linkLIST.append(link)
	url2 = url.replace('/download-view-online/','/online/')
	html = openURL_cached(LONG_CACHE,url2,'',headers,'','HALACIMA-PLAY-2nd')
	html_blocks = re.findall('artId.*?(.*?)col-sm-12',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall(' = \'(.*?)\'',block,re.DOTALL)
	artID = items[0]
	url2 = website0a + '/ajax/getVideoPlayer'
	headers2 = headers
	headers2['Content-Type'] = 'application/x-www-form-urlencoded'
	items = re.findall('getVideoPlayer\(\'(.*?)\'',block,re.DOTALL)
	threads = CustomThread(False)
	def linkFUNC():
		html = openURL_cached(LONG_CACHE,url2,data,headers2,'','HALACIMA-PLAY-3rd')
		html = html.replace('SRC=','src=')
		link = re.findall("src='(.*?)'",html,re.DOTALL)
		if 'http' not in link[0]: link[0] = 'http:' + link[0]
		return link[0]
	for server in items:
		payload = { 'Ajax' : '1' , 'art' : artID , 'server' : server }
		data = urllib.urlencode(payload)
		threads.start_new_thread(server,linkFUNC)
	threads.wait_finishing_all_threads()
	linkLIST = linkLIST + threads.resultsDICT.values()
	import RESOLVERS
	RESOLVERS.PLAY(linkLIST,script_name)
	return

def SEARCH(search):
	if search=='': search = KEYBOARD()
	if search == '': return
	#search = search.replace(' ','+')
	url = website0a + '/search.html'
	headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
	payload = { 'name' : search , 'search' : 'البحث' }
	data = urllib.urlencode(payload)
	html = openURL_cached(REGULAR_CACHE,url,data,headers,'','HALACIMA-SEARCH-1st')
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	ITEMS('/category/',html)
	#if 'art_list' in html: ITEMS('/category/',html)
	#else: xbmcgui.Dialog().ok('no results','لا توجد نتائج للبحث')
	return



