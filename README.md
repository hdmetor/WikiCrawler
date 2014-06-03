This is a basic crawler for Wikipedia articles.
Please don't use it to actively crawl it at runtime. And if you need to, remember to [follow their rules](
http://en.wikipedia.org/wiki/Wikipedia:Database_download#Please_do_not_use_a_web_crawler):

Note that I filter out external, disambiguation and other links (e.g. images).

Still work in progress


####Possible improvement:

* the first links shown are the ones in the summary box (as per html order). Maybe I should show the links in the text before them?

* pass the as arguments to the script the following variables:

  - file location
  - start page
  - length

* keep track of the ordering of the crawl

* define a method that crawls all the links of the start page, up do a fixed depth


