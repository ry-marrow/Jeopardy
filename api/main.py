from .website import create_app, socketio
from .website import create_app, db
from flask_migrate import Migrate
# from flask_socketio import SocketIO

app = create_app()
migrate = Migrate(app, db)
#socketio = SocketIO(app)

if __name__ == '__main__': # only if we run the file and not import it, will it run
    # app.run(debug=True) # debug=True this means that every time we make a change to any of our python code, it will automatically rerun the web server.
    socketio.run(app, debug=True) # debug=True this means that every time we make a change to any of our python code, it will automatically rerun the web server.
    
    
