import os
from flask import Blueprint, Flask, render_template, request
from module.dbmodule import Database

# 파일경로 없을경우 경로생성
# if True:
#     ddir = "parking"
#     num_ddir = "numPlate"
#     if not os.path.isdir('../static/'+ddir):
#         os.mkdir('../static/' + ddir)
#     if not os.path.isdir('../static/'+num_ddir):
#         os.mkdir('../static/' + num_ddir)


car_num_saveView = Blueprint('car_num_saveView',__name__,url_prefix='/car_num_saveView')


# 데이터베이스 테스트 완료
maria = Database()
query = "select * from tb_area where regulation_date = '2022-12-07'"
row = maria.executeOne(query)


@car_num_saveView.route('/saveView')
def car_saveView():
    return render_template("./information/save.html")

@car_num_saveView.route('/dateQuery',methods = ["GET","POST"])
def car_dateQuery():
    date = request.form['date']
    maria = Database()
    query = f"select * from tb_area where regulation_date = '{date}'"
    row = maria.executeAll(query)
    data_list = []
    for r in row:
        print(r)
        data_dic = {
            'parking': r['imgdir_parking'][10:],
            'numplate': r['imgdir_numplate'][10:]
        }
        data_list.append(data_dic)
    print(data_list)
    return render_template("./information/save.html", data_list= data_list)