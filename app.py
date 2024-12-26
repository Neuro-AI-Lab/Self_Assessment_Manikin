import flask
from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_mail import Mail
import ast

import sys
sys.path.append(sys.path[0]+'/security')
from security import config
from security.password_hash import PasswordHash
import security.usertemp as user_temp
import model.UserDAO as UserDAO


app = Flask(__name__)
app.secret_key = config.SESSION_SECRET_KEY
mail = Mail(app)
usertemp = user_temp.UserTemp()
hash_password = PasswordHash()
@app.route('/', methods=['GET', 'POST'])
def index():
    usertemp.__init__()
    if 'username' in session:
        if 'video_path' in session and 'video_count' in session and 'success_len' in session and 'video_name' in session:
            session.pop('video_name')
            session.pop('success_len')
            session.pop('video_path')
            session.pop('video_count')
        if session['username'] != None:
            dao = UserDAO.UserDAO()
            _, _, success_len = dao.get_movie_path_without_success(session['username'])
            session['success_len'] = success_len
    else:
        session['username'] = None
    return render_template('html/index.html')

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
        else:
            flash('아이디 비밀번호가 틀립니다.', category='error')
    return render_template('html/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('html/register.html')
    if request.method == 'POST':
        try:
            userid = request.form['ID']
            password = request.form['Password']
            re_password = request.form['RepeatPassword']
            username = request.form['Name']
            email = request.form['Email']
            phone = request.form['Phone']
            age = request.form['Age']
        except:
            flash("내용을 전부 기입하세요.", category='error')
            return render_template('html/register.html')
        dao = UserDAO.UserDAO()
        if not (userid and password and re_password and username and email and phone):
            flash('Please check your login details and try again.', category='error')
            return render_template('html/register.html')
        if dao.checkid(userid):
            flash('이미 있는 아이디입니다.', category='error')
            return render_template('html/register.html')
        if dao.checkEmail(email):
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
        flash('저장되었습니다.\n로그인을 해주세요.', category='success')
        return render_template('html/register.html')

@app.route('/samtest', methods=['GET', 'POST'])
def samtest():
    if not session.get('username'):
        return render_template('html/login.html')
    if request.method == 'GET':
        dao = UserDAO.UserDAO()

        path, video_name, success_len = dao.get_movie_path_without_success(session['username'])
        count = 0
        session['video_name'] = video_name
        session['video_path'] = path
        session['video_count'] = count
        session['success_len'] = success_len
        if 108 > session['video_count']:
            return render_template('html/samtest.html', path=path, video_check=True)
        else:
            flash("평가를 완료 했습니다.")
            return redirect(url_for('index'))
    elif request.method == 'POST':
        try:
            valance = request.form['valence']
            arousal = request.form['arousal']
            dominance = request.form['dominance']
            liking = request.form['liking']
            familiarity = request.form['familiarity']
            emotion = request.form['emotion']
        except:
            flash('SAM 평가를 완료하세요.', category='error')
            return render_template('html/samtest.html', video_check = True)
        if 'video_path' in session and 'video_count' in session and 'success_len' in session and 'video_name' in session:
            dao = UserDAO.UserDAO()
            path, video_name, success_len = dao.get_movie_path_without_success(session['username'])
            assessment_id = session['username'] + '/' + str(success_len)
            dao.save_movie_assessment(assessment_id, session['username'], session['video_name'], valance, arousal, dominance, liking, familiarity, emotion)
            session['video_count']+=1
            session['success_len'] = success_len
            session['video_name'] = video_name
            session['video_path'] = path

        else:
            dao = UserDAO.UserDAO()
            path, video_name, success_len = dao.get_movie_path_without_success(session['username'])
            count = 0
            session['video_name'] = video_name
            session['video_path'] = path
            session['video_count'] = count
            session['success_len'] = success_len

        if 108 > session['video_count']:
            return render_template('html/samtest.html', video_check = True)
        else:
            flash("평가를 완료 했습니다.")
            return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)