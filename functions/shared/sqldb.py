import psycopg2
from psycopg2 import sql
from functions.shared.mydataclasses import News
from dataclasses import asdict

class postgresql:
    def __init__(self, host, database, user, password, table_name):
        self.table_name = table_name
        self.connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
        )
        self.connection.set_session(autocommit=True)
    
    def insert_news(self, news: News):
        news_dict = {k: v for k, v in asdict(news).items() if v is not None}
        try: 
            with self.connection.cursor() as cursor:
                
                stmt = sql.SQL("""
                    INSERT INTO ({table_name} {column_tuple})
                    VALUES ({value_tuple})
                """).format(
                    table_name = sql.Identifier(self.table_name),
                    column_tuple = sql.SQL(', ').join([
                        sql.Identifier(col) for col in news_dict.keys()
                    ]),
                    value_tuple = sql.SQL(', ').join([
                        sql.Literal(val) for val in news_dict.values()
                    ])
                )
                cursor.execute(stmt)
        except Exception as e:
            print(e)


    
    
    
