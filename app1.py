from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime

class NewsScraper:
    def __init__(self, url):
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        
        # Initialize webdriver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=chrome_options
        )
        
        self.url = url
        self.articles = []

    def scrape_articles(self, max_articles=10):
        try:
            # Navigate to the website
            self.driver.get(self.url)
            
            # Find article elements (adjust selectors based on specific website)
            article_elements = self.driver.find_elements(By.CSS_SELECTOR, 'article, .article, .news-item')
            
            # Limit number of articles scraped
            article_elements = article_elements[:max_articles]
            
            # Extract article details
            for element in article_elements:
                try:
                    title = element.find_element(By.CSS_SELECTOR, 'h2, .title').text
                    link = element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    
                    # Optional: Extract summary if available
                    try:
                        summary = element.find_element(By.CSS_SELECTOR, '.summary, .excerpt').text
                    except:
                        summary = ""
                    
                    self.articles.append({
                        'title': title,
                        'link': link,
                        'summary': summary,
                        'scraped_date': datetime.now()
                    })
                except Exception as e:
                    print(f"Error extracting individual article: {e}")
        
        except Exception as e:
            print(f"Scraping error: {e}")
        
        return self.articles

    def save_to_csv(self, filename=None):
        if not filename:
            filename = f"news_articles_{datetime.now().strftime('%Y%m%d')}.csv"
        
        df = pd.DataFrame(self.articles)
        df.to_csv(filename, index=False)
        print(f"Articles saved to {filename}")

    def __del__(self):
        # Close browser when done
        if hasattr(self, 'driver'):
            self.driver.quit()

# Example usage
def main():
    # Replace with actual news website URL
    scraper = NewsScraper('https://medium.com/')
    
    # Scrape articles
    articles = scraper.scrape_articles(max_articles=15)
    
    # Save to CSV
    scraper.save_to_csv()

    # Print scraped articles
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"Link: {article['link']}")
        print("---")

if __name__ == "__main__":
    main()