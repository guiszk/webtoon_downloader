import requests
from bs4 import BeautifulSoup as bs
import sys
import os

if(len(sys.argv) != 2):
    print('python ' + sys.argv[0] + ' <url>')
    sys.exit(1)

url = sys.argv[1]
if(url.endswith('/')):
    url = url[:-1]
sname = url.split('/list')[0].split('/')[-1].replace('-', '_')
if('&page' in url):
    url = url.split('&page')[0]
lasturl = url + '&page=1000'

def getsoup(url):
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    return soup

soup = getsoup(lasturl)

allurls = []
for i in soup.findAll('a'):
    if('episode_no' in i['href']):
        if not(i['href'] in allurls):
            allurls.append(i['href'])

pagenum = ''
for i in soup.findAll('a', {'href': '#'}):
    if(i.span and not pagenum):
        if(i.span.attrs.get('class')[0] == 'on'):
            pagenum = i.span.text
pagenum = int(pagenum)

for i in range(pagenum-1, 0, -1):
    newurl = url + '&page=' + str(i)
    soup = getsoup(newurl)
    for i in soup.findAll('a'):
        if('episode_no' in i['href']):
            if not(i['href'] in allurls):
                allurls.append(i['href'])

if not(os.path.isdir(sname)):
    os.mkdir(sname)

for n, url in enumerate(allurls):
    soup = getsoup(url)
    imgid = 1
    for i in soup.findAll('img', {'class': '_images'}):
        epid = url.split('episode_no=')[1]
        epname = url.split('/')[6]
        print('Downloading episode ' + epid + ' - ' + str(imgid) + '(' + str(n+1)+ '/' + str(len(allurls)) + ')')
        cmd = 'curl --referer "' + url + '" "' + i['data-url'] + '" -o ' + sname + '/' + sname + '_' + epid + '_' + str(imgid) + '_' + epname + '.jpg'
        os.system(cmd)
        imgid += 1
