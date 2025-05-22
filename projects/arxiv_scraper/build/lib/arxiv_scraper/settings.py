# arxiv_scraper/settings.py

BOT_NAME = 'arxiv_scraper'

SPIDER_MODULES = ['arxiv_scraper.spiders']
NEWSPIDER_MODULE = 'arxiv_scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False # ArXiv API usage is generally fine, but be mindful.

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'arxiv_scraper.pipelines.ArxivFilesPipeline': 1,
   'arxiv_scraper.pipelines.ExcelPipeline': 300,
}


# Configure FilesPipeline settings
FILES_STORE = 'Data' # Base directory: Data/{keyword}/ArxivPaper/

# Set a User-Agent
# USER_AGENT = 'arxiv_scraper (+http://www.yourdomain.com)' # Replace with your info if deploying

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1 # 1 second delay between requests to be polite
CONCURRENT_REQUESTS_PER_DOMAIN = 8 # Max concurrent requests to any single domain

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 4.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Ensure UTF-8 encoding for feed exports (though we use a custom Excel pipeline)
FEED_EXPORT_ENCODING = 'utf-8'

# Logging
LOG_LEVEL = 'INFO' # Can be 'DEBUG' for more verbose output