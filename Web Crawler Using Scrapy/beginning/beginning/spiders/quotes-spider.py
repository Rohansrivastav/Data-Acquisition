# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
class QuotesSpider(scrapy.Spider):
    name="quotes_spider"#name of our spider
    def start_requests(self):
        urls=['http://quotes.toscrape.com/page/1/',
             'http://quotes.toscrape.com/page/2/',
             ]
        for url in urls:#generator function
            yield scrapy.Request(url=url,callback=self.parse)#when the response comes , we need to parse it
    def parse(self,response):
        page_id=response.url.split('/')[-2]
        filename="quotes-%s.html"%page_id
        #parsing the data into a json file
        for i in response.css("div.quote"):
            text=i.css("span.text::text").get()
            author=i.css("small.author::text").get()##these codes are written from inspecting the html code from thr web 
            tags=i.css("a.tag::text").getall()
            yield{
             'text':text,
             'author':author,
             'tags':tags,        
            }
        #if we want scrape all thr web pages , we have to create a recursive crawler
        next_page=response.css('li.next a::attr(href)').get()##from inspecting the html code of the next button in the web page
        if next_page is not None:
            next_page=response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse)
       
    
    
    
    
    ##scrapy crawl quotes_spider -o quotes.json (executing this coomand on the terminal will create a json file named as quotes.json)
         
        
        #saving the response in a html file locally
       # with open(filename,'wb')as f:
         #   f.write(response.body)
          #  self.log('Saved file %s'% filename)