## crawling www.researchgate.net with python and scrapy


## scrapy installation

https://doc.scrapy.org/en/latest/intro/install.html#intro-install

## crawling command

(also see the Scrapy tutorial: https://doc.scrapy.org/en/latest/intro/tutorial.html)
 
In the Terminal, go to the Scrapy project’s top level directory (`https://github.com/jauffretp/BeyondLab/tree/master/ScrapeResearchGate/scrapy_RG`) and run

```
scrapy crawl researchGate -o members_instit_loc_exp.json
```

Here, "researchGate" is the name of the class `scrapy.Spider` in the `rg_scrapy.py` file in the `spiders` subfolder 
The -o argument is the output filename. 

If you want to create your own Scrapy project, the starting command is

```
scrapy startproject ProjectName
```

(see `https://doc.scrapy.org/en/latest/intro/tutorial.html`). This will create the basic files needed for the project. I used `scrapy_RG` as ProjectName. 

However, in order to run the code here you also need Scrapoxy (`http://scrapoxy.io`) and an Amazon AWS account.

## Sample output

The file `https://github.com/jauffretp/BeyondLab/blob/master/ScrapeResearchGate/scrapy_RG/members_instit_loc_exp.json.try3` contains 1350 crawled records` (after one night of crawling).




