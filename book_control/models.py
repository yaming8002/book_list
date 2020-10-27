from django.db import models
import pymysql
import requests
# import charts
import json

# 資料庫參數設定
class mySql_work():
    def __init__(self):
        self.db_settings = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "1qaz2wsx",
            "db": "booklist",
            "cursorclass":pymysql.cursors.DictCursor
        }
        # 建立Connection物件
        # conn = pymysql.connect(**self.db_settings)
        # cursor = conn.cursor()
        # # cursor.execute("SELECT * FROM students")

        # row = cursor.execute("SELECT * FROM `own_book_list` ;")        
        # print(cursor.fetchall())
        #資料表相關操作


    def Select(self,title="",Author=""):
        conn = pymysql.connect(**self.db_settings)
        cursor = conn.cursor()
        sqlcmd = "SELECT * FROM `own_book_list`"
        if title != "" and Author != "":
            sqlcmd = sqlcmd + f" where LOCATE('{title}', title) "+\
                f"& LOCATE('{Author}', Author)"
        elif  title != "":
            sqlcmd = sqlcmd + f"where LOCATE('{title}', title)"
        elif  Author != "":
            sqlcmd = sqlcmd + f"where LOCATE('{Author}', Author)"
        sqlcmd = sqlcmd +";"
        print(sqlcmd)
        # select * from table_test where FIND_IN_SET("23", field_A)
        cursor.execute(sqlcmd)

        row = cursor.fetchall()
        print(row)
        # conn.close()
        return row

    def addBook(self,data):
        bookinformaction =f"https://www.googleapis.com/books/v1/volumes?q=isbn:{data}"
        # bookinformaction ="https://www.googleapis.com/books/v1/volumes"
        print(bookinformaction)
        response =  requests.get(bookinformaction )
        # print(type(response.text))
        dct = json.loads(response.text)['items'][0]['volumeInfo']
        upset = {
            'title' : dct['title'] if 'title' in dct.keys() else "",
            'subtitle' : dct['subtitle'] if 'subtitle' in dct.keys() else "",
            'ISBN' : dct['industryIdentifiers'][0]['identifier'] if 'industryIdentifiers' in dct.keys() else "",
            'authors': dct['authors'] if 'authors' in dct.keys() else "",
            'publisher' : dct['publisher'] if 'publisher' in dct.keys() else "",
            'publishedDate' : dct['publishedDate'] if 'publishedDate' in dct.keys() else "",
            'smallThumbnail' : dct['imageLinks']['smallThumbnail'] if 'imageLinks' in dct.keys() else ""
        }

        # print("==================",upset.values())
        temp  = [x for x in  upset.values()]
        conn = pymysql.connect(**self.db_settings)
        cursor = conn.cursor()
        sqlcmd = f"INSERT INTO `own_book_list` (`title`,`subtitle`,`ISBN`,`Author`,`publisher`,`publishedDate`,`smallThumbnail`) VALUES ( '"
        sqlcmd = f"{sqlcmd} {temp[0]}'"
        for x in temp[1:]:
            # print(x)
            temp = "".join(f'{x}'.split("'"))
            # print(temp)
            sqlcmd = sqlcmd+f",'{temp}'" 
        sqlcmd  =sqlcmd +")"    
        print(sqlcmd)
        cursor.execute(sqlcmd)
        conn.commit()
        conn.close()
        
        return 0

    def delBook(self,data):
        conn = pymysql.connect(**self.db_settings)
        cursor = conn.cursor()
        sqlcmd = f"DELETE FROM `own_book_list` WHERE ISBN='{data}';"
        print(sqlcmd)
        cursor.execute(sqlcmd)
        conn.commit()
        conn.close()

if __name__ == "__main__":
    temp = mySql_work()
    temp.addBook("9789864343713")
    pass