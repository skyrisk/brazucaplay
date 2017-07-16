import xbmc
import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs
import tarfile
import os
import re
import sys
import subprocess
import shutil
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import os
#download_tools get it
trunkfolder="https://raw.githubusercontent.com/Shani-08/ShaniXBMCWork/master/other"
python7_apk_arm = trunkfolder + "/python7/python4A-arm.tar.gz"
python7_apk_x86 = trunkfolder + "/python7/python4A_x86.tar.gz"

addon_id = 'script.video.f4mProxy'
settings = xbmcaddon.Addon(id=addon_id)
addonpath = settings.getAddonInfo('path').decode('utf-8')
pastaperfil = xbmc.translatePath(settings.getAddonInfo('profile')).decode('utf-8')

def installPy7ForAndroid():
    if not os.path.exists(pastaperfil): xbmcvfs.mkdir(pastaperfil)
    #Hack to get xbmc app id
    xbmcfolder=xbmc.translatePath(addonpath).split("/")
    found = False
    if 1==1:#settings.getSetting('auto_appid') == 'true':
        i = 0
        for folder in xbmcfolder:
            if folder.count('.') >= 2 and folder != addon_id :
                found = True
                break
            else:
                i+=1
        if found == True:
            uid = os.getuid()
            app_id = xbmcfolder[i]
    else:
        if settings.getSetting('custom_appid') != '':
            uid = os.getuid()
            app_id = settings.getSetting('custom_appid')
            found = True

    if found == True:
        settings.setSetting('app_id',app_id)
        if "arm" in os.uname()[4]:
            python7bundle = os.path.join(pastaperfil,python7_apk_arm.split("/")[-1])
            download_tools().Downloader(python7_apk_arm,python7bundle,"downloading python7 for Android Arm","pycrypto")
        else:
            python7bundle = os.path.join(pastaperfil,python7_apk_x86.split("/")[-1])
            download_tools().Downloader(python7_apk_x86,python7bundle,"downloading python7 for Android x86","pycrypto")
        if tarfile.is_tarfile(python7bundle):
            download_tools().extract(python7bundle,pastaperfil)
            download_tools().remove(python7bundle)
        python7folder = os.path.join(pastaperfil,"python7")
        xbmc_data_path = os.path.join("/data", "data", app_id)
        if os.path.exists(xbmc_data_path) and uid == os.stat(xbmc_data_path).st_uid:
            android_binary_dir = os.path.join(xbmc_data_path, "files", app_id)
            if not os.path.exists(android_binary_dir): os.makedirs(android_binary_dir)
                android_exec_folder = os.path.join(android_binary_dir,"python7")
                if not os.path.exists(android_exec_folder): os.makedirs(android_exec_folder)
                else:
                    #clean install for android - delete old folder
                    print android_exec_folder
                    try:
                        os.system("chmod -R 777 "+android_exec_folder+"/*")
                        os.system("rm -r '"+android_exec_folder+"'")
                    except: pass
                    try: os.makedirs(android_exec_folder)
                    except: pass
                xbmc.sleep(200)
        recursive_overwrite(python7folder, android_exec_folder, ignore=None)
        pythonbin = os.path.join(android_exec_folder,"python","bin","python")
        st = os.stat(pythonbin)
        import stat
        os.chmod(pythonbin, st.st_mode | stat.S_IEXEC)
        if os.path.exists(python7folder):
        try:
            os.system("chmod -R 777 "+python7folder+"/*")
            os.system("rm -r '"+python7folder+"'")
        except: pass                
