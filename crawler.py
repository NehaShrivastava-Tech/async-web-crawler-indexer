import asyncio
import contextlib
import json
from bs4 import BeautifulSoup
import httpx
from urllib.parse import urljoin, urlparse

class NetworkResourceManager:
    def __init__(self, worker_name):
        self.worker_name = worker_name
        self.client = None

    async def __aenter__(self):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        self.client = httpx.AsyncClient(timeout=10.0, headers=headers, follow_redirects=True)
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()


class GoogleCaliberCrawler:
    def __init__(self, base_domain="docs.python.org"):
        self.search_index = {}
        self.visited_urls = set()
        self.base_domain = base_domain

    async def start_crawl(self, seed_url, max_pages=10):
        """Automatically discovers and crawls links dynamically using BFS logic."""
        queue = [seed_url]
        pages_crawled = 0
        
        async with NetworkResourceManager("WorkerNode-Main") as client:
            while queue and pages_crawled < max_pages:
                current_url = queue.pop(0)
                
                if current_url in self.visited_urls:
                    continue
                    
                print(f"🕷️ [{pages_crawled + 1}/{max_pages}] Crawling: {current_url}")
                try:
                    response = await client.get(current_url)
                    if response.status_code == 200:
                        self.visited_urls.add(current_url)
                        pages_crawled += 1
                        
                        # Parse HTML & update text index
                        soup = BeautifulSoup(response.text, 'html.parser')
                        self.update_search_index(current_url, soup)
                        
                        # Extract deep links dynamically
                        for link in soup.find_all('a'):
                            href = link.get('href')
                            if href:
                                absolute_url = urljoin(current_url, href)
                                # Keep the crawler restricted to the target domain so it doesn't wander off
                                if urlparse(absolute_url).netloc == self.base_domain:
                                    if absolute_url not in self.visited_urls and absolute_url not in queue:
                                        queue.append(absolute_url)
                                        
                        await asyncio.sleep(0.5) # Polite latency gap
                except Exception as e:
                    print(f"❌ Failed processing {current_url}: {e}")

    def update_search_index(self, url, soup):
        text = soup.get_text()
        words = text.lower().split()
        
        for word in words:
            cleaned_word = ''.join(e for e in word if e.isalnum())
            if len(cleaned_word) > 3:  
                if cleaned_word not in self.search_index:
                    self.search_index[cleaned_word] = []
                if url not in self.search_index[cleaned_word]:
                    self.search_index[cleaned_word].append(url)

    def save_index_to_disk(self, filename="index.json"):
        with open(filename, "w") as f:
            json.dump(self.search_index, f, indent=4)
        print(f"💾 Database saved successfully to '{filename}'!")


# --- Unified Execution Engine ---
async def main():
    crawler = GoogleCaliberCrawler(base_domain="docs.python.org")
    seed = "https://docs.python.org/3/tutorial/index.html"
    
    print("--- Running Production Asynchronous Discovery Crawler ---")
    await crawler.start_crawl(seed, max_pages=8)
    crawler.save_index_to_disk()
    
    print("\n==================================================")
    print("🔍 RELATIONAL INTERSECTING SEARCH ENGINE READY")
    print("==================================================")
    
    while True:
        user_input = input("\nEnter search keywords (or type 'exit'): ").lower().strip()
        if user_input == 'exit':
            break
            
        search_words = [w.strip() for w in user_input.split() if w.strip()]
        if not search_words: continue
            
        final_results = None
        for word in search_words:
            cleaned_word = ''.join(e for e in word if e.isalnum())
            matched_pages = set(crawler.search_index.get(cleaned_word, []))
            
            if final_results is None:
                final_results = matched_pages
            else:
                final_results = final_results.intersection(matched_pages)
                
        if final_results:
            print(f"🎯 Found {len(final_results)} page(s) for '{user_input}':")
            for idx, match in enumerate(final_results, 1):
                print(f"  {idx}. {match}")
        else:
            print(f"❌ No matching documents found for individual or joint terms.")

if __name__ == "__main__":
    asyncio.run(main())
    # --- Unified Execution Engine ---
async def main():
    # PASTE THESE TWO LINES HERE:
    crawler = GoogleCaliberCrawler(base_domain="bbc.com")
    seed = "https://www.bbc.com/news"
    
    print("--- Running Production Asynchronous Discovery Crawler ---")
    await crawler.start_crawl(seed, max_pages=8)
    crawler.save_index_to_disk()
