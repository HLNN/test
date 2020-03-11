from bs4 import BeautifulSoup
import requests
import time
import re
import os


class Top:
    def __init__(self):
        self.page = "https://movie.douban.com/top250"
        self.pages = [
            "https://movie.douban.com/top250?start={}&filter=".format(str(i))
            for i in range(0, 250, 25)
        ]
        self.comment = "https://movie.douban.com/subject/{num}/comments?start={start}&limit=20&sort=new_score&status=P"
        self.movies = []
        self.num = 0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
            "Cookie": 'viewed="1321789"; bid=KQLGt3JXHlA; gr_user_id=325dd335-32f7-40e4-badd-e88522c6a22f; _vwo_uuid_v2=DDF6359B9D53E386A3FFE8385C22E64E|f0bc2fe3124370eaf3e9350096df670c; ll="118268"; ap=1; __utmz=30149280.1518680117.6.3.utmcsr=link.zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=223695111.1518680117.5.2.utmcsr=link.zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; as="https://sec.douban.com/b?r=https%3A%2F%2Fmovie.douban.com%2Ftop250"; ps=y; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1518751297%2C%22https%3A%2F%2Flink.zhihu.com%2F%3Ftarget%3Dhttp%253A%2F%2Fmovie.douban.com%2Ftop250%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.953503549.1512921026.1518692008.1518751298.10; __utmb=30149280.0.10.1518751298; __utmc=30149280; __utma=223695111.1987325686.1517673910.1518692008.1518751298.9; __utmb=223695111.0.10.1518751298; __utmc=223695111; _pk_id.100001.4cf6=beee78244e51c0f7.1517673916.9.1518751499.1518692757.',
        }

    def top_page(self, url):
        wb_data = requests.get(url).text
        time.sleep(2)
        print(url)

        pattern = re.compile(
            '<a href="(https://movie.douban.com/subject/.*?)".*?"title">(.*?)</span>',
            re.S
        )
        items = re.findall(pattern, wb_data)

        for item in items:
            self.movie_page(item)

    def movie_page(self, item):
        url = item[0]
        wb_data = requests.get(url).text
        time.sleep(2)
        print(url)

        pattern = re.compile('v:genre">(.*?)</span>', re.S)
        genres = re.findall(pattern, wb_data)

        pattern = re.compile('v:average">(.*?)</strong>', re.S)
        rate = re.findall(pattern, wb_data)

        self.num += 1
        movie = {
            'num': self.num,
            'name': item[1],
            'genre': genres,
            'rate': rate
        }
        self.movies.append(movie)

        pattern = re.compile('(\d+)', re.S)
        num = re.findall(pattern, item[0])[0]

        self.comment_page(num)

    def comment_page(self, num):
        comments = []
        for start in range(0, 220, 20):
            url = self.comment.format(num=num, start=start)
            wb_data = requests.get(url).text
            time.sleep(2)
            print(url)

            pattern = re.compile('class="short">(.*?)</span>', re.S)
            comments += re.findall(pattern, wb_data)
            with open('{}.txt'.format(self.num), 'w') as f:
                f.write(str(comments))

    def main(self):
        for page in self.pages:
            self.top_page(page)

        with open('movie.cvs', 'w') as f:
            f.write(str(self.movies))
        print('finish')
        print(os.system('ls'))


top = Top()
top.main()
