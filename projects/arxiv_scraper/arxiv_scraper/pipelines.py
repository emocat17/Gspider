# arxiv_scraper/pipelines.py
import os
import re
import pandas as pd
from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.project import get_project_settings
from itemadapter import ItemAdapter

class ArxivFilesPipeline(FilesPipeline):
    
    def _clean_filename(self, title):
        illegal_chars_pattern = r'[\\/:*?"<>|\n\r\t]'
        safe_title = re.sub(illegal_chars_pattern, ' ', title)
        safe_title = " ".join(safe_title.split()) # Remove multiple spaces
        return safe_title[:200] # Limit filename length

    def file_path(self, request, response=None, info=None, *, item=None):
        adapter = ItemAdapter(item)
        keyword = adapter.get('keyword', 'unknown_keyword')
        title = adapter.get('title', 'untitled')
        safe_title = self._clean_filename(title)
        
        # Get published date to create year/quarter structure (optional, but good for organization)
        # For simplicity, we'll use the structure Data/{keyword}/ArxivPaper/{safe_title}.pdf
        # If you want year/quarter, you'd parse item['published_date'] here.
        
        # Path: Data/{keyword}/ArxivPaper/{safe_title}.pdf
        return f"{keyword}/ArxivPaper/{safe_title}.pdf"

class ExcelPipeline:
    def __init__(self):
        self.items_by_keyword = {}
        self.settings = get_project_settings()

    def open_spider(self, spider):
        # Create base 'Data' directory if it doesn't exist
        # The FilesPipeline will handle its own subdirectories based on FILES_STORE
        # This pipeline handles the Excel file directory.
        self.data_dir = self.settings.get('FILES_STORE', 'Data') # Use FILES_STORE as base
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Initialize list for the current spider's keyword
        self.items_by_keyword[spider.keyword] = []


    def close_spider(self, spider):
        keyword = spider.keyword # Get keyword from spider instance
        
        if not self.items_by_keyword.get(keyword):
            spider.logger.info(f"No items collected for keyword '{keyword}' to save to Excel.")
            return

        # Directory for Excel file: Data/{keyword}/
        keyword_data_dir = os.path.join(self.data_dir, keyword)
        if not os.path.exists(keyword_data_dir):
            os.makedirs(keyword_data_dir)

        excel_filename = os.path.join(keyword_data_dir, f"{keyword}_papers.xlsx")
        
        df = pd.DataFrame(self.items_by_keyword[keyword])
        
        # Remove 'files' and 'file_urls' columns before saving to Excel if they are too verbose
        if 'files' in df.columns:
            df = df.drop(columns=['files'])
        # 'file_urls' might be useful, but 'pdf_link' is usually what users want in Excel
        # if 'file_urls' in df.columns:
        #     df = df.drop(columns=['file_urls'])
        if 'keyword' in df.columns: # Not really needed in the excel file itself
            df = df.drop(columns=['keyword'])

        try:
            df.to_excel(excel_filename, index=False, engine='openpyxl')
            spider.logger.info(f"Excel spreadsheet saved to {excel_filename}")
        except Exception as e:
            spider.logger.error(f"Failed to save Excel file {excel_filename}: {e}")


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        keyword = adapter.get('keyword')
        
        # Store item (as dict) for later conversion to DataFrame
        # We convert item to dict here to avoid issues with Scrapy items in Pandas later
        # and to ensure 'files' field (added by FilesPipeline) is captured if needed for debugging
        # but we will likely drop it before saving to excel.
        item_dict = adapter.asdict()
        
        # The 'files' field is added by FilesPipeline *after* this item might pass through other pipelines.
        # So, we append the item as is. The 'files' field will be populated if FilesPipeline runs before this one.
        self.items_by_keyword.setdefault(keyword, []).append(item_dict)
        return item # Important: return item for other pipelines