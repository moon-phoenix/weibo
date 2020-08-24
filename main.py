from flask import Flask
from flask import redirect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from libs.orm import db
from user.view import user_bp
# from website.view import website_bp
from user.models import USER

app = Flask(__name__)
app.secret_key = r'(uieroih!ivo*he!ui%ggfpo#ghi$o232ibjb)'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/weibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 每次请求结束后都会自动提交数据库中的变动

manager = Manager(app)

db.init_app(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

app.register_blueprint(user_bp)
# app.register_blueprint(website_bp)


@app.route('/')
def home():
    return redirect('/user/login')


if __name__ == '__main__':
    app.debug = True
    manager.run()
