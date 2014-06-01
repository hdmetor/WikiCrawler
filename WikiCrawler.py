from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib
import urllib.request
import re
import pickle
import time


class WikiCrawler:
  """ Wikipedia Article Crawler """
  #max number of links stored that need to be visited
  general_len = 500
  root = 'http://en.wikipedia.org/wiki/'
  def __init__(self, start, length, path):
    self.visited = self.load(path)
    self.to_visit = [start]
    self.path = path
    if start in self.visited:
      print(start, 'was already crawled... quitting')
      quit()
    self.length = length
    #self.path = path


  def crawl(self):
    local_length = self.length
    while local_length > 0:
      if not self.to_visit:
        print('all pages crawled, quitting')
        quit()
      else:  
        page = self.to_visit[0]
        self.to_visit.pop(0)
      if page in self.visited:
        print ('skipping ',page)
        pass
      else:
        print(self.length - local_length + 1,': crawling ',page)
        local_length-=1
        try:
          htmltext = urllib.request.urlopen(self.root+page).read()
          time.sleep(1)
          soup = BeautifulSoup(htmltext)
          all_links = self.links(soup)
          self.visited[page] = {'links': all_links,
                            'lang': self.languages(soup),
                            'text': self.text_lenght(soup)
                            }
          self.to_visit = self.extend_list(self.to_visit, all_links,10)
        except urllib.error.HTTPError:
          print(page,' is a bad url, it will be skipped')
    print('done with crawling, saving the results')   
    self.save(self.path)
  def text_lenght(self,soup):
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
    print('saving')
    visited_save = self.visited
    with open(path,'wb') as fp:
      pickle.dump(visited_save,fp)

def wiki_links_condition(x):
  if x:
        return x.startswith('/wiki/') and ':' not in x and not x.endswith('_(disambiguation)')
  else:
        return False

if __name__ == '__main__':
  start = 'Wikipedia'
  max_iter = 2
  crawler = WikiCrawler(start, max_iter,'dunmp.p')
  crawler.crawl()