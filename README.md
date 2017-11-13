### NBA Draft :jack_o_lantern:
Crawling data from https://www.basketball-reference.com/draft/

- `DDL.sql` defined the database schema, I use MySQL here but theoretically it works in most common databases.
- `requirements.txt` defined the `python` package I use.
  - `beautifulsoup` to parse `html` data
  - `requests` to send http requests
  - `pymysql` to interact with database
  - Life is short, I use Python : )
- They write messy code (such as uncommenting code blocks in the runtime to dynamically display data :hankey:). Anyway, if you find some abnormal ways to parse data from the website, thanks to their :boom:
- run `python3 crawler.py` to begin the journey!