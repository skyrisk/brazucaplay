import xbmc, xbmcgui, xbmcaddon, xbmcplugin, re
import urllib, urllib2
import re, string
import threading
import os
import base64
#from t0mm0.common.addon import Addon
#from t0mm0.common.net import Net
import urlparse
import xbmcplugin
import cookielib

__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.f4mTester'
selfAddon = xbmcaddon.Addon(id=addon_id)

#addon = Addon('plugin.video.f4mTester', sys.argv)
#net = Net()

mode =None
play=False

#play = addon.queries.get('play', None)
paramstring=sys.argv[2]
#url = addon.queries.get('playurl', None)
print paramstring
name=''
proxy_string=None
proxy_use_chunks=True
auth_string=''
streamtype='HDS'
setResolved=False
if paramstring:
    paramstring="".join(paramstring[1:])
    params=urlparse.parse_qs(paramstring)
    url = params['url'][0]
    try:
        name = params['name'][0]
    except:pass

    try:
        proxy_string = params['proxy'][0]
    except:pass
    try:
        auth_string = params['auth'][0]
    except:pass
    print 'auth_string',auth_string
    try:
        streamtype = params['streamtype'][0]
    except:pass
    print 'streamtype',streamtype

    

    swf=None
    try:
        swf = params['swf'][0]
    except:pass

    callbackpath=""
    try:
        callbackpath = params['callbackpath'][0]
    except:pass

    iconImage=""
    try:
        iconImage = params['iconImage'][0]
    except:pass    
 
    callbackparam=""
    try:
        callbackparam = params['callbackparam'][0]
    except:pass
    
    
    try:
        proxy_use_chunks_temp = params['proxy_for_chunks'][0]
        import json
        proxy_use_chunks=json.loads(proxy_use_chunks_temp)
    except:pass
    
    simpleDownloader=False
    try:
        simpleDownloader_temp = params['simpledownloader'][0]
        import json
        simpleDownloader=json.loads(simpleDownloader_temp)
    except:pass
	
	
    mode='play'

    try:    
        mode =  params['mode'][0]
    except: pass
    maxbitrate=0
    try:
        maxbitrate =  int(params['maxbitrate'][0])
    except: pass
    play=True

    try:
        setResolved = params['setresolved'][0]
        import json
        setResolved=json.loads(setResolved)
    except:setResolved=False
    
def playF4mLink(url,name,proxy=None,use_proxy_for_chunks=False,auth_string=None,streamtype='HDS',setResolved=False,swf="", callbackpath="", callbackparam="",iconImage=""):
    from F4mProxy import f4mProxyHelper
    player=f4mProxyHelper()
    #progress = xbmcgui.DialogProgress()
    #progress.create('Starting local proxy')

    if setResolved:
        urltoplay,item=player.playF4mLink(url, name, proxy, use_proxy_for_chunks,maxbitrate,simpleDownloader,auth_string,streamtype,setResolved,swf,callbackpath, callbackparam,iconImage)
        item.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

    else:
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
        player.playF4mLink(url, name, proxy, use_proxy_for_chunks,maxbitrate,simpleDownloader,auth_string,streamtype,setResolved,swf,callbackpath, callbackparam,iconImage)
    
    return   
    
def getUrl(url, cookieJar=None,post=None,referer=None,isJsonPost=False, acceptsession=None):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if isJsonPost:
        req.add_header('Content-Type','application/json')
    if acceptsession:
        req.add_header('Accept-Session',acceptsession)
        
    if referer:
        req.add_header('Referer',referer)
    response = opener.open(req,post,timeout=30)
    link=response.read()
    response.close()
    return link;

def getBBCUrl(urlToFetch):
    urlsel=''
    try:
        text=getUrl(urlToFetch)
        bitRate="1500"
        overrideBitrate=selfAddon.getSetting( "bbcBitRateMax" )
        if overrideBitrate<>"": bitRate=overrideBitrate
        bitRate=int(bitRate)
        regstring='href="(.*?)" bitrate="(.*?)"'
        birates=re.findall(regstring, text)
        birates=[(int(j),f) for f,j in birates]
        birates=sorted(birates, key=lambda f: f[0])
        
        for r, url in birates:
            if r<=bitRate:
                ratesel, urlsel=r, url 
            else:
                break
        if urlsel=='': urlsel=birates[1]
        print 'xxxxxxxxx',ratesel, urlsel
    except: pass
    return urlsel
    
    
