import WikiHelper 
import pickle
import time
import random

#this could be arguments to pass in the future
root = 'http://en.wikipedia.org/wiki/'
file_loc = 'final.p'
start = 'DC_Comics'
#number of pages to crawl
lenght = 198 

print ('loading old file')
#load previous data
with open(file_loc, 'rb') as host:
    visited = pickle.load(host)
print ('old file loaded with ',len(visited),' visited pages')


if start in visited:
  print(start ,' was already crawled')
  quit()


# not using old list on purpouse
to_visit = [start]


# we can limit how many page we save if needed
limit = 20

while len(to_visit) > 0 and lenght>0:
  print (lenght)
  lenght-=1
  #be kind with wiki servers
  time.sleep(1)
  
  #random version
  WikiHelper.crawl(random.choice(to_visit),visited, to_visit, root)
  
  #non random version
  #crawl(to_visit[0])

print('crawl finished, saving now')
with open(file_loc, 'wb') as fp:
    pickle.dump(visited, fp)
print('saved')

