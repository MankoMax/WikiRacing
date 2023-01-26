import requests
from bs4 import BeautifulSoup
import time
from typing import List
from db import Database


requests_per_minute = 100
links_per_page = 200


class WikiRacer:
    def __init__(self):
        self.base_url = "https://uk.wikipedia.org/wiki/"
        self.last_request_time = time.time()
        self.request_interval = 60 / requests_per_minute
        self.db = Database()
        
    def fetch_page(self, title, if_exist=False):
        if not if_exist:
            db_title = self.db.add_title(title)
        else:
            db_title = self.db.get_title(title)
            
        processed_titles = list()
        
        if time.time() - self.last_request_time < self.request_interval:
                time.sleep(self.request_interval - (time.time() - self.last_request_time))
        try:
            response = requests.get(self.base_url + title)
            if response.status_code != 200:
                return []
        except:
            return []
        
        self.last_request_time = time.time()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        page = soup.find("div", {"id": "mw-content-text"})
        raw_links = page.find_all("a")
        
        for link in raw_links:
            try:
                if link['href'].startswith("/wiki/"):
                    if 'title' in link.attrs:
                        processed_titles.append(link['title'])
                        self.db.add_title(title=link['title'], parent_id=db_title[0])
                    else:
                        continue
            except Exception as e:
                continue
        return processed_titles[:links_per_page]
        
                    
    def get_urls_children(self, title) -> List[str]:
        db_title = self.db.get_title(title)
        processed_titles = list()
        
        if not db_title:
            processed_titles = self.fetch_page(title)
        else:
            title_children = self.db.get_children(db_title[0])
            if title_children:
                for child in title_children:
                    processed_titles.append(child[1])
            else:
                processed_titles = self.fetch_page(title, if_exist=True)
        return processed_titles[:links_per_page]
    
    
    def trace_path(self, parent: dict, first: str, second: str):
        path = [second]

        while True:
            path.append(parent[second])
            second = path[-1]
            
            if second == first:
                path.reverse()
                return path
            
            
    def find_path(self, start: str, finish: str) -> List[str]:
        queue = [start]
        visited = set()
        parent = {}
        
        while queue:
            title = queue.pop(0)
            cur_parent = title
            children = self.get_urls_children(title)

            for child in children:
                if child not in visited:
                    parent[child] = cur_parent
                    visited.add(child)
                    queue.append(child)
                
                if child == finish:
                    path = self.trace_path(parent, start, finish)
                    return path
        return []
        
        


if __name__ == '__main__':
    start_time = time.time()
    racer = WikiRacer()
    
    path = racer.find_path('Фестиваль', 'Пілястра')
    
    print(path)
    print("--- %s seconds ---" % (time.time() - start_time))