def GUIEditExportName(name):

    exit = True 
    while (exit):
          kb = xbmc.Keyboard('default', 'heading', True)
          kb.setDefault(name)
          kb.setHeading('Enter Url')
          kb.setHiddenInput(False)
          kb.doModal()
          if (kb.isConfirmed()):
              name  = kb.getText()
              #name_correct = name_confirmed.count(' ')
              #if (name_correct):
              #   GUIInfo(2,__language__(33224)) 
              #else: 
              #     name = name_confirmed
              #     exit = False
          #else:
          #    GUIInfo(2,__language__(33225)) 
          exit = False
    return(name)
    
if mode ==None:
    bbcsname='http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hds/uk/pc/ak/'
    videos=[[getBBCUrl('%sbbc_one_hd.f4m'%bbcsname) +'|Referer=http://www.bbc.co.uk/iplayer/live/bbcone&X-Requested-With=ShockwaveFlash/18.0.0.160','bbc1 (uk)','http://www.parker1.co.uk/myth/icons/tv/bbc1.png',0,'',False],
    [getBBCUrl('%sbbc_two_hd.f4m'%bbcsname)+'|Referer=http://www.bbc.co.uk/iplayer/live/bbctwo&X-Requested-With=ShockwaveFlash/18.0.0.160','bbc2 (uk)','http://www.parker1.co.uk/myth/icons/tv/bbc2.png',0,'',False],
    [getBBCUrl('%sbbc_three_hd.f4m'%bbcsname)+'|Referer=http://www.bbc.co.uk/iplayer/live/bbctwo&X-Requested-With=ShockwaveFlash/18.0.0.160','bbc3 (uk)','http://www.parker1.co.uk/myth/icons/tv/bbc3.png',0,'',False],
    [getBBCUrl('%sbbc_four_hd.f4m'%bbcsname)+'|Referer=http://www.bbc.co.uk/iplayer/live/bbctwo&X-Requested-With=ShockwaveFlash/18.0.0.160','bbc4 (uk)','http://www.parker1.co.uk/myth/icons/tv/bbc4.png',0,'',False],
    [getBBCUrl('http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hds/uk/pc/llnw/bbc_news24.f4m')+'|Referer=http://www.bbc.co.uk/iplayer/live/bbctwo&X-Requested-With=ShockwaveFlash/18.0.0.160','bbc news (uk)','http://www.parker1.co.uk/myth/icons/tv/bbcnews.png',0,'',False],
    [getBBCUrl('http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hds/uk/pc/llnw/bbc_parliament.f4m')+'|Referer=http://www.bbc.co.uk/iplayer/live/bbctwo&X-Requested-With=ShockwaveFlash/18.0.0.160','bbc parliment (uk)','',0,'',False],
    #    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/cbbc/cbbc_1500.f4m','cbbc (uk) 1500kbps','',0,'',False],
#    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/cbeebies/cbeebies_1500.f4m','cbeebeies (uk) 1500kbps','',0,'',False],
#    ['http://vs-hds-uk-live.edgesuite.net/pool_1/live/bbc_parliament/bbc_parliament.isml/bbc_parliament-audio_2%3d96000-video%3d1374000.f4m|Referer=http://www.bbc.co.uk/iplayer/live/bbcparliament&X-Requested-With=ShockwaveFlash/18.0.0.160','bbc parliment (uk) 1500kbps','',0,'',False],
#    ['http://vs-hds-uk-live.bbcfmt.vo.llnwd.net/pool_5/live/bbc_news_channel_hd/bbc_news_channel_hd.isml/bbc_news_channel_hd-audio_2%3d96000-video%3d1374000.f4m|Referer=http://www.bbc.co.uk/iplayer/live/bbcnews&X-Requested-With=ShockwaveFlash/18.0.0.160','bbc news (uk) 1500kbps','',0,'',False],
#    ['http://vs-hds-uk-live.bbcfmt.vo.llnwd.net/pool_5/live/bbc_one_london/bbc_one_london.isml/bbc_one_london-audio_2%3d96000-video%3d1374000.f4m|Referer=http://www.bbc.co.uk/iplayer/live/bbcone&X-Requested-With=ShockwaveFlash/18.0.0.160&X-Forwarded-For=212.58.241.131','bbc1 (outside uk) 1500kbps','http://www.parker1.co.uk/myth/icons/tv/bbc1.png',0,'',False],
#    ['http://vs-hds-uk-live.bbcfmt.vo.llnwd.net/pool_5/live/bbc_two_hd/bbc_two_hd.isml/bbc_two_hd-audio_2%3d96000-video%3d1374000.f4m|Referer=http://www.bbc.co.uk/iplayer/live/bbctwo&X-Requested-With=ShockwaveFlash/18.0.0.160','bbc2 (outside uk) 1500kbps','http://www.parker1.co.uk/myth/icons/tv/bbc2.png',0,'',False],
#    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc3/bbc3_1500.f4m|X-Forwarded-For=212.58.241.131','bbc3 (outside uk) 1500kbps [link not valid]','',0,'',False],
#    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc4/bbc4_1500.f4m|X-Forwarded-For=212.58.241.131','bbc4 (outside uk) 1500kbps [link not valid]','',0,'',False],
#    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/cbbc/cbbc_1500.f4m|X-Forwarded-For=212.58.241.131','cbbc (outside uk) 1500kbps','',0,'',False],
#    ['http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/cbeebies/cbeebies_1500.f4m|X-Forwarded-For=212.58.241.131','cbeebeies (outside uk) 1500kbps','',0,'',False],
#    ['http://vs-hds-uk-live.edgesuite.net/pool_1/live/bbc_parliament/bbc_parliament.isml/bbc_parliament-audio_2%3d96000-video%3d1374000.f4m|Referer=http://www.bbc.co.uk/iplayer/live/bbcparliament&X-Requested-With=ShockwaveFlash/18.0.0.160|X-Forwarded-For=212.58.241.131','bbc parliment (outside uk) 1500kbps','',0,'',False],
#    ['http://vs-hds-uk-live.bbcfmt.vo.llnwd.net/pool_5/live/bbc_news_channel_hd/bbc_news_channel_hd.isml/bbc_news_channel_hd-audio_2%3d96000-video%3d1374000.f4m|Referer=http://www.bbc.co.uk/iplayer/live/bbcnews&X-Requested-With=ShockwaveFlash/18.0.0.160&X-Forwarded-For=212.58.241.131','bbc news (outside uk) 1500kbps','',0,'',False],
    ['http://nhkworld-hds-live1.hds1.fmslive.stream.ne.jp/hds-live/nhkworld-hds-live1/_definst_/livestream/nhkworld-live-128.f4m','nhk 128','',0,'',False],
    ['http://nhkworld-hds-live1.hds1.fmslive.stream.ne.jp/hds-live/nhkworld-hds-live1/_definst_/livestream/nhkworld-live-256.f4m','nhk 256','',0,'',False],
    ['http://nhkworld-hds-live1.hds1.fmslive.stream.ne.jp/hds-live/nhkworld-hds-live1/_definst_/livestream/nhkworld-live-512.f4m','nhk 512','',0,'',False],
    ['http://77.245.150.95/hds-live/livepkgr/_definst_/liveevent/livestream.f4m','Turkish','',0,'',False],
    ['http://88.157.194.246/live/ramdisk/zrtp1/HDS/zrtp1.f4m','j0anita','',0,'',False],
    ['http://ak.live.cntv.cn/z/cctv9_1@139238/manifest.f4m?hdcore=2.11.3&g=OUVOVEOVETYH','cntv.cn','',0,'',False],
    ['http://mlghds-lh.akamaihd.net/z/mlg17_1@167001/manifest.f4m?hdcore=2.11.3&g=TOFRPVFGXLFS','alibaba','',0,'',False],
    ['http://peer-stream.com/api/get_manifest.f4m?groupspec=G:0101010c050e6f72663200','streamtivi.com','',0,'',False],
    ['http://164.100.31.234/hds-live/livepkgr/_definst_/rstvlive.f4m','Rajya Sabha TV','',0,'',False],
    ['http://fmssv1.merep.com/hds-live/livepkgr/_definst_/liveevent/livestream.f4m?blnpc20130909042035_1061880273','media center','',0,'',False],
    ['http://fms01.stream.internetone.it/hds-live/livepkgr/_definst_/8fm/8fm1.f4m','Italy otto 8 FMTV','',0,'',False],
    ['http://88.150.239.241/hds-live/livepkgr/_definst_/liveevent/livestream.f4m','Son Araba','',0,'',False],
    ['http://202.162.123.172/hds-live/livepkgr/_definst_/liveevent/livestream4.f4m','Chine Live event 4','',0,'',False],
    ['http://zb.wyol.com.cn/hds-live/livepkgr/_definst_/wslhevent/hls_pindao_1_350.f4m','CCTV 1 China','',0,'',False],
    ['http://zb.zghhzx.net/hds-live/livepkgr/_definst_/wslhevent/hls_pindao_1_350.f4m','CCTV13 China','',0,'',False],
    ['http://zb.sygd.tv/hds-live/livepkgr/_definst_/wslhevent/hls_pindao_1_350.f4m','SYGD TV china','',0,'',False],
    ['http://zb.pudongtv.cn/hds-live/livepkgr/_definst_/wslhevent/hls_pindao_1_500.f4m','Pudong TV China','',0,'',False],
    ['http://88.150.239.241/hds-live/livepkgr/_definst_/liveevent/livestream.f4m','AKS TV Turkey','',0,'',False],
    ['http://fms.quadrant.uk.com/hds-live/livepkgr/_definst_/liveevent/livestream.f4m','Quadrant live streams UK','',0,'',False],
    ['http://cdn3.1internet.tv/hds-live11/livepkgr/_definst_/1tv-hd.f4m','1 HD cdn1 Russia','',0,'',False],
    ['http://cdn2.1internet.tv/hds-live/livepkgr/_definst_/1tv.f4m','1 HD cdn2 Russia','',0,'',False],
    ['http://193.232.151.135/hds-live-not-protected/livepkgr/_1099_/1099/1099-70.f4m','ndtv plus - proxy needed','',0,'',False],
    ['http://bbcwshdlive01-lh.akamaihd.net/z/atv_1@61433/manifest.f4m?hdcore=2.11.3','BBC Arabic','',0,'',False],
    ['http://skaihd-f.akamaihd.net/z/advert/ORAL_B_SHAKIRA_20-SKAI.mp4/manifest.f4m?hdcore=2.6.8&g=OGEJOEGNJICP','Greek Oral B advert','',0,'',False],
    ['http://srgssr_uni_11_ww-lh.akamaihd.net/z/enc11uni_ww@112996/manifest.f4m?g=XTJVOORDBMQF&hdcore=2.11.3','RTS Swiss a proxy needed?','',0,'',False],
    ['http://ccr.cim-jitp.top.comcast.net/cimomg04/OPUS/83/162/119271491507/1389989008837/119271491507_1389986611184_1850000_4.f4m','aliakrep DRM not working','',0,'',False],
    ['http://stream1-prod.spectar.tv:1935/mrt-edge/_definst_/mrt3/smil:all-streams.isml/manifest.f4m','mrt3/all-streams.isml','',0,'',False],        
    ['http://hdv.gamespotcdn.net/z/d5/2013/10/16/Gameplay_GettingRevengeinGTAOnline_101613_,600,1000,1800,3200,4000,.mp4.csmil/manifest.f4m?hdcore=2.10.3&g=JNMDDRCQSDCH','Recorded..Getting Revenge in GTA maxbitrate 2000','',2006,'',False],        
    ['http://hdv.gamespotcdn.net/z/d5/2013/10/16/Gameplay_GettingRevengeinGTAOnline_101613_,600,1000,1800,3200,4000,.mp4.csmil/manifest.f4m?hdcore=2.10.3&g=JNMDDRCQSDCH','Recorded..Getting Revenge in GTA maxbitrate Highest','',0,'',False],        
    ['http://hdv.gamespotcdn.net/z/d5/2014/04/24/GSNews_Apr24_20140424a_,600,1000,1800,3200,4000,.mp4.csmil/manifest.f4m?hdcore=2.10.3&g=KUVLMGTKPJFF','Recorded..Gamespot news highest bitrate','',0,'',False],        
    ['http://hdv.gamespotcdn.net/z/d5/2014/04/24/GSNews_Apr24_20140424a_,600,.mp4.csmil/manifest.f4m?hdcore=2.10.3&g=KUVLMGTKPJFF','Recorded..Gamespot news 600 bitrate','',0,'',False],        
    ['http://202.125.131.170:1935/pitelevision/smil:geokahani.smil/manifest.f4m','Pitelevision geo kahani','',0,'',False], 
    ['http://stream.flowplayer.org/flowplayer-700.flv','TESTING not F4M','',0,'',False], 
    ['http://hlscache.fptplay.net.vn/live/htvcmovieHD_2500.stream/manifest.f4m|Referer=http://play.fpt.vn/static/mediaplayer/FPlayer.swf','Viet 2500bitrate','',0,'',False],
    ['http://hlscache.fptplay.net.vn/live/onetv_1000.stream/manifest.f4m|Referer=http://play.fpt.vn/static/mediaplayer/FPlayer.swf','Viet 1000bitrate','',0,'',False], 
    ['http://88.157.194.246/live/ramdisk/zsic/HDS/zviseu.f4m','Sic http://viseu.es.tl/','',0,'',False], 
    ['http://www.rte.ie/manifests/rte1.f4m','Rte.ie multi nested manifests','',0,'',False], 
	['http://olystreameast.nbcolympics.com/vod/157717c8-9c74-4fd1-ab1a-7daca5246324/geo1-lucas-oil-pro-motocross0531120959-ua.ism/manifest(format=f4m-f4f).f4m','NBc olypics','',900,'108.163.254.214:7808',False], 
	['http://olystreameast.nbcolympics.com/vod/31883e54-e85b-4551-a24a-46accc4a9d49/nbc-sports-live-extra0601123118-ua.ism/manifest(format=f4m-f4f,filtername=vodcut).f4m','NBc extra olypics','',900,'108.163.254.214:7808',False], 

    ['http://77.245.150.95/hds-live/livepkgr/_definst_/liveevent/livestream.f4m','something else','',0,'',False]]
     

    #['http://dummy','Custom']]
    #print videos

    if 1==2: #disable it as these links are not working, not sure why
        req = urllib2.Request('http://www.gzcbn.tv/app/?app=ios&controller=cmsapi&action=pindao')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        ##	print link

        s='title\":\"(.*?)\",\"stream\":\"(.*?)\"'
        #    
        match=re.compile(s).findall(link)
        i=0
        for i in range(len(match)):
            match[i]= (match[i][1].replace('\\/','/'),match[i][0])


        videos+=match #disabled for time being as these are not working
    #print videos
    for (file_link,name,imgurl,maxbitrate,proxy,usechunks) in videos:
        liz=xbmcgui.ListItem(name,iconImage=imgurl, thumbnailImage=imgurl)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        #liz.setProperty("IsPlayable","true")
        u = sys.argv[0] + "?" + urllib.urlencode({'url': file_link,'mode':'play','name':name,'maxbitrate':maxbitrate,'proxy':proxy,'proxy_for_chunks':usechunks}) 
        print u
        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False, )


   
    
elif mode == "play":
    print 'PLAying ',mode,url,setResolved
    
    if not name in ['Custom','TESTING not F4M'] :
        playF4mLink(url,name, proxy_string, proxy_use_chunks,auth_string,streamtype,setResolved,swf , callbackpath, callbackparam,iconImage)
    else:
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=url )
        xbmc.Player().play( url,listitem)
    
        #newUrl=GUIEditExportName('')
        #if not newUrl=='':
        #    playF4mLink(newUrl,name)




if not play:
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
    
 