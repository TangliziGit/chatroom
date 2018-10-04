from flask import (
    Flask, render_template
)
from flask_socketio import SocketIO

from chatroom import database
from chatroom import auth

def create_app():
    app=Flask(__name__)
    app.config.from_pyfile('config.py')
    app.teardown_appcontext(database.BaseDatabase.teardown)
    # app.cli.add_command()
    app.register_blueprint(auth.bp)

    @app.route('/index', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.errorhandler(404)
    def page_not_find(error):
        return render_template('404.html'), 404

    return app

def create_socket(app):
    socket=SocketIO(app)
    return socket
