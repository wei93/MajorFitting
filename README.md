# MajorFitting

###RateMyProfessor Crawler
we used the Scrapy, which was originally designed for web scraping, it can also be used to extract data using APIs (such as Amazon Associates Web Services) or as a general purpose web crawler to collect the data.

first step:
user need install the scrapy to install using pip. using pip to run:
pip install Scrapy 

second step:
after we set up the environment for the Scrapy. we can run the application in the first directory of file by:
scrapy crawl cragis -o items.json. (the cragis will indicates which spider document we will use and finally result the json type for the data )

The code for crawler is in crawler folder. The output (comments of all departments in Texas A&M) is in RateMyProfessorsdata folder.

###Core Algorithms

We implemented two main functionalities for the project. The first functionality is to output the statistically improbable phrases of each department's comments. We listed the top 50 pharses with the highest TFIDF score of each department. The folder named rankresult(5 words) contains the result of pharses whose longest length is five words. The folder named rankresult(10 words) is the result of ranked pharses with the longest length of 10 words. 

The second functionality is to rank departments that is most cosine similar to the input query. For example the input query is "exam is hard" in query.txt. The program will output the top 5 departments with highest cosine score.

1. statistically improbable phrases of each department's comments

   run "python rankTFIDF.py"
   
2. vector space model plus cosine to rank departments by input query

   run "python query.py ratemyprofessorsdata query.txt"
   
###UI
   
   run "python server.py"
   on brower, open the url "localhost:5000"
