from flask import Blueprint, url_for, request, render_template, flash, session, g, redirect
from module import dbmodule

logins = Blueprint('singup', __name__, url_prefix='/singup')


# static_folder='static',static_url_path='/static/css' 혹시나몰라서 남김


# 회원가입 기능 삭제할 예정
@logins.route('/login_singup_query', methods=['GET', 'POST'])
def login_singup_query():
    if request.method == 'POST':
        welcome = ''
        No_welcome = ''
        id = request.form['sigup_id']
        password = request.form['sigup_pw']
        drone_name = request.form['sigup_droneName']
        db_class = dbmodule.Database()
        # query = f"insert into test values ({id},{password},{drone_name})"
        # db_class.execute(query)
        # db_class.commit()
        query1 = f"select id from tb_login where id = '{id}'"
        print(query1)
        query2 = f"insert into tb_login values ({id},{password},{drone_name})"
        print(query2)
        row1 = db_class.executeOne(query1)
        print(row1)
        print(type(row1))
        if row1 is None:
            welcome = '회원가입 완료되었습니다'
            query = f"insert into tb_login values ('{id}','{password}','{drone_name}')"
            db_class.execute(query)
            db_class.commit()
            return render_template("manager/login.html", welcome=welcome)
        elif row1['id'] == id:
            if row1['id'] == '':
                No_welcome = '가입할 아이디랑 비밀번호 입력하시오'
                return render_template("manager/sigup.html", No_welcome=No_welcome)
            else:
                No_welcome = '이미 있는 아이디입니다. 다시 회원가입 하세요'
                return render_template("manager/sigup.html", No_welcome=No_welcome)


@logins.route('/login_test', methods=['GET', 'POST'])
def login_test():
    msg = ''
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
        db_class = dbmodule.Database()
        sql = f"select * from tb_login where mb_id = '{id}'and mb_pw = '{pw}'"
        print(sql)
        # row = db_class.executeAll(sql)
        row1 = db_class.executeOne(sql)
        # row2 = db_class.execute(sql)

        # print(row)
        print(row1)
        # print(row2)
        if row1:
            if row1['mb_id'] == '' and row1['mb_pw'] == '':
                msg = '로그인 아이디랑 비밀번호 입력하세요!'
                return render_template('manager/login.html', msg=msg)
            else:
                session['loggedin'] = True
                session['id'] = row1['mb_id']
                session['pw'] = row1['mb_pw']
                # return redirect(url_for('singup.login_check'))
                return redirect(url_for('main.mains'))
        else:
            msg = '아이디 틀렸거나 비번 다시 하세요'
    return render_template('manager/login.html', msg=msg)


@logins.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    return redirect(url_for('main.index'))


# android
@logins.route('/login_android', methods=['GET', 'POST'])
def login_android():
    msg = ''

    id = request.form['id']
    pw = request.form['pw']
    db_class = dbmodule.Database()
    sql = f"select * from tb_login where mb_id = '{id}'and mb_pw = '{pw}'"
    print(sql)
    row = db_class.executeOne(sql)
    print(row)

    if row:
        if row['mb_id'] == '' and row['mb_pw'] == '':
            msg = "아이디랑 비밀번호 입력하세요!"
        else:
            msg = "true"

    else:
        msg = "아이디 또는 비밀번호가 틀렸습니다."

    return msg