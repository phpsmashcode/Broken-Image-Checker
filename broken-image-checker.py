import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import concurrent.futures
import time
import os
from collections import deque
import csv
from datetime import datetime

class WebsiteImageChecker:
    def __init__(self, base_url, max_pages=None):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited_urls = set()
        self.images_checked = set()
        self.broken_images = []
        self.valid_images = []
        self.max_pages = max_pages
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Create reports directory if it doesn't exist
        self.reports_dir = os.path.join(os.getcwd(), 'image_reports')
        os.makedirs(self.reports_dir, exist_ok=True)

    def is_valid_url(self, url):
        """Check if the URL is valid and belongs to the same domain."""
        try:
            parsed = urlparse(url)
            return all([parsed.scheme, parsed.netloc]) and parsed.netloc == self.domain
        except:
            return False

    def is_valid_webpage(self, url):
        """Check if the URL is likely to be a webpage (not a file or image)."""
        webpage_extensions = {'.html', '.htm', '.php', '.asp', '.aspx', ''}
        return os.path.splitext(urlparse(url).path)[1].lower() in webpage_extensions

    def check_image_url(self, img_data):
        """Check if an image URL is accessible."""
        if img_data['url'] in self.images_checked:
            return None
        
        self.images_checked.add(img_data['url'])
        try:
            response = self.session.head(img_data['url'], timeout=5, allow_redirects=True)
            if response.status_code == 404:
                return False, "404 Not Found"
            elif response.status_code >= 400:
                return False, f"HTTP {response.status_code}"
            return True, "OK"
        except requests.RequestException as e:
            return False, str(e)

    def get_page_links(self, url):
        """Extract all links from a webpage."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            links = []
            for a in soup.find_all('a', href=True):
                href = urljoin(url, a['href'])
                if self.is_valid_url(href) and self.is_valid_webpage(href):
                    links.append(href)
            return links
        except Exception as e:
            print(f"Error getting links from {url}: {e}")
            return []

    def get_page_images(self, url):
        """Extract all image URLs from a webpage."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            images = []
            for img in soup.find_all('img'):
                src = img.get('src')
                if src:
                    absolute_url = urljoin(url, src)
                    if urlparse(absolute_url).scheme in ['http', 'https']:
                        images.append({
                            'url': absolute_url,
                            'alt': img.get('alt', ''),
                            'page_url': url,
                            'location': str(img.parent)[:100] + '...'
                        })
            return images
        except Exception as e:
            print(f"Error getting images from {url}: {e}")
            return []

    def crawl_website(self):
        """Crawl the website and check all images."""
        start_time = time.time()
        pages_queue = deque([self.base_url])
        pages_checked = 0

        print(f"\nStarting crawl of {self.base_url}")
        print("This may take a few minutes depending on the website size...")
        
        while pages_queue and (self.max_pages is None or pages_checked < self.max_pages):
            current_url = pages_queue.popleft()
            
            if current_url in self.visited_urls:
                continue
                
            self.visited_urls.add(current_url)
            pages_checked += 1
            
            print(f"\nChecking page {pages_checked}: {current_url}")
            
            # Get all images from the current page
            page_images = self.get_page_images(current_url)
            
            # Check images in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_img = {executor.submit(self.check_image_url, img): img 
                               for img in page_images}
                
                for future in concurrent.futures.as_completed(future_to_img):
                    img = future_to_img[future]
                    result = future.result()
                    
                    if result is None:  # Image already checked
                        continue
                        
                    is_valid, status = result
                    if not is_valid:
                        self.broken_images.append({
                            'url': img['url'],
                            'alt': img['alt'],
                            'status': status,
                            'page_url': img['page_url'],
                            'location': img['location']
                        })
                    else:
                        self.valid_images.append(img['url'])
            
            # Add new pages to the queue
            new_links = self.get_page_links(current_url)
            pages_queue.extend(link for link in new_links if link not in self.visited_urls)
            
            # Progress update
            print(f"Pages checked: {pages_checked}")
            print(f"Images checked: {len(self.images_checked)}")
            print(f"Broken images found: {len(self.broken_images)}")
        
        self.save_report()
        
        # Final summary
        print(f"\nCrawl completed in {time.time() - start_time:.2f} seconds")
        print(f"Total pages checked: {pages_checked}")
        print(f"Total images checked: {len(self.images_checked)}")
        print(f"Total broken images: {len(self.broken_images)}")

    def save_report(self):
        """Save the broken images report to a CSV file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"broken_images_{self.domain}_{timestamp}.csv"
        filepath = os.path.join(self.reports_dir, filename)
        
        print(f"\nSaving report to: {filepath}")
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Page URL', 'Image URL', 'Status', 'Alt Text', 'Location'])
                for img in self.broken_images:
                    writer.writerow([
                        img['page_url'],
                        img['url'],
                        img['status'],
                        img['alt'],
                        img['location']
                    ])
            
            print(f"\nReport saved successfully!")
            print(f"Total broken images found: {len(self.broken_images)}")
            print(f"You can find the report at: {filepath}")
            
            # If no broken images were found, create an empty report with a note
            if not self.broken_images:
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['No broken images found'])
                print("No broken images were found on the website.")
            
            # Try to open the reports folder
            try:
                os.startfile(self.reports_dir)
            except:
                print(f"\nYou can manually open the reports folder at: {self.reports_dir}")
                
        except Exception as e:
            print(f"\nError saving report: {e}")
            print(f"Attempted to save at: {filepath}")
            
            # Fallback to desktop if current directory is not writable
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            fallback_filepath = os.path.join(desktop_path, filename)
            
            try:
                with open(fallback_filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Page URL', 'Image URL', 'Status', 'Alt Text', 'Location'])
                    for img in self.broken_images:
                        writer.writerow([
                            img['page_url'],
                            img['url'],
                            img['status'],
                            img['alt'],
                            img['location']
                        ])
                print(f"\nReport saved to desktop instead: {fallback_filepath}")
            except Exception as e2:
                print(f"\nCould not save report to desktop either: {e2}")
                print("\nHere are the broken images found:")
                for img in self.broken_images:
                    print(f"\nPage: {img['page_url']}")
                    print(f"Image: {img['url']}")
                    print(f"Status: {img['status']}")

if __name__ == "__main__":
    print("Website Broken Image Checker")
    print("=" * 30)
    website_url = input("\nEnter website URL to check (include http:// or https://): ")
    max_pages = input("Enter maximum number of pages to check (press Enter for unlimited): ")
    max_pages = int(max_pages) if max_pages.strip() else None
    
    print("\nStarting check...")
    checker = WebsiteImageChecker(website_url, max_pages)
    checker.crawl_website()
    
    input("\nPress Enter to exit...")