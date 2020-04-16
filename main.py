import threading
import urllib3
from bs4 import BeautifulSoup
import sys
import os

class Crawler:
    def __init__(self, http, novel_url):
        self.novel_url = novel_url
        self.chapter_list = []
        self.http = http

    def crawlChaper(self):
        html = http.request('GET',self.novel_url).data.decode('utf-8')
        self.page = BeautifulSoup(html, 'lxml')
        for chapters in self.page.findAll('li', class_='wp-manga-chapter'):
            url = chapters.a
            self.chapter_list.append(url.get('href'))

class Chapter(threading.Thread):
    def __init__(self, http, url):
        threading.Thread.__init__(self)
        self.url = url
        html = http.request('GET',url).data.decode('utf-8')
        self.page = BeautifulSoup(html, 'lxml')

    def run(self):
        self.getText()
        self.writeChapter()
        print('DONE - '+self.title)

    def getText(self):
        post = self.page.find('div', class_='reading-content')
        text = post.get_text()
        self.text = text

        # title
        title = post.find('h3')
        if title is None:
            title = post.find('h4')
            if title is None:
                self.title = self.url.split('/')[-1].replace('-',' ')
            else:
                self.title = title.get_text().replace('/n', '')
        else:
            self.title = title.get_text().replace('/n', '')
        return text

    def writeChapter(self):
        filename = 'output/'+self.title+'.txt'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as file:
            file.write(self.text)
        return

if __name__ == "__main__":
    # sys.argv[1]
    http = urllib3.PoolManager()
    crawler = Crawler(http,'https://boxnovel.com/novel/omniscient-readers-viewpoint/')
    crawler.crawlChaper()
    
    threads_pool = []
    for i in crawler.chapter_list:
        print('thread started')
        thread = Chapter(http, i)
        thread.start()
        threads_pool.append(thread)

    for thread in threads_pool:
        thread.join()