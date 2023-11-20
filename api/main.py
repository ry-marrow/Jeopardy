from __init__ import create_app
#
from __init__ import create_app, db
from flask_migrate import Migrate


app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__': # only if we run the file and not import it, will it run
    app.run(debug=True) # debug=True this means that every time we make a change to any of our python code, it will automatically rerun the web server.
    
    

