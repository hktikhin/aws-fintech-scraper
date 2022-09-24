import requests
import os 
from functions.shared.mydataclasses import News
from functions.shared.sqldb import postgresql
from typing import Any, Dict
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def unix2date(ms: int) -> str:
    return datetime.fromtimestamp(ms/ 1_000).strftime(r"%Y-%m-%d")


class IEXstock:

    def __init__(self, token, symbol):
        self.BASE_URL = 'https://cloud.iexapis.com/stable'
        self.token = token
        self.symbol = symbol

    def get_company_news(self, retry: int = 5) -> list[dict]:
        # Return the recent 10 news 
        # source: https://iexcloud.io/docs/core/NEWS

        for _ in range(retry):
            url = f"{self.BASE_URL}/data/CORE/NEWS/{self.symbol}?last=10&token={self.token}"
            r = requests.get(url)
            if r.status_code == 200:
                return r.json()

        print(f"Get news request fail for news {self.symbol}")


    def get_credit_usage(self):
        url = f"{self.BASE_URL}/account/usage/credits?token={self.token}"
        r = requests.get(url)
        
        return r.json()

def get_top_symbols_news() -> list[dict]:
    """
    Get news from IEXcloud for top 10 symbols listed in the app 
    """
    symbols = ['AAPL', 'AMC', 'MZFT', 'AMZN', 'TSLA', 'BB', 'GME', 'SPCE', 'F', 'FB']
    result = []
    for symbol in symbols:
        s = IEXstock(os.getenv("IEX_TOKEN"), symbol)
        tmp = s.get_company_news()
        if tmp:
            result += tmp
    return result

def handler(event: Dict[str, Any], _: object):
    rds = postgresql(
            host=os.getenv("DATABASE_HOST"),
            database="projectvaluehub",
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            table_name="us_news"
        )
    news_lst = get_top_symbols_news()
    for news in news_lst:
        news_obj = News(
            headline=news["headline"],
            summary=news["summary"],
            url=news["url"],
            date=unix2date(news["datetime"]),
            provider=news["provider"],
            source=news["source"],
            symbol=news["symbol"],
            related=news["related"]
        )
        rds.insert_news(news_obj)
    print("Insertion Completed")

# if __name__ == '__main__':
#     import time
#     start_time = time.time()
#     handler(None, None)
#     end_time = time.time()
#     print("Time elapsed in this example code: ", end_time - start_time)