# MajorFitting

###RateMyProfessor Crawler
we used the Scrapy, which was originally designed for web scraping, it can also be used to extract data using APIs (such as Amazon Associates Web Services) or as a general purpose web crawler to collect the data.

first step:
user need install the scrapy to install using pip. using pip to run:
pip install Scrapy 

second step:
after we set up the environment for the Scrapy. we can run the application in the first directory of file by:
scrapy crawl cragis -o items.json. (the cragis will indicates which spider document we will use and finally result the json type for the data )

###Core Algorithms

1. statistically improbable phrases of each department's comments

   run "python rankTFIDF.py"
   
2. vector space model plus cosine to rank departments by input query

   run "python query.py ratemyprofessorsdata query.txt"
