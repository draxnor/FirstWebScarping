# MoreleNetGPUScrapper
Webscrapping GPU offers from Polish on-line shops.
(currently only 1 - 'morele.net').

Scrapped data is saved to MySQL database.
Project written in Python. Scrapping using BeautifulSoup package.

## MySQL database
Database was prepared with project development in mind, where there will be multiple scrappers for multiple online shops.

Using mysql-connector as a MySQL driver.


### Database diagram

![scrapper_db_diagram](https://github.com/draxnor/MoreleNetGPUScrapper/assets/28366625/9752b4a8-9c4b-4f73-a675-37cccfc2a505)


## Future plans

The project started as a microproject, but it is fun and will be continued

I already tried scraping other shops like x-kom.pl or proline.pl, but unlike 'morele.net' those 2 are using anti-scraping techniques.
Especially x-kom might be difficult to scrap as it recognizes GET requests typical for bot/scripts and blocks further requests from same IP address.
Also they use auto-generated css selectors, what makes scraping more difficult.

Sounds like fun anyway, so I just need some time.

Todo:
- Scrapping multiple shops
- Rotating proxy to avoid being blocked
- Add session details to GET requests to pretend sending request as a web browser (bot will eventually get blocked otherwise)
- Adding scheduler to automatically scrap data once every day
- Add connection errors handling
