from flask import Blueprint, render_template, redirect
import re
from form import RegisterForm

register = Blueprint('register', __name__)
#用户名要求：中文、英文字母、数字；-、_、.等合法字符集范围之外的字符不允许使用；长度限制在36个字符之内
username_pattern = re.compile(r'[\u4e00-\u9fa5a-zA-Z0-9]{2,36}$s')

#密码要求
password_pattern = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\s\S]{8,36}')


@register.route('/')
def get__register():
    return render_template('register.html', form=RegisterForm())


@register.route('/', methods=['POST'])
def post__register():
    from models import User
    try:
        form = RegisterForm()
        #assert form.validate_on_submit(), 'invalid form fields'
        username = form.username.data
        assert username_pattern.fullmatch(username), '用户名不合法！'
        password = form.password.data
        confirm_password = form.confirm_password.data
        assert password == confirm_password, '两次输入密码不一致！'
        assert password_pattern.fullmatch(password), '密码不合法！'
        hash_password = form.get_hash_password()
        User.create_user(username, hash_password)
        return redirect('/login')
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        return render_template('register.html', form=RegisterForm(), message=message)
