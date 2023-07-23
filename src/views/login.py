from flask import Blueprint, render_template, redirect,url_for
from form import LoginForm
from common import *

login = Blueprint('login', __name__)


@login.route('/')
def get__login():
    return render_template('login.html', form=LoginForm())


@login.route('/', methods=['POST'])
def post__login():
    from models import User, OnlineUser
    try:
        form = LoginForm()
        assert form.validate_on_submit(), 'invalid form fields'
        #调用form对象的get_hash_password方法，获取表单中输入的密码经过哈希（hash）后的值，并且赋值给hash_password变量。 
        hash_password = form.get_hash_password()
        username = form.username.data
        #调用User类的get_by方法，根据username和hash_password查询用户记录，并且赋值给user变量。
        user = User.get_by(username=username, hash_password=hash_password)
        assert user, 'incorrect username or password'
        token = OnlineUser.create_record(user.id_)
        return set_token(redirect('/'), token)
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        return render_template('login.html', form=LoginForm(), message=message)
