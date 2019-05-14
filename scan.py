#/bin/python3.6

from colored import fg,attr
import argparse
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


Version = "0.3"
EndPointUser = '/?author={id}'
Headers = {'Accept-Encoding':'gzip,deflate','User-Agent':'Mozilla/4.0 (compatible;MSIE 7.0;Windows'} 
Headers_Extract = ['Server','X-Powered-by']

parse = argparse.ArgumentParser()
parse.add_argument('-u','--url', help='Domain to Extract users', required=True)
parse.add_argument('-m','--maxusers', help='Set max users to find.', 
                    required=False, type=int,default=10)
args = parse.parse_args()

def banner():
    f = open('banner.txt','r')
    print(f.read().format(version=Version))

def validateconnection(domain):
    print("{}Validating Domain {}{}{}".format(fg('white'),attr('bold'), domain, attr('reset')))
    try:
        res = requests.get(domain)
        if res.status_code == 200:
            if len(res.headers) > 0:
                for h in Headers_Extract:
                    if h in res.headers:
                        print('{}{}{}{}:{}{}'.format(fg('blue'),
                            fg('light_cyan'),h,attr('reset'),res.headers[h],attr('reset')))
                print('\r\n')
                        
        else:
            print('{}{}The domain {} not exists.{}'.format(fg('red'), attr('bold'), 
                domain, attr('reset')))
    
        return res.status_code == 200
    except:
        print('{}{}The domain {} not exists.{}'.format(fg('red'), attr('bold'), 
                domain, attr('reset')))
        return False

            

def extractuser(text):
    o = urlparse(text)
    params = o.path.split('/')
    user = ''
    for p in range(0,len(params)):
        if params[p] == 'author':
            user = params[p+1]
    return user

def try2extractuser(text):
    soup = BeautifulSoup(text,'lxml')
    for link in soup.findAll('link'):
        href = link.get('href')
        if 'author' in href:
            return extractuser(href)

def printresult(users):
    print('{}Found Users:{}'.format(fg('yellow'), attr('reset')))
    for u in users:
        print('{}[*] {}{}'.format(fg('green'),u,attr('reset')))


def scan(domain):
    print("Looking for a Users....")
    findusers = []
    for i in range(0,args.maxusers):
        url = domain + EndPointUser.format(id=str(i))
        res = requests.get(url, headers=Headers)
        if len(res.history) > 0:
            if res.history[0].status_code == 301:
                for h in res.history[0].headers:
                    if h == 'Location':
                        user = extractuser(res.history[0].headers[h])
                        findusers.append(user)
        else:
            user = try2extractuser(res.text)
            if user is not None:
                findusers.append(user)

    printresult(findusers)
                        
                


if __name__=='__main__':
    banner()
    url = args.url
    if not url.startswith('http'):
        url = 'http://' + args.url
    
    if validateconnection(url):
        scan(url)
