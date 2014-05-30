from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib
import urllib.request
import re




# safer version of remove
def remove_el(l, key):
  try:
    l.remove(key)
  except ValueError:
    pass
  return l    

# gives a list of all the languages 
def languages(soup):
  langs = soup.find_all('a', lang=True)
  return [tag['lang'] for tag in langs]

#actually extract the links
def extract_links(soup):
  all_links = soup.findAll('a', {'href': wiki_links_condition})#, limit = limit)
  returned_links = []
  #just to be sure there are no duplicates links (and preserving the order!)
  for tag in all_links:
    if tag['href'][6:] in returned_links:
      pass
    else:
      returned_links.append(tag['href'][6:])
  return returned_links

#filtering out external link, disambiguation and non-article links (i.e. images)
def wiki_links_condition(x):
  if x:
        return x.startswith('/wiki/') and ':' not in x and not x.endswith('_(disambiguation)')
  else:
        return False
  
def crawl(page, visited, to_visit, root):

  htmltext = urllib.request.urlopen(root+page).read()
  soup = BeautifulSoup(htmltext)
  links = remove_el(list(extract_links(soup)),page)
  visited[page] = {

      'links' : links,
      'languages' : languages(soup), 
      'text_lenght' : text_lenght(soup)

      }

  missing = [li for li in links if ((li not in visited) and (li not in to_visit))]
  to_visit.remove(page)
  to_visit.extend(missing)

def text_lenght(soup):
  return len(soup.find('div', id='bodyContent').get_text())