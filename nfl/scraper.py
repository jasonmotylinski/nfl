import logging
import md5
import urllib2

from BeautifulSoup import BeautifulSoup

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

host = 'http://www.nfl.com'
base_url = host + '/stats/categorystats?tabSeq=0&season=2015&seasonType=REG&experience=&Submit=Go&archive=false&conference=null&statisticCategory={0}&d-447263-p=1&qualified=false'


def scrape_category(category):
    return scrape(base_url.format(category))


def scrape(url):
    logger.info("Url: {0}".format(url))

    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)

    results = soup.find('table', id="result")
    ths = results.findAll('th')
    logger.info("Header: {0}".format(ths))
    stats = []
    for tr in results("tr"):
        tds = tr.findAll('td')
        if len(tds) > 0:
            stat = {
                ths[0].string: tds[0].string,
                ths[1].string: tds[1].find("a").string,
                ths[2].string: tds[2].find("a").string,
                ths[3].string: tds[3].string,
                ths[4].string: tds[4].string.strip(),
                ths[5].string: tds[5].string.strip(),
                ths[6].string: tds[6].string.strip(),
                ths[7].string: tds[7].string.strip(),
                ths[8].string: tds[8].string.strip()
            }
            m = md5.new()
            m.update(stat["Player"] + stat["Team"] + stat["Pos"])
            stat["id"] = m.hexdigest()
            stats.append(stat)

    nav = soup.find("span", {"class": "linkNavigation floatRight"})
    if nav:
        last_link_in_page_list = nav.findAll("a")[-1]
        if last_link_in_page_list.text == 'next':
            stats = stats + scrape(host + last_link_in_page_list['href'])
    return stats
