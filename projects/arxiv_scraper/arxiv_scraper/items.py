# arxiv_scraper/items.py
import scrapy

class ArxivPaperItem(scrapy.Item):
    published_date = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    summary = scrapy.Field()
    link = scrapy.Field()
    pdf_link = scrapy.Field()
    # For FilesPipeline
    file_urls = scrapy.Field() # List of URLs to download
    files = scrapy.Field()     # Stores download results (path, checksum, etc.)
    keyword = scrapy.Field()   # To help with file path i