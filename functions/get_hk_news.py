import feedparser
import time
import os 
from datetime import datetime
from dataclasses import asdict
from functions.shared.mydataclasses import News
from functions.shared.mongoDB import NewsDB
from typing import Any, Dict

def get_news():
    '''
    Get HK finance news from multiple source 
    ::return: 
        - dictionary with provider as key and fetched raw news as values  
    '''
    result = {}
    rssLinkDict = {
        "mingpao": "https://news.mingpao.com/rss/pns/s00004.xml",
        "rthk": "http://rthk9.rthk.hk/rthk/news/rss/c_expressnews_cfinance.xml"
    }
    for provider, rssLink in rssLinkDict.items():
        newsFeed = feedparser.parse(rssLink)
        result[provider] = newsFeed.entries
    return result
    

def handler(event: Dict[str, Any], _: object):
    newsDB = NewsDB('hkFinanceDB', 'news', os.environ["MONGO_URL"])
    collection = newsDB.connectDB()
    news_dict = get_news()
    news_obj_lst = []
    current_datetime = datetime.now()
    for provider, news_list in news_dict.items():
        for news in news_list:
            news_obj = News(
                headline=news["title"],
                summary=news["summary"],
                url=news["link"],
                date=datetime(*news['published_parsed'][:6]),
                provider=provider,
                source=news["author"] if "author" in news.keys() else None,
                created_at=current_datetime
            )
            news_obj_lst.append(news_obj)
    newsDB.insertManyNews(collection, map(lambda news_obj: asdict(news_obj), news_obj_lst))

if __name__ == '__main__':
    import time
    start_time = time.time()
    handler(None, None)
    end_time = time.time()
    print("Time elapsed in this code: ", end_time - start_time)