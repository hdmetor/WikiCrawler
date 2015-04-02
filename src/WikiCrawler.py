from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib
import urllib.request
import re
import pickle
import time
import datetime


class WikiCrawler:
    """Wikipedia Article Crawler"""
    #max number of links stored in the queue
    queue_max = 500
    root = 'http://en.wikipedia.org/wiki/'
    headers = {
        "User-Agent": "github.com/hdmetor/WikiCrawler"
    }
    def __init__(self, path):
        self.visited = self.load(path)
        self.path = path
    def crawl(self, start, max_length, add_links = True, num_links = 10):
        """
        crawl is the main worker
        it will start from \'start\' which can be either a page or a list of pages
        if \'add_links\' is set to true, then it will add the first \'num_links\' links of each page to the queue
        the crawling will stop after \'max_length\' iterations
        """
        if type(start) == str:
            if self.query(start):
                print(start, 'was already crawled')
                return
            self.to_visit = [start]
        elif type(start) == list:
            self.to_visit = start
        local_length = max_length
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
                print(max_length - local_length + 1,': crawling ',page)
                local_length-=1
                try:
                    crawl_html(page, num_links)
                except urllib.error.HTTPError:
                    print(page,' is a bad url, it will be skipped')
        print('done with crawling, saving the results')
        self.save(self.path)
    def crawl_html(page, num_links, sleep_time = 1):
        """Given a page, the function will obtain the html code of it and extract the internal links, number of tranlation and text lenght of the page, using beautifulsoup.
            Is it possible to change the max number of links saved and change the sleep time between requests, default to 1 sec """
        htmltext = urllib.request.urlopen(self.root+page, headers=headers).read()
        #be kind :)
        time.sleep(sleep_time)
        soup = BeautifulSoup(htmltext)
        all_links = self.links(soup)
        self.visited[page] = {
                                'links': all_links,
                                'languages': self.languages(soup),
                                'text_length': self.text_length(soup),
                                'time' : datetime.datetime.now()
                              }
        if add_links:
            self.to_visit = self.extend_list(self.to_visit, all_links, max = num_links)
        if (max_length - local_length ) % 100 == 0 and (max_length - local_length ) !=max_iter:
          self.save(self.path)

    # TODO
    def crawl_raw(page):
        """Exract the required informations form the Wikipedia markdown language."""
        pass

    def text_length(self,soup):
        """text_length computes the text length of an article, pass the soup as argument"""
        return len(soup.find('div', id='bodyContent').get_text())
    def languages(self, soup):
        """languages computes the number of translation of an article, pass the soup as argument"""
        langs = soup.find_all('a', lang=True)
        return [tag['lang'] for tag in langs]
    def links(self, soup):
        """links computes the number of links (internal to Wikipedia) inside on article, pass the soup as argument"""
        all_links = soup.findAll('a', {'href': wiki_links_condition})#, limit = limit)
        returned_links = []
        #just to be sure there are no duplicates links (and preserving the order!)
        for tag in all_links:
            if tag['href'][6:] in returned_links:
                pass
            else:
                returned_links.append(tag['href'][6:])
        return returned_links
    def examine_depth(page, depth):
        if depth == 0:
            pass
        #if the page was already crawled
        if page in self.visited:
            for link in self.visited['links']:
                examine_depth(link,depth - 1)
    def extend_list(self, list1, list2, max = None):
        """
        extend_list(list1, list2, max) extends list1 with element in list2 with a max of \'max\' number of elements
        \'max\' default case is None, when each elemt is added
        if list1 is bigger than the queue then the funcion returns list1
        """
        if len(list1) > self.queue_max:
            return list1
        else:
            index = 1
            for elem in list2:
                if max != None and index > max:
                    break
                else:
                    if elem not in list1:
                        list1.append(elem)
                        index+=1
            return list1
    def load(self,path):
        """load loads the data contained in a pickle file stored in \'path\'"""
        try:
            with open(path,'rb') as fp:
                return pickle.load(fp)
        #if the file dosen't exist, start with a empty dict
        except FileNotFoundError:
            return {}
    def save (self,path):
        """save saves the data contained in a pickle file stored in \'path\'"""
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
        """query checks if a page was visited or not"""
        if type(page) == str:
            return page in self.visited


def wiki_links_condition(link):
    """wiki_links_condition checks if \'link\' is link to a Wikipedia article"""
    if link:
        return link.startswith('/wiki/') and ':' not in link and not link.endswith('_(disambiguation)')
    else:
        return False



if __name__ == '__main__':
    # raw page:
    # http://en.wikipedia.org/w/index.php?title=Donald_Duck&action=raw
    start = 'Donald_Duck'
    max_iter = 100
    crawler = WikiCrawler('data/new.p')
    print ('\n\ncrawling started at ',datetime.datetime.now())
    crawler.crawl(start,max_iter, add_links = True)
    print ('\n\ncrawling finished at ',datetime.datetime.now())
    crawler.query(start)
