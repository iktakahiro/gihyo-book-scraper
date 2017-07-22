# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Response

NAME = 'gihyo'
DOMAIN = 'gihyo.jp'
BASE_URL = f'http://{DOMAIN}/book/genre'


class GihyoSpider(scrapy.Spider):
    name = NAME
    allowed_domains = [DOMAIN]
    start_urls = [BASE_URL]

    def parse(self, response: Response) -> Response:
        """Entry point of spider.

        :param Response response: scrapy.http.Response instance
        :yield: scrapy.http.Response instance
        """
        for href in response.css('#genreList ul ul li a::attr(href)'):
            target_url = response.urljoin(href.extract())

            yield scrapy.Request(target_url, callback=self._parse_item)

    def _parse_item(self, response: Response):
        """Scrape a target HTML.

        :param Response response: scrapy.http.Response instance
        :yield:
        """
        genre = response.css('.B_crumbBox span+a+a::text').extract_first()
        sub_genre = response.css('h1.mainTitle01::text').extract_first()
        sub_genre_id = response.url.replace(f'{BASE_URL}?s=', '')[:4]
        genre_id = sub_genre_id[:2]

        for x_book_wrapper in response.css('ul.bookList01 > li'):
            x_book = x_book_wrapper.css('div.data')

            title = ''.join(x_book.css('h3 > a::text').extract()).replace('　', ' ')

            programing_language = '-'
            if genre_id == '06':  # プログラミング・システム開発
                programing_language = classify_programing_language(title)

            published_at = x_book.css('p.sellingdate::text').re_first(r'^(.+)発売$')
            if published_at is None:
                published_at = x_book.css('p.sellingdate span::text').re_first(r'^(.+)発売$')

            x_price = x_book.css('p.price::text')
            is_stock = 1
            if '品切' in x_price.extract_first():
                is_stock = 0

            x_href = x_book.css('h3 a::attr(href)')

            yield {
                'isbn': x_href.re_first(r'^\/book\/\d{4}\/(.+)$').replace('-', ''),
                'genre_id': genre_id,
                'genre': genre,
                'sub_genre_id': sub_genre_id,
                'sub_genre': sub_genre,
                'programing_language': programing_language,
                'title': title,
                'author': x_book.css('p.author::text').extract_first(),
                'published_at': published_at,
                'price': x_price.re_first(r'^定価（本体(.+)円.*$').replace(',', ""),
                'is_stock': is_stock,
                'url': response.urljoin(x_href.extract_first())
            }

        next_href = response.css('div.pageSwitchTop p.next a::attr(href)').extract_first()
        if next_href:
            next_url = response.urljoin(next_href)

            yield scrapy.Request(next_url, callback=self._parse_item)


# TODO
LANGUAGE_LIST = [
    'Python',
    'Ruby',
    'PHP',
    'Perl',
    'JavaScript',
    'Java',
    'C#',
    'C++'
    'C言語'
    '.NET'
]


def classify_programing_language(title: str) -> str:
    """Classify programing language.

    :param str title: Title of a book
    :rtype: str
    :return: language
    """
    for lang in LANGUAGE_LIST:
        if lang in title:
            return lang

    return '-'
