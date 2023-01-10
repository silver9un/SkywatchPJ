from flask import Blueprint, render_template, redirect, request
drone_registrationView = Blueprint('drone_registration',__name__,url_prefix='/drone_registration')


@drone_registrationView.route('/drone_registrationView')
def drone_view():
    return render_template("./drones/Registration_and_operation.html")

@drone_registrationView.route('/drone_registration', methods=['GET','POST'])
def drone_register():
    if request.method == "POST":
        if request.form['register'] == 'A 구역 드론 통신 등록':
            A = request.form['register']
            text = "192.168.10.1 "
            result_A = text + A + "했습니다."
            print(result_A)
            return render_template("./drones/Registration_and_operation.html", result_A=result_A)
        elif request.form['register'] == 'B 구역 드론 통신 등록':
            B = request.form['register']
            text = "192.168.10.2 "
            result_B = text + B + "했습니다."
            print(result_B)
            return render_template("./drones/Registration_and_operation.html",result_B=result_B)
        elif request.form['register'] == 'C 구역 드론 통신 등록':
            C = request.form['register']
            text = "192.168.10.3 "
            result_C = text + C + "했습니다."
            print(result_C)
            return render_template("./drones/Registration_and_operation.html", result_C=result_C)
        elif request.form['register'] == 'D 구역 드론 통신 등록':
            D = request.form['register']
            text = "192.168.10.4 "
            result_D = text + D + "했습니다."
            print(result_D)
            return render_template("./drones/Registration_and_operation.html", result_D=result_D)


