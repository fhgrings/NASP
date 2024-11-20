import os
import logging
import time
import json
import requests
import time
import random
import subprocess
from .slice_config import *

BASE_HELM = "../helm_charts/*"
BASE_HELM_TMP = "/tmp/helm-nasp-temp/"
BASE_NFs = [ "nrf","amf", "nssf", "udr", "webui", "ausf", "pcf","smf", "udm", "upf", "mongodb"]


class NsmfService():
    """Nsmf Service Class"""
    def allocNsi(self, req):
        """Get All NSSTs Core"""
        try:
            logging.info("allocNSI")
            
            S_NSSAI = "1"+f"2744{int(random.random()*100)}"
            logging.info(f"S_NSSAI Selected = {S_NSSAI}")
            data = {"name": req.json["name"], "description": req.json["description"], "S_NSSAI": S_NSSAI}
            logging.info(data)
            self.add_to_db(data, "nsi")
            self.deploy_ns(req,S_NSSAI)
            return f"Alloc Completed with success", 200
        except Exception as exception:
            return f"Bad Request - {str(exception)}", 400

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
        try:
            logging.info("Start Deploy CN")
            namespace = "ns-"+nssai
            #self.create_delay(210)
            self.create_ns(namespace)
            self.create_helm_tmp(BASE_HELM)
            NFs, amf_ip = self.update_slice_config(BASE_HELM_TMP, req)
            logging.info(NFs)
            for nf in NFs:
                logging.info(self.install_helm(nf, BASE_HELM_TMP+nf, namespace))
            
            if not req.json["description"]["N3GPP Support"]:
                logging.info("Deploying RAN")
                RNFs = ["rantester"]
                for Rnf in RNFs:
                    logging.info(self.install_helm(Rnf, BASE_HELM_TMP+Rnf, namespace))

            if req.json["description"].get("Slice Attributes").get("SSQ").get("Guaranteed Flow Bit Rate - Downlink") > 100000:
                logging.info("Deploying Low latency Transport Network")
            
            logging.info("Deploying Transport")
            time.sleep(0.5)
            self.deploy_transport_network(low_latency=False)

            logging.info("Deploy Completed")
        except Exception as e:
            logging.error(f"Exception Thrown: {str(e)}")
            raise Exception(e)

    def deploy_transport_network(self, low_latency=True):
        intents = []
        short_path = [
            [("of:0000000000000001","3"),("of:0000000000000001","4")],[("of:0000000000000001","4"),("of:0000000000000001","3")],
            [("of:0000000000000004","2"),("of:0000000000000001","3")],[("of:0000000000000004","4"),("of:0000000000000001","2")]
        ]
        long_path = [
            [("of:0000000000000001","4"),("of:0000000000000001","2")],[("of:0000000000000001","2"),("of:0000000000000001","4")],
            [("of:0000000000000002","1"),("of:0000000000000002","2")],[("of:0000000000000002","2"),("of:0000000000000002","1")],
            [("of:0000000000000003","1"),("of:0000000000000003","2")],[("of:0000000000000003","2"),("of:0000000000000003","1")],
            [("of:0000000000000004","1"),("of:0000000000000004","3")],[("of:0000000000000004","4"),("of:0000000000000004","1")]
        ]
        if low_latency:
            intents = short_path
        else:
            intents = long_path
        self.deploy_onos_intents(intents)
        return

    def deploy_onos_intents(self, intents):
        for intent in intents:
            url = "http://67.205.130.238:8181/onos/v1/intents"
            headers = {'Content-Type': 'application/json','Authorization': 'Basic b25vczpyb2Nrcw=='}
            data = {
                "type": "PointToPointIntent",
                "appId": "org.onosproject.cli",
                "ingressPoint": {
                    "device": intent[0][0],
                    "port": intent[0][1]
                },
                "egressPoint": {
                    "device": intent[1][0],
                    "port": intent[1][1]
                }
            }
            response = requests.post(url, headers=headers, json=data)
            logging.info(f"Created Intent: {intent} - Response Status: {response.status_code}")
            time.sleep(0.05)
        return

    def clear_environment(self):
        self.delete_delay()
        self.delete_onos_intents()
        self.delete_ns()
        try:
            open("../data/db/nsi.json", "w", encoding="utf-8").write("[]")
            return f"Environment Cleared", 200
        except Exception as exception:
            return f"Bad Request - {exception}", 400

    def delete_ns(self):
        nsi_list = json.load(open("../data/db/nsi.json", "r"))
        for nsi in nsi_list:
            cmd = f'nohup kubectl delete ns ns-{nsi.get("S_NSSAI")} > /dev/null 2>&1 &'
            try:
                result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                return f"{nsi.get('S_NSSAI')} Deleted Succefully"
            except Exception as exception:
                raise Exception(exception.output.decode('utf-8'))
        return

    def delete_delay(self):
        cmd_list = [f'ssh 127.0.0.1 "tc qdisc del dev eth1 parent 1:1"',
                    f'ssh 127.0.0.1 "tc qdisc del dev eth1 parent 1:1"']
        for cmd in cmd_list:
            try:
                result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                return result.decode('utf-8')
            except Exception as exception:
                continue
                raise Exception(exception.output.decode('utf-8'))

    def delete_onos_intents(self):

        url = "http://67.205.130.238:8181/onos/v1/intents"
        headers = {'Authorization': 'Basic b25vczpyb2Nrcw=='}
        response = requests.get(url, headers=headers)
        for intent in response.json()["intents"]:
            requests.delete(url+"/org.onosproject.cli/"+intent["id"], headers=headers)

    def create_delay(self, delay):
        cmd_list = [f'ssh 127.0.0.1 "tc qdisc add dev eth1 root handle 1: prio;tc filter add dev eth1 parent 1:0 protocol ip prio 1 u32 match ip dst 10.116.0.3 flowid 2:1;tc qdisc add dev eth1 parent 1:1 handle 2: netem delay {delay}ms"',
                    f'ssh 165.227.202.171 "tc qdisc add dev eth1 root handle 1: prio;tc filter add dev eth1 parent 1:0 protocol ip prio 1 u32 match ip dst 10.116.0.2 flowid 2:1;tc qdisc add dev eth1 parent 1:1 handle 2: netem delay {delay-20}ms"']
        for cmd in cmd_list:
            try:
                result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                return result.decode('utf-8')
            except Exception as exception:
                raise Exception(exception.output.decode('utf-8'))
    
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
        NFs_list = BASE_NFs.copy()
        # if req["exposed"]:
        #     enable_public_ip(req)
        if req.json["description"]["N3GPP Support"]:
            NFs_list.append("n3iwf")
        # if not req["shared"]:
        #     add_all_nfs(req)
        # if req["availability"] > 99.99:
        #     add_nf_redundance()
        
        # pdu_resource((req["UE Density"]/100)+0.45)

        # update_UE_PDU_sessions(req)
        return NFs_list, "amf-free5gc-amf-amf-0.amf-service"
        
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
