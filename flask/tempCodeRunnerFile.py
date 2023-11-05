from website import create_app

app = create_app()

if __name__ == '__main__': # only if we run the file and not import it, will it run
    app.run(debug=True) # debug=True this means that every time we make a change to any of our python code, it will automatically rerun the web server.
    
    