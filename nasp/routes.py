import requests
from flask import request, render_template
from src.services.ControllerKeyService import ControllerKeyService
from src.services.NssmfCoreService import NssmfCoreService
from src.services.NssmfRANService import NssmfRANService
from src.services.NsmfService import NsmfService

def configure(app):
    """Configure App Routes"""
    nasp_ui(app)
    nsmf(app)
    nssmf_core(app)
    nssmf_ran(app)

def nasp_ui(app):
    """NASP UI"""
    @app.route('/')
    def index():
        response = requests.get("http://localhost:5000/nasp/nst", timeout=100)
        return render_template("nst.html", use_cases = response.json())

    @app.route('/modal')
    def modal():
        response = requests.get("http://localhost:5000/nasp/nst", timeout=100)
        return render_template("modal.html", use_cases = response.json())

    @app.route('/nsst')
    def nsst():
        data = []
        response = requests.get("http://localhost:5000/nssmfRAN/nsst", timeout=100)
        data += response.json()
        response = requests.get("http://localhost:5000/nssmfCore/nsst", timeout=100)
        data += response.json()
        return render_template("nsst.html", use_cases = data)

    @app.route('/dashboard-metrics')
    def metrics():
        return render_template("dashboard-metrics.html", nssai = 1)
    @app.route('/dashboard-tracing')
    def tracing():
        return render_template("dashboard-tracing.html", nssai = 1)


    @app.route('/nsi')
    def nsi():
        return render_template("nsi.html", nssai = 1)

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

def nsmf(app):
    """
    NSMF
    """
    prefix = "/nasp"
    @app.route(f"{prefix}/controllerKey/", methods=['GET'])
    def get_controllerkey():
        try:
            controller = ControllerKeyService()
            return controller.getControllerKey(request)
        except Exception as exception:
            return str(exception), 500
            
    @app.route(f"{prefix}/controllerKey/", methods=['POST'])
    def put_controllerket():
        try:
            controller = ControllerKeyService()
            return controller.createControllerKey(request)
        except Exception as exception:
            return str(exception), 500

    @app.route(f"{prefix}/nst/", methods=['GET'])
    def get_nst():
        try:
            Nsmf = NsmfService()
            return Nsmf.get_all_nst(request)
        except Exception as exception:
            return str(exception), 500


    @app.route(f"{prefix}/allocNsi/", methods=['PUT'])
    def alloc_nsi():
        try:
            Nsmf = NsmfService()
            return Nsmf.allocNsi(request)
        except Exception as exception:
            return str(exception), 500

def nssmf_core(app):
    """Nssmf Core Routes"""
    prefix = "/nssmfCore"
    @app.route(f"{prefix}/allocNssi/", methods=['PUT'])
    def alloc_nssi_core():
        try:
            NssmfCore = NssmfCoreService()
            return NssmfCore.alloc_nssi(request)
        except Exception as exception:
            return str(exception), 500

    @app.route(f"{prefix}/nssi/", methods=['GET'])
    def get_all_nssi():
        try:
            NssmfCore = NssmfCoreService()
            return NssmfCore.get_all_nssi(request)
        except Exception as exception:
            return str(exception), 500

    @app.route(f"{prefix}/nsst/", methods=['GET'])
    def get_all_nsst_core():
        try:
            NssmfCore = NssmfCoreService()
            return NssmfCore.get_all_nsst(request)
        except Exception as exception:
            return str(exception), 500
    
    @app.route(f"{prefix}/nsst/", methods=['PUT'])
    def add_nsst_core():
        try:
            NssmfCore = NssmfCoreService()
            return NssmfCore.add_nsst(request)
        except Exception as exception:
            return str(exception), 500


def nssmf_ran(app):
    """Nssmf RAN Routes"""
    prefix = "/nssmfRAN"
    @app.route(f"{prefix}/allocNssi/", methods=['PUT'])
    def alloc_nssi_ran():
        try:
            NssmfRAN = NssmfRANService()
            return NssmfRAN.alloc_nssi(request)
        except Exception as exception:
            return str(exception), 500

    @app.route(f"{prefix}/nsst/", methods=['GET'])
    def get_all_nsst_ran():
        try:
            NssmfRAN = NssmfRANService()
            return NssmfRAN.get_all_nsst(request)
        except Exception as exception:
            return str(exception), 500

    @app.route(f"{prefix}/nssi/", methods=['GET'])
    def get_all_nssi_ran():
        try:
            NssmfRAN = NssmfRANService()
            return NssmfRAN.get_all_nssi(request)
        except Exception as exception:
            return str(exception), 500

    @app.route(f"{prefix}/nsst/", methods=['PUT'])
    def add_nsst_ran():
        try:
            NssmfRAN = NssmfRANService()
            return NssmfRAN.add_nsst(request)
        except Exception as exception:
            return str(exception), 500

