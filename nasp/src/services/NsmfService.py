import os
import logging
import time
import json
import requests
import random

class NsmfService():
    """Nsmf Service Class"""
    def allocNsi(self, request):
        try:
            # SST="1"
            # SD=f"27440{random.random(0,9)}"
            # SD=f"274401"
            nst = self.get_nst(request.json['NstTemplateId'])
            logging.info("Selected NSI Template: %s", request.json['NstTemplateId'])
            SST = "1"
            SD = f"27440{int(random.random()*10)}"
            S_NSSAI = SST+SD
            print(nst['ran_nsst'].lower().replace(" ","-"))
            nsi_object = {
                "S_NSSAI": S_NSSAI,
                "SST": "1",
                "SD": SD,
                "name": nst['name'],
                "description": nst['description'],
                "status": 2,
                "NST": nst['id'],
                "ran_nssi": f"{SD}-{nst['ran_nsst'].lower().replace(' ','-')}",
                "core_nssi": f"{SD}-{nst['core_nsst'].lower().replace(' ' ,'-')}"
            }
            self.add_nsi(nsi_object)
            logging.info("Choosen S-NSSAI - SST:%s SD:%s", nsi_object['SST'], nsi_object['SD'])
            logging.info("Selecting NSSI Core...")
            response = requests.get("http://127.0.0.1:5000/nssmfCore/nsst", timeout=100)
            logging.info("NSST Core Selected - ID %s - Description: %s", response.json()[0]['id'], {response.json()[0]['description']})

            logging.info("Selecting NSSI RAN...")
            response = requests.get("http://127.0.0.1:5000/nssmfRAN/nsst", timeout=100)
            logging.info("NSST RAN Selected - ID %s - Description: %s", response.json()[0]['id'], {response.json()[0]['description']})
            logging.info("Deploying NSI SST%sSD%s", nsi_object['SST'], nsi_object['SD'])

            url = "http://localhost:5000/nssmfCore/allocNssi"
            payload = json.dumps({
                "S-NSSAI": {
                    "sst": "1",
                    "sd": "274401"
                },
                "name": "5G Core"
            })
            headers = {
            'Content-Type': 'application/json'
            }
            response = requests.put(url, headers=headers, data=payload, timeout=100)
            time.sleep(1)
            url = "http://localhost:5000/nssmfRAN/allocNssi"
            payload = json.dumps({
                "S-NSSAI": {
                    "sst": "1",
                    "sd": "274401"
                },
                "name": "N3IWF"
            })
            headers = {
            'Content-Type': 'application/json'
            }
            response = requests.request("PUT", url, headers=headers, data=payload, timeout=100)

            return "ok",200
        except Exception as exception:
            logging.error(str(exception))
            return f"Bad Request - {exception}", 400

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
