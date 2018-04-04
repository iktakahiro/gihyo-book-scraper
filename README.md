# gihyo_book_scraper

Web scraping script to get books data from http://gihyo.jp/book/genre

## Setup

```bash
conda install scrapy
```

## Usage

```bash
cd ./gihyo-book-scraper

# rm -f result/book.csv
scrapy crawl gihyo -o result/book.csv
````

column name | description
------------|------------
isbn | ISBN code
genre_id | Genre ID (2 digit)
genre | Genre Name
sub_genre_id | Sub Genre ID (4 digit)
sub_genre | Sub Genre Name
programing_language | Programing Language (Only genre_id = 06)
title | Book title
author | Author(s)
published_at | Date of published
price | Price
is_stock | When a stock is available, this fields is 1.
url | URL

