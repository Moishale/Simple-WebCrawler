import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class WebCrawler:
    def __init__(self, project_name, base_url, domain_name):
        self.project_name = project_name
        self.base_url = base_url
        self.domain_name = domain_name
        self.history = []
        self.session = requests.Session()
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.session.headers.update({'User-Agent': self.user_agent})

    def crawl(self, url):
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                links = []
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href:
                        full_url = urljoin(url, href).rstrip('/')
                        if self.domain_name in full_url and full_url not in self.history:
                            links.append(full_url)
                # add the current URL to history after we've crawled it
                self.history.append(url.rstrip('/'))
                return links
            else:
                return []
        except Exception as e:
            print(f'Error crawling {url}: {e}')
            return []

    def start(self):
        try:
            queue = [self.base_url]
            while queue:
                url = queue.pop(0)
                if url not in self.history:  # skip URLs that have already been crawled
                    links = self.crawl(url)
                    for link in links:
                        if link not in queue and link not in self.history:  # add new URLs to queue
                            queue.append(link)
                    self.history.append(url)
                    print(url)
        except KeyboardInterrupt:
            for link in queue:
                WebCrawler.save_to_file(self.project_name, link)

    @classmethod
    def save_to_file(cls, file_name, data):
        with open(f'{file_name}.txt', 'a',) as f:
            f.write(data + '\n')


crawler = WebCrawler(
    'youtube', 'https://youtube.com', 'youtube.com')
crawler.start()
