from flask import Flask, jsonify
import routes
import sys
import logging

def createApp():
    app = Flask(__name__,
                static_url_path='', 
                static_folder='web/static',
                template_folder='web/templates')
    routes.configure(app)
    return app

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)s - %(module)s.%(funcName)s(): %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    stream=sys.stdout
)
app = createApp()
app.run(use_reloader=True)