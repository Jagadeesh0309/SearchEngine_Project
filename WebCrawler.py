
import requests
from bs4 import BeautifulSoup
import threading
import os
import re

class Variables():
    def __init__(self):
        self.count = 0

    def CountIncrement(self):
        self.count += 1

    def GetCount(self):
        return self.count


class WebCrawlerIR(threading.Thread):
    def __init__(self, MainLink, URLVisited, URLLimit, lock, SaveDir, CountData, URLMap):
        threading.Thread.__init__(self)
        self.MainLink = MainLink
        self.URLVisited = URLVisited
        self.URLLimit = URLLimit
        self.lock = lock
        self.SaveDir = SaveDir
        self.CountData = CountData
        self.URLMap = URLMap

    def URLCrawl(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
                NormalizedURL = None  
                for link in soup.find_all('a', href=True):
                    NormalizedURL = self.URLClean(response.url, link['href'])
                    with self.lock:
                        if len(self.URLVisited) >= self.URLLimit:
                            return
                        if NormalizedURL is not None and NormalizedURL not in self.URLVisited:
                            self.URLVisited.add(NormalizedURL)
                            #print("Link:", NormalizedURL)
                            self.CountData.CountIncrement()
                            filename = f"KUData{self.CountData.GetCount()}.txt"
                            fullpath = os.path.join(self.SaveDir, filename)
                            with open(fullpath, 'w', encoding='utf-8') as f:
                                f.write(response.text)
                                self.URLMap[fullpath] = NormalizedURL   
                            thread = WebCrawlerIR(NormalizedURL, self.URLVisited, self.URLLimit, self.lock, self.SaveDir, self.CountData, self.URLMap)
                            thread.start()
        except ConnectionResetError:
            print("ConnectionResetError occurred but script will continue.")
        except Exception as e:
            print("Error:", e)


    def URLClean(self, base_url, link):
        try:
            if not link or not isinstance(link, str):
                return None
            if re.search(r"/navigator(/navigator)*", link):
                return None
            if link.startswith('http'):
                return link
            elif link.startswith('/'):
                if base_url.endswith('/'):
                    return base_url[:-1] + link
                else:
                    return base_url + link
            else:
                return None
        except Exception as e:
            return None




    def run(self):
        self.URLCrawl(self.MainLink)

def WebsiteCrawler(InitialURL, URLLimit):
    URLVisited = set()
    lock = threading.Lock()

    SaveDir = 'webpages'
    if not os.path.exists(SaveDir):
        os.mkdir(SaveDir)
    URLMap = {}
    CountData = Variables()
    thread = WebCrawlerIR(InitialURL, URLVisited, URLLimit, lock, SaveDir, CountData, URLMap)
    thread.start()
    thread.join()
    return URLMap





