#!/usr/bin/env python
#encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib2, urllib
import json, os

"""
global config file
"""

access_token=""
app_id = ""
defauld_home_path = ""

def fileHandle(filename):
    if defauld_home_path in filename:
        path = filename
    elif not filename.startswith("/app") and filename.startswith("/"):
        path = defauld_home_path + filename.lstrip("/")
    else:
        path = defauld_home_path + filename
    return path

def getQuota():
    """
        get quota of your space
    """
    url = "https://pcs.baidu.com/rest/2.0/pcs/quota?method=info&access_token=%s" % access_token
    fd = urllib2.urlopen(url)
    print fd.read()

def getInfo(df_name=""):
    """
        get the info of file or dir
    """
    path = fileHandle(df_name)
    url = "https://pcs.baidu.com/rest/2.0/pcs/file?method=meta&access_token="+access_token + "&path=" + path
    response = urllib2.urlopen(url)
    fd = urllib2.urlopen(url)
    return json.loads(fd.read())

def downloadFile(filename, save_dir="."):

    path = fileHandle(filename)
    of = os.path.basename(path)
    path = path.replace("/", "%2F")
    url = "https://pcs.baidu.com/rest/2.0/pcs/file?method=download&access_token=" + access_token + "&path=" + path
    response = urllib2.urlopen(url)
    with open(of, "wb") as fd:
        for line in response:
            fd.write(line)
            line.upper()
def isfile(fname):
    file_info = getInfo(fname)
    print file_info
    if file_info["list"][0]["isdir"] == 0:
        return True
    else:
        return False

def isdir(fname):
    dir_info = getInfo(fname)
    if dir_info["list"][0]["isdir"] == 1:
        return True
    else:
        return False

def downloadDir(dir_name):   
    out_dirname = os.path.basename(dir_name)
    os.mkdir(out_dirname)
    os.chdir(out_dirname)
    listdir = listDir(dir_name)
    for listinfo in listdir["list"]:
        fname = listinfo["path"]
        print "fname is", fname 
        if isfile(fname):
            print "Download ..."
            downloadFile(fname)
        elif isdir(fname):
            print fname
            print "It dir ..."
            downloadDir(fname)
        else:
            print "Na ni"
            pass
    os.chdir("..")

def uploadFile(l_filename, s_dir="/"):   #s_dir, the dir you used,not include the filename
    import urllib
    """
    upload a singal file
    """
    s_filename = s_dir + l_filename
    path = fileHandle(s_filename)
    print path
    path = path.replace("/", "%2F")

    url = "https://pcs.baidu.com/rest/2.0/pcs/file?method=upload&access_token=" + access_token + "&path=" + path
    
    cmd = "curl -X POST -k -L --form file=@" + l_filename + " \"" + url + "\""
    
    print cmd
    curl_res = os.popen(cmd)
    print curl_res.read()

    # response = urllib2.urlopen(url)
    # print response.read()

    # postDate = urllib.urlencode(http_data)
    # print url
    # req = urllib2.Request(url=url, data=postDate)
    # print req.data
    # res = urllib2.urlopen(req)
    # print res.read()

def makeDir(dirname):
    path = fileHandle(dirname)
    print path
    path = path.replace("/", "%2F")
    url = "https://pcs.baidu.com/rest/2.0/pcs/file?method=mkdir&access_token=" + access_token + "&path=" + path
    fd = urllib2.urlopen(url)


def listDir(dir_name):
    path = fileHandle(dir_name)
    url = "https://pcs.baidu.com/rest/2.0/pcs/file?method=list&access_token=" + access_token + "&path=" + path
    response = urllib2.urlopen(url)
    fd = urllib2.urlopen(url)
    return json.loads(fd.read())
    # print type(fd.read())

up_dir_file = []
def uploadDir(l_dir_name, r_path="/"):
    # r_w_dir_name = os.path.basename(l_dir_name)
    up_root = os.path.basename(l_dir_name) + "/"
    # path = r_path + r_w_dir_name
    up_dir_file.append(os.path.basename(l_dir_name))
    up_dir_name = "/" + "/".join(up_dir_file)
    print "the making dir is", up_dir_name
    makeDir(up_dir_name)
    l_filelist = os.listdir(l_dir_name)
    os.chdir(l_dir_name)
    for l_f in l_filelist:
        if os.path.isdir(l_f):
            # up_dir_file.append(l_f)
            uploadDir(l_f)
        else:
            print "file upload"                                             #is a file
            up_path = "/" + "/".join(up_dir_file) + "/"
            local_name = l_f
            print l_f, up_path
            uploadFile(local_name, up_path)
    up_dir_file.pop(-1)
    os.chdir("..")

def download():
    pass

# getQuota()

# makeDir("/a")
# uploadFile("books")
# listDir("/")
# downloadFile("/apps/books_everywhere/music/2.png")
# uploadFile("a/aa.py")
# downloadDir("music")
# isfile("/apps/books_everywhere/music/2.png")
# makeDir("aaa")
uploadDir("book")
