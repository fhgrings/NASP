from flask import request, jsonify, render_template
import json
from src.services.ControllerKeyService import ControllerKeyService
from src.services.NssmfCoreService import NssmfCoreService


def configure(app):

    @app.route('/')
    def index():
        use_cases = [{
            "name": "mIoT",
            "description": "Massive IoT",
            "status": "Ready",
            "is_shared": False
        },
        {
            "name": "urllc",
            "description": "Ultra Realiability Low Latency",
            "status": "Ready",
            "is_shared": False
        }]
        return render_template("table.html", use_cases = use_cases)

    @app.route('/table')
    def table():
        use_cases = [{
            "name": "mIoT",
            "description": "Massive IoT",
            "status": "Pending",
            "is_shared": False
        },
        {
            "name": "urllc",
            "description": "Ultra Realiability Low Latency",
            "status": "Ready",
            "is_shared": False
        }]
        return render_template("table.html", use_cases = use_cases)


    @app.route('/status')
    def alive():
        return {
            "commit": "087143285",
            "database": "ok",
            "version": "5.1.3"
        }

    @app.route("/controllerKey/", methods=['GET'])
    def getInfoCondutor():
        try:
            controller = ControllerKeyService()
            return controller.getControllerKey(request)
        except Exception as e:
            return str(e), 500
            
    @app.route("/controllerKey/", methods=['POST'])
    def getCondutor():
        try:
            controller = ControllerKeyService()
            return controller.createControllerKey(request)
        except Exception as e:
            return str(e), 500

    @app.route("/allocNssmfCore/", methods=['PUT'])
    def allocNssmfCore():
        try:
            NssmfCore = NssmfCoreService()
            return NssmfCore.allocNssmfCore(request)
        except Exception as e:
            return str(e), 500

    @app.route("/nssmfCore/", methods=['GET'])
    def getAllNssmfCore():
        try:
            NssmfCore = NssmfCoreService()
            return NssmfCore.getAllNssmfCore(request)
        except Exception as e:
            return str(e), 500