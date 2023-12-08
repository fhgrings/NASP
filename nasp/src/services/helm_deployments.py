import os
import logging
import time
import json
import requests
import random
import subprocess
from .slice_config import *

BASE_HELM = "../helm_charts"
BASE_HELM_TMP = "/tmp/helm-nasp-temp/"
BASE_NFs = [ "nrf","amf",  "rantester","nssf", "udr", "webui", "ausf", "pcf","smf", "udm", "upf", "mongodb"]


class NsmfService():
    """Nsmf Service Class"""
    def allocNsi(self, req):
        """Get All NSSTs Core"""
        try:
            logging.info("allocNSI")
            
            S_NSSAI = "1"+f"27440{int(random.random()*10)}"
            logging.info(f"S_NSSAI Selected = {S_NSSAI}")
            data = {"name": req.json["name"], "description": req.json["description"], "S_NSSAI": S_NSSAI}
            logging.info(data)
            self.add_to_db(data, "nsi")
            self.deploy_ns(req,S_NSSAI)
            return f"Alloc Completed with success", 200
        except Exception as exception:
            return f"Bad Request - {exception}", 400

    def getAllNsi(self, request):
        """Get All NSIs"""
        try:
            data = open("../data/db/nsi.json", "r", encoding="utf-8")
            return json.load(data)
        except Exception as exception:
            return f"Bad Request - {exception}", 400

    def add_nsi(self, nsi):
        """Get All NSSTs Core"""
        try:
            data = open("../data/db/nsi.json", encoding="utf-8")
            try:
                nsi_list = json.load(data)
            except Exception as exception:
                print(str(exception))
                nsi_list = []
            
            nsi_list.append(nsi)
            f = open("../data/db/nsi.json", "w", encoding="utf-8")
            f.write(json.dumps(nsi_list))
            f.close()
            return data
        except Exception as exception:
            return f"Bad Request - {exception}", 400



    def add_to_db(self, data, table):
        try:
            db_data = open(f"../data/db/{table}.json", encoding="utf-8")
            try:
                nsi_list = json.load(db_data)
            except Exception as exception:
                print(str(exception))
                nsi_list = []
            nsi_list.append(data)
            f = open("../data/db/nsi.json", "w", encoding="utf-8")
            f.write(json.dumps(nsi_list))
            f.close()
            return
        except Exception as exception:
            print(str(exception))

    def deploy_ns(self, req, nssai="default"):
        """
        Create NS => Cp to tmp => Update configs => Deploy
        """
        namespace = "ns-"+nssai
        self.create_ns(namespace)
        self.create_helm_tmp(BASE_HELM)
        NFs = self.update_slice_config(BASE_HELM_TMP, req)
        for nf in NFs:
            print(self.install_helm(nf, BASE_HELM_TMP+nf, namespace))


    def create_ns(self, name):
        cmd = f'kubectl create ns {name}'
        try:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8')
        except Exception as exception:
            raise Exception(exception.output.decode('utf-8'))
        
    def create_helm_tmp(self, path):
        cmd = f'cp -r {path} /tmp/helm-nasp-temp'
        try:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8')
        except Exception as exception:

            raise Exception(exception.output.decode('utf-8'))
        
    def update_slice_config(self, base_path, req):
        # if req["exposed"]:
        #     enable_public_ip(req)
        # if req["N3GPP Support"]:
        #     enable_n3iwf(req)
        # if not req["shared"]:
        #     add_all_nfs(req)
        # if req["availability"] > 99.99:
        #     add_nf_redundance()
        
        # pdu_resource((req["UE Density"]/100)+0.45)

        # update_UE_PDU_sessions(req)
        return BASE_NFs
        
    def install_helm(self, name,path,ns="default"):
        cmd = f'helm -n {ns} install {name} {path}'
        try:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            return f"{name} Install with Success"
        except Exception as exception:
            raise Exception(exception.output.decode('utf-8'))







    def getAllNsi(self, request):
        """Get All NSIs"""
        try:
            data = open("../data/db/nsi.json", "r", encoding="utf-8")
            return json.load(data)
        except Exception as exception:
            return f"Bad Request - {exception}", 400
        
    def get_all_nst(self, request):
        """Get All NSTs"""
        try:
            data = open("../data/db/nst.json", "r", encoding="utf-8")
            return json.load(data)

        except Exception as exception:
            return f"Bad Request - {exception}", 400

    def get_nst(self, id):
        """Get NSTs"""
        try:
            data = open("../data/db/nst.json", "r", encoding="utf-8")
            for item in json.load(data):
                print(item['id'] + id)
                if item['id'] == id:
                    print(item)
                    return item
        except Exception as exception:
            return f"Bad Request - {exception}", 400
        return {}


    def add_nst(self, request):
        """Get All NSSTs Core"""
        try:
            data = open("../data/db/nst.json", encoding="utf-8")
            try:
                nst_list = json.load(data)
            except Exception as exception:
                print(str(exception))
                nst_list = []
            if request.json.get("is_shared") == "on": is_shared = True
            if request.json.get("is_shared") == "": is_shared = False
                
            nst_list.append({
                "name": request.json.get("name"),
                "description": request.json.get("description"),
                "ran_nsst": request.json.get("ran_nsst"),
                "core_nsst": request.json.get("core_nsst"),
                "id": "1",
                "status": "Ready",
                "is_shared": is_shared,
                "RN_path": f"../helm_charts/ran/{request.json.get('ran_nsst')}",
                "TN_path": "",
                "CN_path": f"../helm_charts/core/{request.json.get('core_nsst')}"
            })
            f = open("../data/db/nst.json", "w", encoding="utf-8")
            print(type(nst_list[0]))
            f.write(json.dumps(nst_list))
            f.close()
            return data
        except Exception as exception:
            return f"Bad Request - {exception}", 400

    def add_nsi(self, nsi):
        """Get All NSSTs Core"""
        try:
            data = open("../data/db/nsi.json", encoding="utf-8")
            try:
                nsi_list = json.load(data)
            except Exception as exception:
                print(str(exception))
                nsi_list = []
            
            nsi_list.append(nsi)
            f = open("../data/db/nsi.json", "w", encoding="utf-8")
            f.write(json.dumps(nsi_list))
            f.close()
            return data
        except Exception as exception:
            return f"Bad Request - {exception}", 400
