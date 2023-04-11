from flask import Flask, jsonify
import routes

def createApp():
    app = Flask(__name__,
                static_url_path='', 
                static_folder='web/static',
                template_folder='web/templates')
    routes.configure(app)
    return app


app = createApp()
app.run(use_reloader=True)