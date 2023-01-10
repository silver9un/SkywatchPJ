# 사용하기 쉽게 데이터베이스 클래스 해둠

import pymysql

class Database:
    def __init__(self):
        self.db = pymysql.connect(host='project-db-stu.ddns.net',
                                  port=3307,
                                  user='sky',
                                  password='1q2w3e',
                                  db='sky',
                                  charset='utf8')
        self.curosr = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self,query,args={}):
        self.curosr.execute(query,args)

    def executeOne(self,query,args={}):
        self.curosr.execute(query,args)
        row = self.curosr.fetchone()
        return row

    def executeAll(self,query,args={}):
        self.curosr.execute(query,args)
        row = self.curosr.fetchall()
        return row

    def commit(self):
        self.db.commit()


# 테스트 한 내용
# sql = "select * from test"
# db_class = Database()
# a = db_class.executeOne(sql)
# print(a)
# db_class.commit()


