import os
import sys
import argparse, urllib, os, requests
from concurrent.futures import ProcessPoolExecutor,as_completed

from tqdm import tqdm
#%%
# website = 'https://www.unsplash.com'
# session = requests.Sesson()
# search = 'face'
# base_url = website + '/napi/search/photos?query={0}&xp=&per_page=20&'.format(search)
# response = session.get(base_url)
# urls = []
# if response.status_code == 200:
#     results = response.json()['results']
#     urls = urls+[(url['id'],url['urls']['raw']) for url in results]
# urllib.request.urlretrieve(urls[0][1],'./'+urls[0][0]+'.jpg')
#%%
class _unsplash(object):
    def __init__(self):
        self.website = "https://www.unsplash.com"
        self.session = requests.Session()
    def __call__(self,search,pages=None):
        base_url   = self.website+"/napi/search/photos?query    {0}&xp=&per_page=20&".format(search)
        if not pages:
            pages      = self.session.get(base_url).json()['total_pages']
        urls=[]
        for page in tqdm(range(1,pages+5),desc = "Downloading image URLs"):
            search_url  = self.website+"/napi/search/photos?query={0}&xp=&per_page=20&page={1}".format(search,page)
            response    = self.session.get(search_url)
            if response.status_code == 200 :
                results = response.json()['results']
                urls    = urls+[(url['id'],url['urls']['raw']) for url in results]
        return list(set(urls))
unsplash = _unsplash()

class _download_imgs(object):
    def __init__(self,output_dir,query):
        self.query     = query
        self.directory = output_dir+'/'+query
        if not os.path.isdir(self.directory) : os.makedirs(self.directory)
    def __call__(self,urls):
        with ProcessPoolExecutor() as pool:
            downloads = [pool.submit(urllib.request.urlretrieve,url[1],self.directory+'/'+url[0]+'.jpg') for url in urls]
            for download in tqdm(as_completed(downloads),total=len(downloads),desc='Downloading '+self.query+" images...."):
                pass

class _scrape(object):
    def __call__(self,args):
        if args[0].lower() == 'unsplash' : urls = unsplash(args[1].lower(), args[3])
        download_imgs     = _download_imgs(args[2],args[1].lower())
        download_imgs(urls)
scrape=_scrape()
#%%
# if __name__=='__main__':
#     parser = argparse.ArgumentParser(description='Web Scraping')
#     parser.add_argument('-w', default='unsplash',choices = ['unsplash'], metavar = 'website', required = False, type = str,
#                         help = 'name of the website that you want to scrape data from, example: unsplash')
#     parser.add_argument('-q', metavar = 'query', required = True, type = str,
#                         help = 'search term for query, example: mushroom')
#     parser.add_argument('-o', metavar = 'output directory', required = True, type = str,
#                         help = 'Path to the folder where you want the data to be stored, the directory will be created if not present')
#     parser.add_argument('-p', metavar = 'no of pages', type = int, help = 'Number of pages to scrape')
#
#     args = parser.parse_args()
#     scrape(args)

download_img_path = os.path.join(os.getcwd(), '2. data', '1. unsplash')
if not os.path.exists(download_img_path):
    os.mkdir(download_img_path)

keyword = 'house interior'
noofpages = 2

args = ['unsplash', keyword, download_img_path, noofpages]
scrape(args)
