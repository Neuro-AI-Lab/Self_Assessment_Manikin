import flask
from flask import Flask, render_template, session, request, flash, send_file
from flask_mail import Mail

import sys
sys.path.append(sys.path[0]+'/security')
from security import config
from security.password_hash import PasswordHash
import security.usertemp as user_temp
import model.UserDAO as UserDAO


app = Flask(__name__)
#app.config.update(config.MAIL_INFOMATION)
#app.config.update(dict(DEBUG=True))
app.secret_key = config.SESSION_SECRET_KEY
mail = Mail(app)
usertemp = user_temp.UserTemp()
hash_password = PasswordHash()
@app.route('/', methods=['GET', 'POST'])
def index():
    usertemp.__init__()
    if 'username' in session:
        username = session['username']
    else:
        username = None
    return render_template('html/index.html', username=username)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    usertemp.__init__()
    if request.method == 'POST':
        userid = request.form['ID']
        password = request.form['Password']
        dao = UserDAO.UserDAO()
        if dao.signin(userid, hash_password.password_hash(password)):
            session['username'] = userid
            flask.flash('반갑습니다. ' + userid + '님', category='success')
            print(1)
        else:
            flash('아이디 비밀번호가 틀립니다.', category='error')
            print(2)
    return render_template('html/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('html/register.html')
    if request.method == 'POST':
        userid = request.form['ID']
        password = request.form['Password']
        re_password = request.form['RepeatPassword']
        username = request.form['Name']
        email = request.form['Email']
        phone = request.form['Phone']
        age = request.form['Age']
        print(phone)
        dao = UserDAO.UserDAO()
        print(dao.checkEmail(email))
        if not (userid and password and re_password and username and email and phone):
            flash('Please check your login details and try again.', category='error')
            return render_template('html/register.html')
        if dao.checkid(userid):
            flash('이미 있는 아이디입니다.', category='error')
            return render_template('html/register.html')
        if dao.checkEmail(email) == True:
            flash('이미 있는 이메일입니다.', category='error')
            return render_template('html/register.html')
        if 20 < len(userid) or len(userid) < 6:
            flash('아이디는 6~20자리 사이의 값이여야합니다.', category='error')
            return render_template('html/register.html')
        if password != re_password:
            flash('비밀번호가 다릅니다.', category='error')
            return render_template('html/register.html')
        if len(password) < 8 or len(password) > 25:
            flash('비밀번호는 8~25자리 사이의 값이여야합니다.', category='error')
            return render_template('html/register.html')
        if int(age) >= 100 or int(age) < 1:
            flash('나이를 제대로 입력하세요.', category='error')
            return render_template('html/register.html')

        usertemp.setup(userid, hash_password.password_hash(password), email, username, int(age), phone)
        usertemp.saveuser()
        flash('good', category='success')
        return render_template('html/register.html')

@app.route('/samtest', methods=['GET', 'POST'])
def samtest():
    if request.method == 'GET':
        dao = UserDAO.UserDAO()
        path = list(dao.get_movie_path())
        count = 0
        return render_template('html/samtest.html', path = path, count = count)
    elif request.method == 'POST':
        path = request.form['path']
        count = request.form['count']
        count+=1
        return render_template('html/samtest.html', path=path, count=count)

#@app.route('/emailcheck', methods=['GET','POST'])
#def emailcheck():
#    if request.method == 'GET':
#        mail.send(usertemp.email_code())
#        render_template('html/emailcheck.html')
#    elif request.method == 'POST':
#        userotp= request.form['otp']
#        if usertemp.otp_check(userotp):
#            flash('이메일 인증이 완료 되었습니다.', category='success')
#            usertemp.__init__()
#        else:
#            flash('잘못된 번호를 입력했습니다. 다시 확인해 주세요.', category='error')



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)