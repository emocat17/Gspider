# arxiv_scraper/spiders/arxiv_spider.py
import scrapy
import feedparser
from datetime import datetime
import re
import urllib.parse # Ensure this import is present
from arxiv_scraper.items import ArxivPaperItem

class ArxivSpider(scrapy.Spider):
    name = 'arxiv' # Make sure you run 'scrapy crawl arxiv'
    allowed_domains = ['export.arxiv.org', 'arxiv.org']
    base_url = 'http://export.arxiv.org/api/query?'
    max_results_per_request = 1000

    def __init__(self, keyword="zero trust", start_year="2020", *args, **kwargs):
        super(ArxivSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        try:
            self.start_date = datetime(int(start_year), 1, 1)
        except ValueError:
            self.logger.error(f"Invalid start_year: {start_year}. Using 2020.")
            self.start_date = datetime(2020, 1, 1)
        self.current_start_index = 0
        self.logger.info(f"Spider initialized with keyword: '{self.keyword}', start_date: {self.start_date.strftime('%Y-%m-%d')}")

    def _clean_filename(self, title):
        illegal_chars_pattern = r'[\\/:*?"<>|\n\r\t]'
        safe_title = re.sub(illegal_chars_pattern, ' ', title)
        safe_title = " ".join(safe_title.split())
        return safe_title[:200]

    # Changed from start_requests to start to address deprecation warning and make it async
    async def start(self): # Scrapy 2.13+ prefers async def start(self)
        query = f'all:"{self.keyword}"'
        params = {
            'search_query': query,
            'start': self.current_start_index,
            'max_results': self.max_results_per_request,
            'sortBy': 'submittedDate',
            'sortOrder': 'ascending'
        }
        # Corrected URL construction
        query_string = urllib.parse.urlencode(params)
        url = self.base_url + query_string
        
        self.logger.info(f"Initial request URL: {url}")
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        self.logger.info(f"Parsing response from: {response.url}")
        
        # It's good practice to check for errors in the response
        if response.status != 200:
            self.logger.error(f"Received non-200 response ({response.status}) for URL: {response.url}")
            return

        try:
            feed = feedparser.parse(response.body)
        except Exception as e:
            self.logger.error(f"Failed to parse feed from {response.url}: {e}")
            return

        if not feed.entries:
            self.logger.info("No more entries found or feed is empty. Stopping.")
            return

        entries_processed_count = 0
        for entry in feed.entries:
            try:
                published_date_str = entry.published.split('T')[0]
                published_date = datetime.strptime(published_date_str, '%Y-%m-%d')
            except (AttributeError, ValueError, KeyError) as e:
                self.logger.warning(f"Could not parse date for entry '{entry.get('title', 'N/A')}': {entry.get('published', 'N/A')}. Error: {e}. Skipping.")
                continue

            if published_date < self.start_date:
                self.logger.debug(f"Skipping old entry: {entry.title} ({published_date_str})")
                continue
            # This check might be too aggressive if entries are not perfectly sorted or if there's a slight delay
            # if published_date > datetime.now(): 
            #     self.logger.info(f"Found entry from future {entry.title} ({published_date_str}), stopping further processing for this page.")
            #     break 

            item = ArxivPaperItem()
            item['keyword'] = self.keyword
            item['published_date'] = entry.published
            item['title'] = entry.title
            item['authors'] = ', '.join(author.name for author in entry.authors)
            item['summary'] = entry.summary
            item['link'] = entry.link
            
            pdf_link = next((link.href for link in entry.links if 'title' in link and link.title.lower() == 'pdf'), None)
            item['pdf_link'] = pdf_link

            if pdf_link:
                item['file_urls'] = [pdf_link]
            else:
                item['file_urls'] = []
            
            entries_processed_count +=1
            yield item
        
        self.logger.info(f"Processed {entries_processed_count} relevant entries from this page (total fetched: {len(feed.entries)}).")

        # Pagination
        # Only request next page if we got the max_results we asked for,
        # and we actually processed some relevant entries (or allow if no relevant entries but still full page)
        if len(feed.entries) == self.max_results_per_request:
            self.current_start_index += len(feed.entries) # Increment by total entries fetched
            query = f'all:"{self.keyword}"'
            next_page_params = {
                'search_query': query,
                'start': self.current_start_index,
                'max_results': self.max_results_per_request,
                'sortBy': 'submittedDate',
                'sortOrder': 'ascending'
            }
            # Corrected URL construction for pagination
            next_page_query_string = urllib.parse.urlencode(next_page_params)
            next_page_url = self.base_url + next_page_query_string
            
            self.logger.info(f"Fetching next set of results from index {self.current_start_index}. URL: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            if len(feed.entries) < self.max_results_per_request:
                 self.logger.info(f"Fetched {len(feed.entries)} entries, less than max_results ({self.max_results_per_request}), assuming end of results. Stopping pagination.")
            # If entries_processed_count is 0 but len(feed.entries) == self.max_results_per_request, it means all entries on the page were too old.
            # The current logic will continue paginating, which is correct.