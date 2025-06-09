from routes.user import user
from routes.teacher import teacher
from routes.browse import browse
from routes.admin import admin

from flask import  render_template, send_from_directory
import os
from db_config import app
from flask_cors import CORS




CORS(app)

# 第2步 注册模块user
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(teacher, url_prefix='/teacher')
app.register_blueprint(browse, url_prefix='/teacher')
app.register_blueprint(admin, url_prefix='/admin')



@app.route('/yes')
def ping():
    return render_template('chartrun.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def ok():

    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
