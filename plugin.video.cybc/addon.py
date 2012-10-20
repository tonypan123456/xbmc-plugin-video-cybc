import os
import xbmcplugin, xbmcgui, sys
import urllib2, urllib, re

# magic; id of this plugin's instance - cast to integer
_pluginName = (sys.argv[0])
_thisPlugin = int(sys.argv[1])
_connectionTimeout = 20
_header = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
#_videoCategoriesUrl = "http://www.cybc.com.cy/video-on-demand/index.php?option=com_videoflow&task=categories"
_videoCategoriesUrl = "http://www.cybc-media.com/video/index.php/video-on-demand?task=categories&layout=list"
_audioCategoriesUrl = "http://www.cybc.com.cy/audio-on-demand/index.php?option=com_videoflow&task=categories"
_cybcAudioContentServer = 'http://www.cybc.com.cy'
_cybcVideoContentServer = 'http://www.cybc-media.com'

def listMainCategories():
    
#    addDir("Video", "http://www.cybc-media.com/video/index.php/video-on-demand?task=categories&layout=list", "video", '')
    addDir("Video", _videoCategoriesUrl, "videoCategories", '')
    addDir("Audio", _audioCategoriesUrl, "audioCategories", '')
    
def listVideoCategories(url):
    try:
        print "requesting url " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        match = re.compile('<a href="(/video/index.php/video-on-demand\?task=cats&amp;cat=(.*)&amp;sl=categories&amp;layout=list)" >(.+?)</a>').findall(link)
#        match = re.compile('<a href="(/video-on-demand/index.php\?option=com_videoflow&amp;task=cats&amp;cat=(.*)&amp;layout=grid&amp;sl=categories)">(.+?)</a>').findall(link)
        
        for i in range(len(match)):
            videoCategoryUrl = _cybcVideoContentServer + match[i][0]    #?mode=videoCategoryContent&url=videoCategoryContent&categoryId=' + match[i][1]
            match[i] = (videoCategoryUrl, match[i][1], unicode(match[i][2], 'utf-8'))
        
        for url, catId, name in match:
            addDir(name, url, 'videoCategoryContent', '')
    except urllib2.URLError:
        addLink("Failed to connect to the CyBC media server", '', '', '')
    

def listVideosInCategory(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        match = re.compile('<a href="(/video/index.php/video-on-demand\?task=play&amp;id=(.*)&amp;sl=cats)">(.+?)</a>').findall(link)
#        match = re.compile('<a href="(/video-on-demand/index.php\?option=com_videoflow&amp;task=play&amp;id=(.*)&amp;sl=cats")>(.+?)</a>').findall(link)
        
        for i in range(len(match)):
            playVideoUrl = _cybcVideoContentServer + match[i][0]
            match[i] = (playVideoUrl, match[i][1], unicode(match[i][2], 'utf-8'))
    
        for url, videoId, name in match:
            addLink(name, url, 'resolveAndPlayVideo', '')
    except urllib2.URLError:
        addLink("Failed to connect to the CyBC media server", '', '', '')
   
def resolveAndPlayVideo(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
    
        match = re.compile("'file':.*'(http://www.cybc-media.com/video/videoflow/videos/.*)',").findall(link)
#        match = re.compile("'file':.*'(http://www.cybc.com.cy/video-on-demand/../videoflow/videos/.*)',").findall(link)
        
        listItem = xbmcgui.ListItem(path=str(match[0]))
        listItem.setProperty('IsPlayable', 'true')
        
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
    except urllib2.URLError:
        addLink("Failed to connect to the CyBC media server", '', '', '')

def listAudioCategories(url):
    try:
        print "requesting url " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        match = re.compile('<a href="(/audio-on-demand/index.php\?option=com_videoflow&amp;task=cats&amp;cat=(.*)&amp;layout=grid&amp;sl=categories)">(.+?)</a>').findall(link)
        
        for i in range(len(match)):
            audioCategoryUrl = _cybcAudioContentServer + match[i][0]
            match[i] = (audioCategoryUrl, match[i][1], unicode(match[i][2], 'utf-8'))
        
        for url, catId, name in match:
            addDir(name, url, 'audioCategoryContent', '')
    except urllib2.URLError:
        addLink("Failed to connect to the CyBC media server", '', '', '')

def listAudioInCategory(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        match = re.compile('<a href="(/audio-on-demand/index.php\?option=com_videoflow&amp;task=play&amp;id=(.*)&amp;sl=cats")>(.+?)</a>').findall(link)
        
        for i in range(len(match)):
            playAudioUrl = _cybcAudioContentServer + match[i][0]
            match[i] = (playAudioUrl, match[i][1], unicode(match[i][2], 'utf-8'))
    
        for url, videoId, name in match:
            addLink(name, url, 'resolveAndPlayAudio', '')
    except urllib2.URLError:
        addLink("Failed to connect to the CyBC media server", '', '', '')
 
def resolveAndPlayAudio(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', _header)
        response = urllib2.urlopen(req, timeout = _connectionTimeout)
        link=response.read()
        response.close()
        match = re.compile("'file':.*'(http://www.cybc.com.cy/audio-on-demand/videoflow/audio/.*)',").findall(link)
        
        listItem = xbmcgui.ListItem(path=(str(match[0]).replace(" ", "%20")))
        listItem.setProperty('IsPlayable', 'true')
        
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
    except urllib2.URLError:
        addLink("Failed to connect to the CyBC media server", '', '', '')
    
    
def addLink(name,url,mode,iconimage):
    u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty("IsPlayable","true");
    ok=xbmcplugin.addDirectoryItem(handle=_thisPlugin,url=u,listitem=liz,isFolder=False)
    return ok


def addDir(name,url,mode,iconimage):
    u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)#+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=_thisPlugin,url=u,listitem=liz,isFolder=True)
    return ok
        
def getparams():
    """
    Pick up parameters sent in via command line
    @return dict list of parameters
    @thanks Team XBM - I lifted this straight out of the
    shoutcast addon
    """
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

params = getparams()

try:
    url = params["url"]
    urlUnquoted = urllib.unquote_plus(url)
except:
    url = None
  
if url == None:
    #do listing
    listMainCategories()
else:
    if params["mode"] == 'videoCategories':
        listVideoCategories(urlUnquoted)
    elif params["mode"] == 'videoCategoryContent':
        listVideosInCategory(urlUnquoted)
    elif params["mode"] == 'resolveAndPlayVideo':
        resolveAndPlayVideo(urlUnquoted)
    elif params["mode"] == 'audioCategories':
        listAudioCategories(urlUnquoted)
    elif params["mode"] == 'audioCategoryContent':
        listAudioInCategory(urlUnquoted)
    elif params["mode"] == 'resolveAndPlayAudio':
        resolveAndPlayAudio(urlUnquoted)
        
xbmcplugin.endOfDirectory(_thisPlugin)        
