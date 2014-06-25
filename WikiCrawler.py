from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib
import urllib.request
import re
import pickle
import time
import datetime


class WikiCrawler:
    """ Wikipedia Article Crawler """
    #max number of links stored that need to be visited
    general_len = 500
    root = 'http://en.wikipedia.org/wiki/'
    def __init__(self, path):
        self.visited = self.load(path)
        self.path = path
    def crawl(self, start, length, add_links = True):
        if start in self.visited:
            print(start, 'was already crawled')
            return
        if type(start) == str:
            self.to_visit = [start]
        elif type(start) == list:
            self.to_visit = start
        local_length = length
        while local_length > 0:
            if not self.to_visit:
                print('all pages crawled, quitting')
                self.save(self.path)
                quit()
            else:    
                page = self.to_visit[0]
                self.to_visit.pop(0)
            if page in self.visited:
                print ('\t\tskipping ',page)
                pass
            else:
                print(length - local_length + 1,': crawling ',page)
                local_length-=1
                try:
                    htmltext = urllib.request.urlopen(self.root+page).read()
                    #be kind :)
                    time.sleep(1)
                    soup = BeautifulSoup(htmltext)
                    all_links = self.links(soup)
                    self.visited[page] = {'links': all_links,
                                                        'languages': self.languages(soup),
                                                        'text_length': self.text_length(soup),
                                                        'time' : datetime.datetime.now()
                                                        }
                    if add_links:
                        self.to_visit = self.extend_list(self.to_visit, all_links,10)
                    if (length - local_length ) % 100 == 0 and (length - local_length ) !=max_iter:
                      self.save(self.path)
                except urllib.error.HTTPError:
                    print(page,' is a bad url, it will be skipped')
        print('done with crawling, saving the results')     
        self.save(self.path)
    def text_length(self,soup):
        return len(soup.find('div', id='bodyContent').get_text())
    def languages(self,soup):
        langs = soup.find_all('a', lang=True)
        return [tag['lang'] for tag in langs]
    def links(self, soup):
        all_links = soup.findAll('a', {'href': wiki_links_condition})#, limit = limit)
        returned_links = []
        #just to be sure there are no duplicates links (and preserving the order!)
        for tag in all_links:
            if tag['href'][6:] in returned_links:
                pass
            else:
                returned_links.append(tag['href'][6:])
        return returned_links
    def examine_depth(page,depth):
        if depth == 0:
            pass
        #if the page was already crawled
        if page in self.visited:
            for link in self.visited['links']:
                examine_depth(link,depth - 1)
    def extend_list(self,list1,list2, max):
        if len(list1) > self.general_len:
            return list1
        else:
            index = 1
            for i in list2:
                if index > max:
                    break
                else:
                    if i not in list1:
                        list1.append(i)
                        index+=1
            return list1
    def load(self,path):
        try:
            with open(path,'rb') as fp:
                return pickle.load(fp)
        #if the file dosen't exist, start with a empty dict
        except FileNotFoundError:
            return {}
    def save (self,path):
        print('saving at ',datetime.datetime.now())
        visited_save = self.visited
        with open(path,'wb') as fp:
            pickle.dump(visited_save,fp)
    #def mongo_save(self, path, cache):
    #    pages_db.insert([{page.replace('.','[dot]'): cache[link] } for page in cache])
    #    cache = {}
    #def mongo_load(self, path):
    #    pass
    def query(self,page):
        if page in self.visited:
            print (page ,'was already crawled')
        else:
            print (page ,' wasn\'t crawled')


def wiki_links_condition(x):
    if x:
        return x.startswith('/wiki/') and ':' not in x and not x.endswith('_(disambiguation)')
    else:
        return False

if __name__ == '__main__': 
    start = 'Donald_Duck'
    max_iter = 1000
    crawler = WikiCrawler('data/data.p')
    print ('\n\ncrawling started at ',datetime.datetime.now())   
    crawler.crawl(start,max_iter, add_links = False)
    print ('\n\ncrawling finished at ',datetime.datetime.now()) 
    crawler.query(start)    