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
        """
        Insert a single news into database
        """
        news_dict = asdict(news)
        
        try: 
            with self.connection.cursor() as cursor:
                
                stmt = sql.SQL("""
                    INSERT INTO {table_name} ({column_tuple})
                    VALUES ({value_tuple})
                    ;
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

    def insert_many_news(self, news_lst: list[News]):
        """
        Insert multiple news into database
        """
        news_dicts = [asdict(news) for news in news_lst]

        # Create list of tuple validated by psycopg2 sql string composition
        composed_values = []

        for news_dict in news_dicts:
            composed_values.append(
                sql.SQL("(") + sql.SQL(', ').join([sql.Literal(v) for v in news_dict.values()]) + sql.SQL(")")
            )

        try: 
            with self.connection.cursor() as cursor:
                
                stmt = sql.SQL("""
                    INSERT INTO {table_name} ({column_tuple})
                    VALUES {value_tuple}
                    ON CONFLICT (symbol, provider, url) DO NOTHING
                    ;
                """).format(
                    table_name = sql.Identifier(self.table_name),
                    column_tuple = sql.SQL(', ').join([
                        sql.Identifier(col) for col in news_dicts[0].keys()
                    ]),
                    value_tuple = sql.SQL(', ').join(composed_values)
                )
                #print(stmt.as_string(context=self.connection))
                cursor.execute(stmt)
                print("Insertion Completed")
        except Exception as e:
            print(e)


    
    
    
