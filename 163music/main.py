#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import urllib.request
import urllib.error
import urllib.parse
import json



def get_all_hotSong():     
    url='http://music.163.com/discover/toplist?id=3778678'    
    header={  
        'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    request=urllib.request.Request(url=url, headers=header)
    html=urllib.request.urlopen(request).read().decode('utf8') 
    html=str(html) 
    pat1=r'<ul class="f-hide"><li><a href="/song\?id=\d*?">.*</a></li></ul>' 
    result=re.compile(pat1).findall(html)  
    result=result[0] 

    pat2=r'<li><a href="/song\?id=\d*?">(.*?)</a></li>'
    pat3=r'<li><a href="/song\?id=(\d*?)">.*?</a></li>' 
    hot_song_name=re.compile(pat2).findall(result) 
    hot_song_id=re.compile(pat3).findall(result)    

    return hot_song_name,hot_song_id

def get_hotComments(hot_song_name,hot_song_id):
    url='http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + hot_song_id + '?csrf_token='   #歌评url
    header={ 
   'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
   
    data={'params':'zC7fzWBKxxsm6TZ3PiRjd056g9iGHtbtc8vjTpBXshKIboaPnUyAXKze+KNi9QiEz/IieyRnZfNztp7yvTFyBXOlVQP/JdYNZw2+GRQDg7grOR2ZjroqoOU2z0TNhy+qDHKSV8ZXOnxUF93w3DA51ADDQHB0IngL+v6N8KthdVZeZBe0d3EsUFS8ZJltNRUJ','encSecKey':'4801507e42c326dfc6b50539395a4fe417594f7cf122cf3d061d1447372ba3aa804541a8ae3b3811c081eb0f2b71827850af59af411a10a1795f7a16a5189d163bc9f67b3d1907f5e6fac652f7ef66e5a1f12d6949be851fcf4f39a0c2379580a040dc53b306d5c807bf313cc0e8f39bf7d35de691c497cda1d436b808549acc'}
    postdata=urllib.parse.urlencode(data).encode('utf8')
    request=urllib.request.Request(url,headers=header,data=postdata)
    reponse=urllib.request.urlopen(request).read().decode('utf8')
    json_dict=json.loads(reponse) 
    hot_commit=json_dict['hotComments']


    num=0
    fhandle=open('./song_comments','a')
    fhandle.write(hot_song_name+':'+'\n')

    for item in hot_commit:
        num+=1
        fhandle.write(str(num)+'.'+item['content']+'\n')
    fhandle.write('\n==============================================\n\n')
    fhandle.close()




hot_song_name,hot_song_id=get_all_hotSong() 

num=0
while num < len(hot_song_name): 
    print('正在抓取第%d首歌曲热评...'%(num+1))
    get_hotComments(hot_song_name[num],hot_song_id[num])
    print('第%d首歌曲热评抓取成功'%(num+1))
    num+=1