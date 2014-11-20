##WikiCrawer:

This is a basic crawler for Wikipedia articles.
Please don't use it to aggressively crawl Wiki and remember to follow [their rules](
http://en.wikipedia.org/wiki/Wikipedia:Database_download#Please_do_not_use_a_web_crawler).

Only articles pages are saved. Disambiguations, links to files or other external links are discarded.

Pages are visited only once, so their data may not be up to date. More recent pages have a time stamp created at the moment of crawling.

Links are saved in the order they appear on the page.

I have implemented some breath first search algorithms to visit the links. All of them allow cycles in the graph. It is possible to limit the search to the first _n_ links and to depth _d_.

##Planned features:

* show the relationship between the number of links +  number of translations and the text length. Find out what kinds of pages are outliers (i.e. long text but fewer links)

* try to predict the number of links given the number of translations and the text length

* find interesting or amusing connections between totally unrelated topics. For example the trip from Machiavelli to French fries (and back) is:

        ['Niccolò_Machiavelli', 'Florence', 'Brussels', 'French_fries']

        ['French_fries', 'Belgium', 'Head_of_state', 'Niccolò_Machiavelli']

    Note that both paths go through Belgium or Brussels

* cluster pages. It would be interesting to see if the path from A to B passes through the same clusters as the one from B to A

* plot the first _n_ links for each page and have the size of the nodes proportional to the number of links

* find the longest path of length _n_ starting from a given page

* draw the word cloud for the start page and see how it changes when visiting new pages in the path

* implement Dijkstra's algorithm for a more efficient graph search. The weight should be proportionally inverse to the number of links, so that the search is preferably done into 'hubs'

##Possible improvements:

* use mongodb to store the data. Change the save method to save only the pages crawled since the last save. Load method needs to load only the list of visited pages.
Possible structure for the db:

        {
            'page': page,
            'links': links,
            'text_length' : text_length,
            'languages' : languages,
            'time_stamp': time_stamp
        }

* define a method that crawls all (or the first _n_) links of the start page, up do a fixed depth

* allow a less verbose option

* pass as arguments to the script the following variables:

    - file location (optional)
    - start page
    - number of iterations


