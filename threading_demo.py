import threading
import requests
from bs4 import BeautifulSoup

class Scraper(threading.Thread):
    def __init__(self, threadId, name, url):
        threading.Thread.__init__(self)
        self.name = name
        self.id = threadId
        self.url = url

    def run(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html.parser')
        links = soup.find_all("a")
        return links
#list the websites in below list
websites = []
i = 1
for url in websites:
    thread = Scraper(i, "thread"+str(i), url)
    res = thread.run()
    # print res