from views import *


def run(app):
    from config import host, port, debug, ssl_context
    app.run(host=host, port=port, debug=debug, ssl_context=ssl_context)


def main():
    from database import create_app
    app = create_app(__name__)

    from config import csrf_key
    app.secret_key = csrf_key
    # ----------- 注册蓝图 ------------ #
    app.register_blueprint(root, url_prefix='/')
    app.register_blueprint(register, url_prefix='/register')
    app.register_blueprint(login, url_prefix='/login')
    app.register_blueprint(logout, url_prefix='/logout')

    run(app)


if __name__ == '__main__':
    main()
